/*  This file is part of Jellyfish.

    Jellyfish is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Jellyfish is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Jellyfish.  If not, see <http://www.gnu.org/licenses/>.
*/

#include <cstdlib>
#include <unistd.h>
#include <assert.h>
#include <signal.h>

#include <cctype>
#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <map>
#include <sstream>
#include <memory>
#include <chrono>

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <jellyfish/err.hpp>
#include <jellyfish/thread_exec.hpp>
#include <jellyfish/hash_counter.hpp>
#include <jellyfish/locks_pthread.hpp>
#include <jellyfish/stream_manager.hpp>
#include <jellyfish/mer_overlap_sequence_parser.hpp>
#include <jellyfish/whole_sequence_parser.hpp>
#include <jellyfish/mer_iterator.hpp>
#include <jellyfish/mer_qual_iterator.hpp>
#include <jellyfish/jellyfish.hpp>
#include <jellyfish/merge_files.hpp>
#include <jellyfish/mer_dna_bloom_counter.hpp>
#include <jellyfish/generator_manager.hpp>
#include <jellyfish/randomc.h>
#include <sub_commands/count_main_cmdline.hpp>
#include <sys/time.h>
#include <sys/resource.h>

// Measure peak memory usage
double measurePeakMemory(){
  struct rusage t;
  getrusage(RUSAGE_SELF, &t);
  return ((double)((size_t)t.ru_maxrss))/1000.0;
}
static count_main_cmdline args; // Command line switches and arguments

namespace err = jellyfish::err;

using std::chrono::system_clock;
using std::chrono::duration;
using std::chrono::duration_cast;

template<typename DtnType>
inline double as_seconds(DtnType dtn) { return duration_cast<duration<double>>(dtn).count(); }

using jellyfish::mer_dna;
using jellyfish::mer_dna_bloom_counter;
using jellyfish::mer_dna_bloom_filter;
typedef std::vector<const char*> file_vector;
typedef jellyfish::stream_manager<file_vector::const_iterator> stream_manager_type;

// Types for parsing arbitrary sequence ignoring quality scores
typedef jellyfish::mer_overlap_sequence_parser<stream_manager_type> sequence_parser;
typedef jellyfish::mer_iterator<sequence_parser, mer_dna> mer_iterator;

// Types for parsing reads with quality score. Interface match type
// above.
class sequence_qual_parser :
  public jellyfish::whole_sequence_parser<jellyfish::stream_manager<file_vector::const_iterator> >
{
  typedef jellyfish::stream_manager<file_vector::const_iterator> StreamIterator;
  typedef jellyfish::whole_sequence_parser<StreamIterator> super;
public:
  sequence_qual_parser(uint16_t mer_len, uint32_t max_producers, uint32_t size, size_t buf_size,
                       StreamIterator& streams) :
    super(size, 100, max_producers, streams)
  { }
};

class mer_qual_iterator : public jellyfish::mer_qual_iterator<sequence_qual_parser, mer_dna> {
  typedef jellyfish::mer_qual_iterator<sequence_qual_parser, mer_dna> super;
public:
  static char min_qual;
  mer_qual_iterator(sequence_qual_parser& parser, bool canonical = false) :
    super(parser, min_qual, canonical)
  { }
};
char mer_qual_iterator::min_qual = '!'; // Phred+33

// k-mer filters. Organized in a linked list, interpreted as a &&
// (logical and). I.e. all filter must return true for the result to
// be true. By default, filter returns true.
struct filter {
  filter* prev_;
  filter(filter* prev = 0) : prev_(prev) { }
  virtual ~filter() { }
  virtual bool operator()(const mer_dna& x) { return and_res(true, x); }
  bool and_res(bool r, const mer_dna& x) const {
    return r ? (prev_ ? (*prev_)(x) : true) : false;
  }
};

struct filter_bc : public filter {
  const mer_dna_bloom_counter& counter_;
  filter_bc(const mer_dna_bloom_counter& counter, filter* prev = 0) :
    filter(prev),
    counter_(counter)
  { }
  bool operator()(const mer_dna& m) {
    unsigned int c = counter_.check(m);
    return and_res(c > 1, m);
  }
};

struct filter_bf : public filter {
  mer_dna_bloom_filter& bf_;
  filter_bf(mer_dna_bloom_filter& bf, filter* prev = 0) :
    filter(prev),
    bf_(bf)
  { }
  bool operator()(const mer_dna& m) {
    unsigned int c = bf_.insert(m);
    return and_res(c > 0, m);
  }
};

enum OPERATION { COUNT, PRIME, UPDATE, FIRST_PASS, SECOND_PASS, SAMPLING_PASS, DATASET_SIZE };
template<typename MerIteratorType, typename ParserType>
class mer_counter_base : public jellyfish::thread_exec {
  int                  nb_threads_;
  mer_hash&            ary_;
  ParserType           parser_;
  filter*              filter_;
  OPERATION            op_;
  double set_probability;
  double sampling_parameter;

public:
  mer_counter_base(int nb_threads, mer_hash& ary, stream_manager_type& streams,
                   OPERATION op, filter* filter = new struct filter , double set_probability_ = 1.0)
    : ary_(ary)
    , parser_(mer_dna::k(), streams.nb_streams(), 3 * nb_threads, 4096, streams)
    , filter_(filter)
    , op_(op)
    , set_probability(set_probability_)
  { }

  virtual void start(int thid) {
    size_t count = 0;
    MerIteratorType mers(parser_, args.canonical_flag);

    switch(op_) {
     case COUNT:
     {
     long long total = 0;
      for( ; mers; ++mers) {
        if((*filter_)(*mers)){
          ary_.add(*mers, 1);
          ++total;
        }
      }
      {
        std::stringstream msg;
        msg << thid << " full pass: finished and inserted " << total << "\n";
        std::cout << msg.str() << std::endl;
      }
    }
      break;


       case DATASET_SIZE:
       {
       long long total = 0;

       {
         std::stringstream msg;
         msg << thid << " computing dataset size... \n";
         std::cout << msg.str() << std::endl;
       }

        for( ; mers; ++mers) {
          if((*filter_)(*mers)){
            ++total;
          }
        }
        {
          std::stringstream msg;
          msg << thid << " dataset size: " << total << "\n";
          std::cout << msg.str() << std::endl;
        }
      }
      break;

      case SAMPLING_PASS:
      {

        int insert_amount = 0;
        long long total = 0;
        int max_insert_amount = 0;
        //int count_2 = 0;
        //bool insert = false;
        //bool __debug1__ = false;
        //bool __debug2__ = false;
        double random_number = 0.0;
        double e_minus_lambda = exp(-set_probability);
        double poisson_probability_ = e_minus_lambda;
        int seed = rand() % 1000;
        CRandomMersenne rng_(seed);

        {
          std::stringstream msg;
          msg << thid << " e_minus_lambda " << e_minus_lambda << "\n";
          msg << thid << " seed " << seed;
          std::cout << msg.str() << std::endl;
        }

        for( ; mers; ++mers) {
            ++total;
            random_number = rng_.Random();
            poisson_probability_ = random_number;
            /*if(__debug1__){
              std::cout << thid << " random_number " << random_number << std::endl;
              std::cout << thid << "    poisson_threshold_ " << poisson_threshold_ << std::endl;
              std::cout << thid << "    insert_amount " << insert_amount << std::endl;
              if(__debug2__){++count_2;}
            }*/
            if(poisson_probability_ > e_minus_lambda){
              while (poisson_probability_ > e_minus_lambda){
                random_number = rng_.Random();
                insert_amount = insert_amount + 1;
                poisson_probability_ = poisson_probability_ * random_number;
                /*if(__debug1__){
                  std::cout << thid << " random_number " << random_number << std::endl;
                  std::cout << thid << "    poisson_probability_ " << poisson_probability_ << std::endl;
                  std::cout << thid << "    insert_amount-1 " << (int)(insert_amount-1) << std::endl;
                  std::cout << thid << "    max_insert_amount " << max_insert_amount << std::endl;
                }*/
                /*if(max_insert_amount < insert_amount){
                  max_insert_amount = insert_amount;
                }*/
              }
              insert_amount = insert_amount - 1;
              if(insert_amount > 0 && (*filter_)(*mers)){
                ary_.add(*mers, insert_amount);
                count = count + insert_amount;
                /*if(__debug2__){
                  std::cout << thid << " inserted k " << *mers << std::endl;
                  std::cout << thid << "    insert_amount " << insert_amount << std::endl;
                  std::cout << thid << "    insert so far " << count << std::endl;
                  std::cout << thid << "    total " << count_2 << std::endl;
                  std::cout << thid << "    ratio " << (double)count / (double)count_2 << std::endl;
                }*/
              }
              insert_amount = 1;
            }
          //std::cout << thid << " first " << *first << std::endl;
          //std::cout << thid << " diff " << first - mers << std::endl;
        }
        {
          std::stringstream msg;
          msg << thid << " sampling pass: finished and inserted " << count << "\n";
          msg << thid << "    max_insert_amount " << max_insert_amount << "\n";
          msg << thid << "    passed kmers " << total << "\n";
          msg << thid << "    ratio " << (double)count/(double)total << "\n";
          std::cout << msg.str() << std::endl;
        }
        /*std::cout << thid << " sampling pass: finished and inserted " << count << std::endl;
        std::cout << thid << "    max_insert_amount " << max_insert_amount << std::endl;
        std::cout << thid << "    total " << total << std::endl;
        std::cout << thid << "    ratio " << (double)count/(double)total << std::endl;*/
      }

        break;

    case FIRST_PASS:
    {

      bool insert = true;
      int total = 0;
      double prob = set_probability;
      int seed = rand() % 1000;
      CRandomMersenne rng_(seed);
      std::cout << thid << " seed " << seed << std::endl;

      for( ; mers; ++mers) {
          insert = rng_.Random() > prob;
          if(insert && (*filter_)(*mers)){
          ary_.set(*mers);
          //std::cout << thid << " inserted k " << *mers << std::endl;
          //std::cout << rng_.Random() << std::endl;
          ++count;
        }
        //std::cout << thid << " first " << *first << std::endl;
        //std::cout << thid << " diff " << first - mers << std::endl;
        ++total;
      }
      std::cout << thid << " first pass: finished and inserted " << count << std::endl;
      std::cout << thid << "    total " << total << std::endl;
      std::cout << thid << "    ratio " << (double)count/(double)total << std::endl;
    }

      break;

    case SECOND_PASS:
    {
      mer_dna tmp_;
      for( ; mers; ++mers) {
        if((*filter_)(*mers)){
          if(ary_.update_add(*mers, 1, tmp_)){
            //std::cout << thid << " increased count of k " << *mers << std::endl;
            ++count;
          }
        }
      }
      std::cout << thid << " second pass: finished and counted " << count << std::endl;
    }

      break;

    case PRIME:
      for( ; mers; ++mers) {
        if((*filter_)(*mers))
          ary_.set(*mers);
        ++count;
      }
      break;

    case UPDATE:
      mer_dna tmp;
      for( ; mers; ++mers) {
        if((*filter_)(*mers))
          ary_.update_add(*mers, 1, tmp);
        ++count;
      }
      break;
    }

    ary_.done();
  }
};

// Counter with and without quality value
typedef mer_counter_base<mer_iterator, sequence_parser> mer_counter;
typedef mer_counter_base<mer_qual_iterator, sequence_qual_parser> mer_qual_counter;

mer_dna_bloom_counter* load_bloom_filter(const char* path) {
  std::ifstream in(path, std::ios::in|std::ios::binary);
  jellyfish::file_header header(in);
  if(!in.good())
    err::die(err::msg() << "Failed to parse bloom filter file '" << path << "'");
  if(header.format() != "bloomcounter")
    err::die(err::msg() << "Invalid format '" << header.format() << "'. Expected 'bloomcounter'");
  if(header.key_len() != mer_dna::k() * 2)
    err::die("Invalid mer length in bloom filter");
  jellyfish::hash_pair<mer_dna> fns(header.matrix(1), header.matrix(2));
  auto res = new mer_dna_bloom_counter(header.size(), header.nb_hashes(), in, fns);
  if(!in.good())
    err::die("Bloom filter file is truncated");
  in.close();
  return res;
}

// If get a termination signal, kill the manager and then kill myself.
static pid_t manager_pid = 0;
static void signal_handler(int sig) {
  if(manager_pid)
    kill(manager_pid, SIGTERM);
  signal(sig, SIG_DFL);
  kill(getpid(), sig);
  _exit(EXIT_FAILURE); // Should not be reached
}

int count_main(int argc, char *argv[])
{
  auto start_time = system_clock::now();

  std::cout << " count_main started " << std::endl;
  std::cout.precision(15);

  srand(system_clock::now().time_since_epoch().count());

  jellyfish::file_header header;
  header.fill_standard();
  header.set_cmdline(argc, argv);

  args.parse(argc, argv);

#ifndef HAVE_HTSLIB
  if(args.sam_given)
    count_main_cmdline::error() << "SAM/BAM/CRAM not supported (missing htslib).";
#endif


  if(args.min_qual_char_given) {
    if(args.min_qual_char_arg.size() != 1)
      count_main_cmdline::error("[-Q, --min-qual-char] must be one character.");
    const char min_qual = args.min_qual_char_arg[0];
    if(!isprint(min_qual))
      count_main_cmdline::error () << "Invalid non-printable quality character";
    if(min_qual < '!' || min_qual > '~')
      count_main_cmdline::error() << "Quality character '" << min_qual
                                  << "' is outside of the range [!, ~]";
    mer_qual_iterator::min_qual = min_qual;
  }
  if(args.min_quality_given) {
    if(args.quality_start_arg < '!' || args.quality_start_arg > '~')
      count_main_cmdline::error() << "Quality start " << args.quality_start_arg
                                  << " is outside the range [" << (int)'!' << ", "
                                  << (int)'~' << ']';
    int min_qual = args.quality_start_arg + args.min_quality_arg;
    if(min_qual < '!' || min_qual > '~')
      count_main_cmdline::error() << "Min quality " << args.min_quality_arg
                                  << " is outside the range [0, "
                                  << ((int)'~' - args.quality_start_arg) << ']';
    mer_qual_iterator::min_qual = min_qual;
  }

  mer_dna::k(args.mer_len_arg);

  std::unique_ptr<jellyfish::generator_manager> generator_manager;
  if(args.generator_given) {
    auto gm =
      new jellyfish::generator_manager(args.generator_arg, args.Generators_arg,
                                       args.shell_given ? args.shell_arg : (const char*)0);
    generator_manager.reset(gm);
    generator_manager->start();
    manager_pid = generator_manager->pid();
    struct sigaction act;
    memset(&act, '\0', sizeof(act));
    act.sa_handler = signal_handler;
    assert(sigaction(SIGTERM, &act, 0) == 0);
  }

  header.canonical(args.canonical_flag);
  mer_hash ary(args.size_arg, args.mer_len_arg * 2, args.counter_len_arg, args.threads_arg, args.reprobes_arg);
  if(args.disk_flag)
    ary.do_size_doubling(false);

  std::unique_ptr<jellyfish::dumper_t<mer_array> > dumper;
  if(args.text_flag)
    dumper.reset(new text_dumper(args.threads_arg, args.output_arg, &header));
  else
    dumper.reset(new binary_dumper(args.out_counter_len_arg, ary.key_len(), args.threads_arg, args.output_arg, &header));
  ary.dumper(dumper.get());

  auto after_init_time = system_clock::now();

  OPERATION do_op = COUNT;
  if(args.if_given) {
    stream_manager_type streams(args.Files_arg);
    streams.paths(args.if_arg.begin(), args.if_arg.end());
    mer_counter counter(args.threads_arg, ary, streams, PRIME);
    counter.exec_join(args.threads_arg);
    do_op = UPDATE;
  }

  // Iterators to the multi pipe paths. If no generator manager,
  // generate an empty range.
  auto pipes_begin = generator_manager.get() ? generator_manager->pipes().begin() : args.file_arg.end();
  auto pipes_end = (bool)generator_manager ? generator_manager->pipes().end() : args.file_arg.end();

  stream_manager_type streams(args.Files_arg);
  streams.paths(args.file_arg.begin(), args.file_arg.end());
  streams.pipes(pipes_begin, pipes_end);
  #ifdef HAVE_HTSLIB
  streams.sams(args.sam_arg.begin(), args.sam_arg.end());
  #endif

  // Bloom counter read from file to filter out low frequency
  // k-mers. Two pass algorithm.
  std::unique_ptr<filter> mer_filter(new filter);
  std::unique_ptr<mer_dna_bloom_counter> bc;
  if(args.bc_given) {
    bc.reset(load_bloom_filter(args.bc_arg));
    mer_filter.reset(new filter_bc(*bc));
  }

  // Bloom filter to filter out low frequency k-mers. One pass
  // algorithm.
  std::unique_ptr<mer_dna_bloom_filter> bf;
  if(args.bf_size_given) {
    bf.reset(new mer_dna_bloom_filter(args.bf_fp_arg, args.bf_size_arg));
    mer_filter.reset(new filter_bf(*bf));
  }



  double prob_to_pass = 1.0;

  if(args.dbsize_flag){
    do_op = DATASET_SIZE;
  }
  else
  if(args.lambda_arg < 1.0){
    std::cout << " sampling mode (one pass) selected " << std::endl;
    std::cout << " args.lambda_arg " << args.lambda_arg << std::endl;
    do_op = SAMPLING_PASS;
    prob_to_pass = args.lambda_arg;
  }

  std::cout << " starting to count... " << std::endl;

  if(args.min_qual_char_given || args.min_quality_given) {
    mer_qual_counter counter(args.threads_arg, ary, streams,
                             do_op, mer_filter.get(), prob_to_pass);
    counter.exec_join(args.threads_arg);
  } else {
    mer_counter counter(args.threads_arg, ary, streams,
                        do_op, mer_filter.get(), prob_to_pass);
    counter.exec_join(args.threads_arg);
  }

  // If we have a manager, wait for it
  if(generator_manager) {
    signal(SIGTERM, SIG_DFL);
    manager_pid = 0;
    if(!generator_manager->wait())
      err::die("Some generator commands failed");
    generator_manager.reset();
  }


  // SECOND PASS

  if(do_op == FIRST_PASS){

    std::cout << " first pass end " << std::endl;

    std::cout << " second pass begin " << std::endl;

    do_op = SECOND_PASS;

    // Iterators to the multi pipe paths. If no generator manager,
    // generate an empty range.
    pipes_begin = generator_manager.get() ? generator_manager->pipes().begin() : args.file_arg.end();
    pipes_end = (bool)generator_manager ? generator_manager->pipes().end() : args.file_arg.end();

    stream_manager_type streams_(args.Files_arg);
    streams_.paths(args.file_arg.begin(), args.file_arg.end());
    streams_.pipes(pipes_begin, pipes_end);
    #ifdef HAVE_HTSLIB
    streams_.sams(args.sam_arg.begin(), args.sam_arg.end());
    #endif

    std::cout << " starting to count... " << std::endl;

    if(args.min_qual_char_given || args.min_quality_given) {
      mer_qual_counter counter(args.threads_arg, ary, streams_,
                               do_op, mer_filter.get());
      counter.exec_join(args.threads_arg);
    } else {
      mer_counter counter(args.threads_arg, ary, streams_,
                          do_op, mer_filter.get());
      counter.exec_join(args.threads_arg);
    }

    // If we have a manager, wait for it
    if(generator_manager) {
      signal(SIGTERM, SIG_DFL);
      manager_pid = 0;
      if(!generator_manager->wait())
        err::die("Some generator commands failed");
      generator_manager.reset();
    }

    std::cout << " second pass end " << std::endl;

  }

  // SECOND PASS END




  auto after_count_time = system_clock::now();

  // If no intermediate files, dump directly into output file. If not, will do a round of merging
  if(!args.no_write_flag) {
    if(dumper->nb_files() == 0) {
      dumper->one_file(true);
      if(args.lower_count_given)
        dumper->min(args.lower_count_arg);
      if(args.upper_count_given)
        dumper->max(args.upper_count_arg);
      dumper->dump(ary.ary());
    } else {
      dumper->dump(ary.ary());
      if(!args.no_merge_flag) {
        std::vector<const char*> files = dumper->file_names_cstr();
        uint64_t min = args.lower_count_given ? args.lower_count_arg : 0;
        uint64_t max = args.upper_count_given ? args.upper_count_arg : std::numeric_limits<uint64_t>::max();
        try {
          merge_files(files, args.output_arg, header, min, max);
        } catch(MergeError &e) {
          err::die(err::msg() << e.what());
        }
        if(!args.no_unlink_flag) {
          for(int i =0; i < dumper->nb_files(); ++i)
            unlink(files[i]);
        }
      } // if(!args.no_merge_flag
    } // if(!args.no_merge_flag
  }

  auto after_dump_time = system_clock::now();

  if(args.timing_given) {
    std::ofstream timing_file(args.timing_arg);
    timing_file << "Init     " << as_seconds(after_init_time - start_time) << "\n"
                << "Counting " << as_seconds(after_count_time - after_init_time) << "\n"
                << "Writing  " << as_seconds(after_dump_time - after_count_time) << "\n";
  }

  std::cout << "Init     " << as_seconds(after_init_time - start_time) << "\n"
  << "Counting " << as_seconds(after_count_time - after_init_time) << "\n"
  << "Writing  " << as_seconds(after_dump_time - after_count_time) << "\n"
  << "Total running time  " << as_seconds(after_count_time - start_time) << "\n";
  std::cout << "Peak Memory (MB):  " << (int)measurePeakMemory() << std::endl;

  return 0;
}
