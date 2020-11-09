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

#include <config.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <iostream>
#include <fstream>
#include <limits>
#include <vector>
#include <unordered_set>
#include <unordered_map>
#include <chrono>
#include <cstdlib>
#include <math.h>

#include <jellyfish/err.hpp>
#include <jellyfish/misc.hpp>
#include <jellyfish/fstream_default.hpp>
#include <jellyfish/jellyfish.hpp>
#include <jellyfish/hash_counter.hpp>
#include <jellyfish/randomc.h>
#include <sub_commands/dump_main_cmdline.hpp>
#include <sys/time.h>
#include <sys/resource.h>
#include <boost/functional/hash.hpp>

namespace err = jellyfish::err;

using std::chrono::system_clock;
using std::chrono::duration;
using std::chrono::duration_cast;

template<typename DtnType>
inline double as_seconds(DtnType dtn) { return duration_cast<duration<double>>(dtn).count(); }

static dump_main_cmdline args; // Command line switches and arguments

typedef std::vector<uint8_t> key_type;

void get_key(key_type& key , std::string& kmer , std::unordered_map<char, int>& nucleotide_map , int mer_len_arg){
  int j = 0;
  int size_ = (int)key.size();
  for(j=0; j < size_; j++){
    key[j] = 0;
  }
  j = 0;
  for(int i=0; i < mer_len_arg; i++){
    //std::cout << kmer[i];
    //std::cout << nucleotide_map[kmer[i]];
    key[j] = key[j] * 4;
    key[j] += nucleotide_map[kmer[i]];
    j = ((i+1) % 4 == 0) ? j + 1 : j;
    //std::cout << "   character " << kmer[i] << std::endl;
    //std::cout << "   mapped to " << nucleotide_map[kmer[i]] << std::endl;
    //std::cout << "   key " << key << std::endl;
  }
  //std::cout << std::endl;
  //return key;
}

//template<typename iterator>
void dist(std::string& db1, std::string& db2, std::ostream &out , double dist_ratio1 , double dist_ratio2) {
  typedef unsigned long long large_integer;
  typedef long double large_double;
  large_integer total_1 = 0;
  long long total_2 = 0;
  long long dist_sum = 0;
  large_double freq_sum_of_abs_diff = 0.0;
  large_double sum_of_products = 0.0;
  large_double sum_of_squared_counts1 = 0.0;
  large_double sum_of_squared_counts2 = 0.0;
  int mer_len_arg = 0;
  std::unordered_map< key_type , int , boost::hash<key_type> > kmers_map;
  std::unordered_map<char, int> nucleotide_map = {
        {'A',0},
        {'C',1},
        {'G',2},
        {'T',3}
  };
  key_type key;
  std::string line;
  std::string kmer;
  std::string count;
  large_double count_ = 0.0;
  int scaled_count = 0;
  long long count1 = 0;
  long long count2 = 0;
  large_double max_elem1 = 0.0;
  large_double max_elem2 = 0.0;

  // compute total_1
  std::ifstream is1(db1);
  while (std::getline(is1, line))
  {
    std::stringstream linestream(line);
    std::getline(linestream,count,';');
    count_ = std::stod(count);
    if (count_ >= args.lower_count_arg){
      ++count1;
      scaled_count = (int)(count_ * dist_ratio1 + 0.5);
      total_1 += scaled_count;
      max_elem1 = (max_elem1 < scaled_count) ? scaled_count : max_elem1;
    }
  }
  is1.close();
  std::cout << " first total count " << total_1 << std::endl;
  std::cout << " first distinct " << count1 << std::endl;
  std::cout << " max_elem1 " << max_elem1 << std::endl;
  // compute total_2
  std::ifstream is2(db2);
  while (std::getline(is2, line))
  {
    std::stringstream linestream(line);
    std::getline(linestream,count,';');
    count_ = std::stod(count);
    if (count_ >= args.lower_count_arg){
      ++count2;
      scaled_count = (int)(count_ * dist_ratio2 + 0.5);
      total_2 += scaled_count;
      max_elem2 = (max_elem2 < scaled_count) ? scaled_count : max_elem2;
    }
  }
  is2.close();
  std::cout << " second total count " << total_2 << std::endl;
  std::cout << " second distinct " << count2 << std::endl;
  std::cout << " max_elem2 " << max_elem2 << std::endl;

  std::cout << " loading hash table... " << std::endl;

  std::ifstream it1(db1);
  {
    std::getline(it1, line);
    std::stringstream linestream(line);
    std::getline(linestream,count,';');
    std::getline(linestream,kmer,';');
    mer_len_arg = kmer.length();
    key.resize((int)ceil((double)mer_len_arg / 4.0));
    std::cout << mer_len_arg << std::endl;
    std::cout << kmer << " " << count_ << std::endl;
    count_ = std::stod(count);
    if (count_ >= args.lower_count_arg){
      get_key(key , kmer , nucleotide_map , mer_len_arg);
      scaled_count = (int)(count_ * dist_ratio1 + 0.5);
      kmers_map[key] = scaled_count;
    }
  }
  while (std::getline(it1, line))
  {
    std::stringstream linestream(line);
    std::getline(linestream,count,';');
    std::getline(linestream,kmer,';');
    count_ = std::stod(count);
    if (count_ >= args.lower_count_arg){
      get_key(key , kmer , nucleotide_map , mer_len_arg);
      scaled_count = (int)(count_ * dist_ratio1 + 0.5);
      if(kmers_map[key] > 0){
        std::cerr << " problem! " << kmer << std::endl;
      }
      kmers_map[key] = scaled_count;
    }
  }
  //it1.key().to_str(buffer);
  //std::cout << " first char " << buffer[0] << std::endl;
  //int counter_len_arg = 7;
  //int threads_arg = 1;
  //int reprobes_arg = 126;
  //mer_hash ary(size_arg, mer_len_arg * 2, counter_len_arg, threads_arg, reprobes_arg);


  std::cout << " reading second dataset... " << std::endl;

  int map_value = 0;
  large_double freq1 = 0.0;
  large_double freq2 = 0.0;
  large_double d_total_1 = (large_double)total_1;
  large_double d_total_2 = (large_double)total_2;
  large_double scaled_value1 = 0.0;
  large_double scaled_value2 = 0.0;
  long long in_common_elements = 0;
  std::ifstream it2(db2);
  while (std::getline(it2, line))
  {
    std::stringstream linestream(line);
    std::getline(linestream,count,';');
    std::getline(linestream,kmer,';');
    count_ = std::stod(count);
    if (count_ >= args.lower_count_arg){
      get_key(key , kmer , nucleotide_map , mer_len_arg);
      map_value = kmers_map[key];
      in_common_elements += (map_value > 0);
      scaled_count = (int)(count_ * dist_ratio2 + 0.5);
      dist_sum += (map_value < scaled_count) ? map_value : scaled_count;
      //total_2 += (map_value > 0 && scaled_count > 0) ? scaled_count : 0;
      freq1 = (large_double)map_value / d_total_1;
      freq2 = (large_double)scaled_count / d_total_2;
      freq_sum_of_abs_diff += (freq1 > freq2) ? freq1 - freq2 : freq2 - freq1;
      scaled_value1 = (large_double)map_value / max_elem1;
      scaled_value2 = (large_double)scaled_count / max_elem2;
      sum_of_products += scaled_value1 * scaled_value2;
      sum_of_squared_counts1 += scaled_value1 * scaled_value1;
      sum_of_squared_counts2 += scaled_value2 * scaled_value2;
    }


    /*if(scaled_count && map_value){
      std::cout << "kmer " << kmer << std::endl;
      std::cout << "scaled_count " << scaled_count << std::endl;
      std::cout << "scaled_count**2 " << (long long)scaled_count * (long long)scaled_count << std::endl;
      std::cout << "  map_value " << map_value << std::endl;
      std::cout << "  map_value**2 " << (long long)map_value * (long long)map_value << std::endl;
      std::cout << "  sum_of_products " << sum_of_products << std::endl;
      std::cout << "  sum_of_squared_counts1 " << sum_of_squared_counts1 << std::endl;
      std::cout << "  sum_of_squared_counts2 " << sum_of_squared_counts2 << std::endl;
      long double denominator_ = sqrt((long double)sum_of_squared_counts1)*sqrt((long double)sum_of_squared_counts2);
      std::cout << "  denominator " << denominator_ << std::endl;
      std::cout << "  result " << (long double)sum_of_products / denominator_ << std::endl;
    }*/

  }

  large_integer total_sum = total_1 + total_2;
  std::cout << " dist_sum " << dist_sum << std::endl;
  std::cout << " total_sum " << total_sum << std::endl;
  large_double bray_curtis = 1.0 - (large_double)dist_sum / (large_double)total_sum * 2.0;
  std::cout << " Bray-Curtis distance " << bray_curtis << std::endl;
  large_double whittaker = 0.5 * freq_sum_of_abs_diff;
  std::cout << " Whittaker distance " << whittaker << std::endl;
  large_double denom1 = sqrt(sum_of_squared_counts1);
  large_double denom2 = sqrt(sum_of_squared_counts2);
  large_double denom = denom1 * denom2;
  large_double cosdist = (sum_of_products  / denom );
  large_double factor = 2.0 * cosdist;
  large_double chord = sqrt(2.0 - factor);
  std::cout << " Chord distance " << chord << std::endl;
  large_double jaccard = (large_double)in_common_elements / (large_double)(count1 + count2);
  std::cout << " Jaccard distance " << jaccard << std::endl;


}

//#define DEBUG_ 1
//#define MULTIPLE_ELLS 1

template<typename iterator>
void dump(iterator& it, std::ostream &out,
          uint64_t lower_count, uint64_t upper_count) {

  if(args.bagsell_arg > 1) {
    std::cout.precision(10);
    double delta = args.delta_arg / 2.0;
    double theta = args.theta_arg;
    #ifdef MULTIPLE_ELLS
    std::vector<double> deviations;
    std::vector<long double> ells;
    #endif
    int ell = args.bagsell_arg;
    double total_number = (double)args.totalkmers_arg;
    int buckets = (int)(total_number / (double)ell + 0.5);
    std::cout << " sampling out mode selected " << std::endl;
    std::cout << " number of kmers in sample " << total_number << std::endl;
    std::cout << " ell " << ell << std::endl;
    double epsilon = 1.0 / (double)ell * ( sqrt( 2.0 * (floor(log2((double)ell) + 1.0) + log(1.0 / delta)) / (double)buckets) );
    std::cout << " epsilon " << epsilon << std::endl;
    double max_deviation = epsilon / 2.0;
    std::cout << " max_deviation " << max_deviation << std::endl;
    if(theta == 0.0){
      theta = epsilon + 2.0 / total_number;
    }
    std::cout << " theta " << theta << std::endl;
    std::cout << " theta * t " << theta * total_number << std::endl;
    double support_lower_bound_filtering = total_number * (theta - max_deviation);
    std::cout << " support_lower_bound_filtering " << support_lower_bound_filtering << std::endl;
    lower_count = (int)(support_lower_bound_filtering + 1.0);
    std::cout << " lower_count " << lower_count << std::endl;
    double biased_freq = 0.0;
    double frequency = 0.0;
    int seed = rand() % 1000;
    int i = 0;
    int supp_a = 0;
    int index = 0;
    long distinct_elements = 0;
    long results = 0;
    CRandomMersenne rng_(seed);
    std::cout << " buckets " << buckets << std::endl;
    long temp_ = (long)buckets * (long)ell;
    std::cout << " buckets * ell " << temp_ << std::endl;
    std::cout << " total_number " << total_number << std::endl;
    std::cout << " buckets " << buckets << std::endl;
    std::cout << " max biased support1 " << (double)buckets / total_number << std::endl;
    std::cout << " min biased support1 " << 1.0 / total_number << std::endl;
    std::cout << " max biased support2 " << (double)buckets / (double)(temp_) << std::endl;
    std::cout << " min biased support2 " << 1.0 / (double)(temp_) << std::endl;

    #ifdef MULTIPLE_ELLS
    double buckets_temp = buckets;
    int num_of_partitions = 0;
    double max_freq = 10000.0 / total_number;
    double ell_temp = double(ell);
    double epsilon_temp = epsilon;
    deviations.reserve(30);
    ells.reserve(30);
    while(epsilon_temp/2.0 < max_freq){
      deviations.push_back(epsilon_temp / 2.0);
      ells.push_back(ell_temp);
      num_of_partitions++;
      buckets_temp = buckets_temp * 2.0;
      ell_temp = floor(total_number / buckets_temp);
      epsilon_temp = 1.0 / ell_temp * ( sqrt( 2.0 * (floor(log2(ell_temp) + 1.0) + log(1.0 / delta)) / buckets_temp) );
      //std::cout << " epsilon_temp    " << epsilon_temp << std::endl;
      //std::cout << "   ell_temp      " << ell_temp << std::endl;
      //std::cout << "   buckets_temp  " << buckets_temp << std::endl;
    }
    std::cout << " num_of_partitions " << num_of_partitions << std::endl;
    long num_part_pow_2 = pow(2 , num_of_partitions-1);
    buckets = buckets * num_part_pow_2;
    std::cout << " new buckets " << buckets << std::endl;
    ell = floor(total_number / (double)buckets);
    std::cout << " new ell " << ell << std::endl;
    #endif

    std::vector<int> ell_counts(buckets , ell);
    std::vector<int> buckets_indexes(buckets);
    std::unordered_set<int> biased_count;
    std::unordered_set<int> biased_count2;
    long _temp = (long)total_number;
    for(i = 0; i < buckets; i++){
      _temp -= ell;
      buckets_indexes[i] = i;
    }
    std::cout << " left out of buckets " << _temp << std::endl;
    i = 0;
    while(_temp > 0){
      --_temp;
      ++ell_counts[i];
      ++i;
      i = i % buckets;
    }
    /*for(i = 0; i < ell_counts.size(); i++){
      std::cout << "ell_counts[" << i << "] = " << ell_counts[i] << std::endl;
      std::cout << "  buckets_indexes[" << i << "] = " << buckets_indexes[i] << std::endl;
    }*/
    long double d_ell = (long double)ell;
    long double upper_bound = 1.0;
    long double lower_bound = 0.0;
    long double temp_bound = 0.0;
    int buckets_rand_max = buckets-1;
    std::cout << " max_deviation (to be sure) " << max_deviation << std::endl;
    std::cout << " theta (to be sure) " << theta << std::endl;
    while(it.next()) {
      ++distinct_elements;
      if(it.val() < lower_count || it.val() > upper_count)
        continue;
      supp_a = it.val();
      frequency = (double)supp_a / total_number;

      // compute biased count
      #ifdef MULTIPLE_ELLS
      biased_count.clear();
      #endif
      biased_count2.clear();
      for(i = 0; i < supp_a; i++){
        // random index in [0,buckets)
        index = rng_.IRandom(0 , buckets_rand_max);
        ell_counts[index] -= 1;
        if(ell_counts[index] == 0 && buckets > 1){
          std::cout << "index " << index << " is now zero" << std::endl;
          // swap count
          ell_counts[index] = ell_counts[buckets-1];
          ell_counts[buckets-1] = 0;
          // swap index
          int temp_index = buckets_indexes[index];
          buckets_indexes[index] = buckets_indexes[buckets-1];
          buckets_indexes[buckets-1] = temp_index;
          index = buckets-1;
          buckets -= 1;
          buckets_rand_max = buckets - 1;
        }
        // cout number of distinct buckets for current k-mer
        #ifdef MULTIPLE_ELLS
        biased_count.insert(buckets_indexes[index]);
        biased_count2.insert(buckets_indexes[index] / num_part_pow_2);
        #endif
        #ifndef MULTIPLE_ELLS
        biased_count2.insert(buckets_indexes[index]);
        #endif
        //std::cout << "buckets_indexes[index]                     = " << buckets_indexes[index] << std::endl;
        //std::cout << "   num_part_pow_2                          = " << num_part_pow_2 << std::endl;
        //std::cout << "   buckets_indexes[index] / num_part_pow_2 = " << buckets_indexes[index] / num_part_pow_2 << std::endl;

      }

      biased_freq = (double)biased_count2.size() / total_number;
      //std::cout << "(not freq) biased_freq = " << biased_freq << std::endl;
      // output only frequent
      if(biased_freq + max_deviation >= theta){
        #ifdef DEBUG_
        //std::cout << "frequency = " << frequency << std::endl;
        //std::cout << "   biased_freq = " << biased_freq << std::endl;
        #endif

        upper_bound = 1.0;
        lower_bound = biased_freq - max_deviation;
        #ifdef MULTIPLE_ELLS
        d_ell = ells[0];
        #endif

        temp_bound = 1.0 - d_ell * (biased_freq + max_deviation);
        temp_bound = (temp_bound > 0.0) ? 1.0 - pow(temp_bound , 1.0 / d_ell) : 1.0;
        upper_bound = (upper_bound < temp_bound) ? upper_bound : temp_bound;
        #ifdef DEBUG_
        if(frequency > upper_bound){
          std::cout << "  frequency = " << frequency << std::endl;
          std::cout << "   (0) upper_bound = " << upper_bound << std::endl;
        }
        #endif

        temp_bound = 1.0 - d_ell * (biased_freq - max_deviation);
        temp_bound = (temp_bound > 0.0) ? 1.0 - pow(temp_bound , 1.0 / d_ell) : 0.0;
        lower_bound = (lower_bound > temp_bound) ? lower_bound : temp_bound;
        #ifdef DEBUG_
        if(lower_bound > frequency){
          std::cout << "  frequency = " << frequency << std::endl;
          std::cout << "   (0) lower_bound = " << lower_bound << std::endl;
        }
        #endif


        #ifdef MULTIPLE_ELLS
        d_ell = floor(ells[0] * 2.0);
        buckets_temp = buckets / (num_part_pow_2 * 2.0);
        double _max_deviation_ = 0.5 / d_ell * ( sqrt( 2.0 * (floor(log2(d_ell) + 1.0) + log(1.0 / delta)) / buckets_temp) );
        biased_count2.clear();
        int bucket_index_converter = pow(2 , num_of_partitions);
        for (auto itr_ = biased_count.begin(); itr_ != biased_count.end(); ++itr_) {
            biased_count2.insert(((int)*itr_) / bucket_index_converter);
        }
        double _biased_freq_ = (double)biased_count2.size() / total_number;
        temp_bound = _biased_freq_ - _max_deviation_;
        lower_bound = (lower_bound > temp_bound) ? lower_bound : temp_bound;
        #ifdef DEBUG_
        if(lower_bound > frequency){
          std::cout << "  frequency = " << frequency << std::endl;
          std::cout << "   (1) lower_bound = " << lower_bound << std::endl;
        }
        #endif

        temp_bound = 1.0 - d_ell * (_biased_freq_ + _max_deviation_);
        temp_bound = (temp_bound > 0.0) ? 1.0 - pow(temp_bound , 1.0 / d_ell) : 1.0;
        upper_bound = (upper_bound < temp_bound) ? upper_bound : temp_bound;
        #ifdef DEBUG_
        if(frequency > upper_bound){
          std::cout << "  frequency = " << frequency << std::endl;
          std::cout << "   (1) upper_bound = " << upper_bound << std::endl;
        }
        #endif

        temp_bound = 1.0 - d_ell * (_biased_freq_ - _max_deviation_);
        temp_bound = (temp_bound > 0.0) ? 1.0 - pow(temp_bound , 1.0 / d_ell) : 0.0;
        lower_bound = (lower_bound > temp_bound) ? lower_bound : temp_bound;
        #ifdef DEBUG_
        if(lower_bound > frequency){
          std::cout << "  frequency = " << frequency << std::endl;
          std::cout << "  theta = " << theta << std::endl;
          std::cout << "  d_ell = " << d_ell << std::endl;
          std::cout << "  _biased_freq_ = " << _biased_freq_ << std::endl;
          std::cout << "  _max_deviation_ = " << _max_deviation_ << std::endl;
          std::cout << "   (2) lower_bound = " << lower_bound << std::endl;
        }
        #endif

        // lower bounds for higher partitions
        i = 1;
        while(i < deviations.size() && frequency > deviations[i]){

          double max_deviation_ = deviations[i];
          d_ell = ells[i];
          biased_count2.clear();
          int bucket_index_converter = pow(2 , num_of_partitions - i - 1);
          for (auto itr_ = biased_count.begin(); itr_ != biased_count.end(); ++itr_) {
              biased_count2.insert(((int)*itr_) / bucket_index_converter);
          }
          double biased_freq_ = (double)biased_count2.size() / total_number;

          temp_bound = biased_freq_ - max_deviation_;
          lower_bound = (lower_bound > temp_bound) ? lower_bound : temp_bound;
          #ifdef DEBUG_
          if(lower_bound > frequency){
            std::cout << "  frequency = " << frequency << std::endl;
            std::cout << "   (3) lower_bound = " << lower_bound << std::endl;
          }
          #endif

          temp_bound = 1.0 - d_ell * (biased_freq_ + max_deviation_);
          temp_bound = (temp_bound > 0.0) ? 1.0 - pow(temp_bound , 1.0 / d_ell) : 1.0;
          upper_bound = (upper_bound < temp_bound) ? upper_bound : temp_bound;
          #ifdef DEBUG_
          if(frequency > upper_bound){
            std::cout << "  frequency = " << frequency << std::endl;
            std::cout << "   (2) upper_bound = " << upper_bound << std::endl;
          }
          #endif

          temp_bound = 1.0 - d_ell * (biased_freq_ - max_deviation_);
          temp_bound = (temp_bound > 0.0) ? 1.0 - pow(temp_bound , 1.0 / d_ell) : 0.0;
          lower_bound = (lower_bound > temp_bound) ? lower_bound : temp_bound;
          #ifdef DEBUG_
          if(lower_bound > frequency){
            std::cout << "  frequency = " << frequency << std::endl;
            std::cout << "   (4) lower_bound = " << lower_bound << std::endl;
          }
          #endif

          i++;
        }
        #endif


        out << it.val() << ";" << it.key() << ";" << frequency << ";" << biased_freq << ";" << lower_bound << ";" << upper_bound << ";" << "\n";
        ++results;
      }
    }
    /*for(i = 0; i < ell_counts.size(); i++){
      std::cout << "ell_counts[" << i << "] = " << ell_counts[i] << std::endl;
      std::cout << "  buckets_indexes[" << i << "] = " << buckets_indexes[i] << std::endl;
    }*/
    std::cout << " distinct_elements = " << distinct_elements << std::endl;
    std::cout << " results = " << results << std::endl;
  }
  else{
    if(args.column_flag) {
      char spacer = args.tab_flag ? '\t' : ' ';
      while(it.next()) {
        if(it.val() < lower_count || it.val() > upper_count)
          continue;
        out << it.key() << spacer << it.val() << "\n";
      }
    } else {
      long distinct_elements = 0;
      long results = 0;
      //double total_number = (double)args.totalkmers_arg;
      //double frequency = 0.0;
      while(it.next()) {
        ++distinct_elements;
        if(it.val() < lower_count || it.val() > upper_count)
          continue;
        //out << ">" << it.val() << "\n" << it.key() << "\n";
        //frequency = (double)it.val() / total_number;
        out << it.val() << ";" << it.key() << ";" /*<< frequency << ";"*/ << "\n";
        ++results;
      }
      std::cout << " distinct_elements = " << distinct_elements << std::endl;
      std::cout << " results = " << results << std::endl;
    }
  }
}

int dump_main(int argc, char *argv[])
{

  auto start_time = system_clock::now();
  std::cout << " dump_main started " << std::endl;

  args.parse(argc, argv);
  std::ios::sync_with_stdio(false); // No sync with stdio -> faster

  std::cout << " parse ok " << std::endl;

  ofstream_default out(args.output_given ? args.output_arg : 0, std::cout);
  if(!out.good())
    err::die(err::msg() << "Error opening output file '" << args.output_arg << "'");

  std::ifstream is(args.db_arg);
  if(!is.good())
    err::die(err::msg() << "Failed to open input file '" << args.db_arg << "'");

  if(args.dist_given){
    std::ifstream is2(args.dist_arg);
    if(!is2.good())
      err::die(err::msg() << "Failed to open input file '" << args.dist_arg << "'");
    is2.close();
    is.close();
    std::cout << "Distance mode selected " << "\n";
    std::cout << "First dataset " << args.db_arg << "\n";
    std::cout << "Second dataset " << args.dist_arg << std::endl;
    std::string db1(args.db_arg);
    std::string db2(args.dist_arg);
    dist(db1 , db2 , out , args.distratio1_arg , args.distratio2_arg);
    auto after_dist_time = system_clock::now();
    std::cout << "Running time for dist  " << as_seconds(after_dist_time - start_time) << "\n";
    return 0;
  }

  jellyfish::file_header header;
  header.read(is);
  jellyfish::mer_dna::k(header.key_len() / 2);

  if(!args.lower_count_given)
    args.lower_count_arg = 0;
  if(!args.upper_count_given)
    args.upper_count_arg = std::numeric_limits<uint64_t>::max();


  if(!header.format().compare(binary_dumper::format)) {
    binary_reader reader(is, &header);
    dump(reader, out, args.lower_count_arg, args.upper_count_arg);
  } else if(!header.format().compare(text_dumper::format)) {
    text_reader reader(is, &header);
    dump(reader, out, args.lower_count_arg, args.upper_count_arg);
  } else {
    err::die(err::msg() << "Unknown format '" << header.format() << "'");
  }

  out.close();

  auto after_dump_time = system_clock::now();

  std::cout << "Running time for dumping  " << as_seconds(after_dump_time - start_time) << "\n";

  return 0;
}
