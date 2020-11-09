import math
import os
import numpy as np
import sys
import time
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-k", type=int ,help="length of k-mers (>0)")
parser.add_argument("-db", help="path to input file (dataset of reads)")
parser.add_argument("-o","--output", help="path to output file (counts of frequent k-mers)")
parser.add_argument("-thr", type=int ,help="Number of threads to use for counting (>0, def. 1)",default=1)
parser.add_argument("-t","--theta", type=float ,help="frequency threshold (in (0,1))",default=0.)
parser.add_argument("-v","--verbose", help="increase output verbosity (def. false)")
parser.add_argument("-rid","--runid", help="unique id for experiments",default=0)
parser.add_argument("-keep","--keepf", help="keep files after experiment",default=0)
parser.add_argument("-L","--lowercount", help="don't output kmers with count < lowercount",default=0)
args = parser.parse_args()

output_path = args.output + ".csv"


def get_result(pattern , path ,  verbose=1):
    fin = open(path,'r')
    for line in fin:
        if pattern in line:
            line = line.replace('\n','')
            if verbose == 1:
                print line
            return line[len(pattern):]
    fin.close()

def get_tot(numthreads, path):
    counter = 0.0
    for i in range(numthreads):
        counter = counter + float(get_result(str(i)+" first pass: finished and inserted ",path,0))
    print "first pass: finished and inserted "+str(counter)
    return counter

def get_dbtot(numthreads, path):
    counter = 0.0
    for i in range(numthreads):
        counter = counter + float(get_result(str(i)+" dataset size: ",path,0))
    return counter


def get_total_positions(dataset):
    print "computing size of "+str(dataset)+"..."
    jellyfish_path = "../bin/jellyfish"
    work_dir_path = "work_dir_GOS/"
    if not os.path.exists(work_dir_path):
        os.system("mkdir "+str(work_dir_path))
    temp_file_path = work_dir_path+"out_temp_"+str(args.runid)+".txt"
    if not args.output:
        path_counts = work_dir_path+"counts_jellyfish_"+str(args.k)+"_"+str(args.runid)+".txt"
    else:
        path_counts = args.output + ".txt"
    path_binary = work_dir_path+"jellyfish_"+str(args.k)+"_"+str(args.runid)+".mf"
    path_reads = args.db
    k = args.k
    thr = args.thr
    cmd = jellyfish_path+" count -m "+str(args.k)+" -s 1M -t "+str(thr)+" --dbsize -o "+str(path_binary)+" "+str(path_reads)+" > "+str(temp_file_path)
    if args.verbose:
        print cmd
    os.system(cmd)
    time.sleep(1)
    numer_of_positions = float(get_dbtot(thr , temp_file_path))
    print "size of "+str(dataset)+" is "+str(numer_of_positions)
    return numer_of_positions

if not args.k:
    print "Argument k is needed"
    parser.print_help(sys.stderr)
    exit()
else:
    if args.k <= 0:
        print "Argument k needs to be >= 0"
        parser.print_help(sys.stderr)
        exit()
if not args.db:
    print "path to dataset is needed!"
    parser.print_help(sys.stderr)
    exit()
if not os.path.isfile(args.db):
    print "path to dataset not correct!"
    parser.print_help(sys.stderr)
    exit()


#print "theta = "+str(args.theta)

def run_jellyfish():
    global sample_size
    jellyfish_path = "../bin/jellyfish"
    work_dir_path = "work_dir_GOS/"
    if not os.path.exists(work_dir_path):
        os.system("mkdir "+str(work_dir_path))
    temp_file_path = work_dir_path+"out_temp_"+str(args.runid)+".txt"
    if not args.output:
        path_counts = work_dir_path+"counts_jellyfish_"+str(args.k)+"_"+str(args.runid)+".txt"
    else:
        path_counts = args.output + ".txt"
    path_binary = work_dir_path+"jellyfish_"+str(args.k)+"_"+str(args.runid)+".mf"
    path_reads = args.db
    k = args.k
    thr = args.thr
    lowercount = args.lowercount
    cmd = jellyfish_path+" count -m "+str(args.k)+" -s 1M -t "+str(thr)+" -o "+str(path_binary)+" -C "+str(path_reads) + " > "+str(temp_file_path)
    print "counting k-mers of "+str(path_reads)+"..."
    if args.verbose:
        print cmd
    os.system(cmd)
    time.sleep(3)
    results_patterns = ("Counting(cpu) ","Total running time(cpu)  ","Writing(cpu)  ","Counting ","Total running time  " , "Writing  " , "Peak Memory (MB):  ")
    results_values = list()
    for pattern in results_patterns:
        results_values.append(get_result(pattern , temp_file_path))

    cmd = jellyfish_path+" dump -c -L "+str(lowercount)+" -o "+str(path_counts)+" "+str(path_binary)+" > "+str(temp_file_path)
    #print "writing k-mers of "+str(path_reads)+" to "+str(path_counts)+"..."
    if args.verbose:
        print cmd
    os.system(cmd)
    time.sleep(3)
    patterns = list()
    results_patterns = ("Running time for dumping  "," results = ")
    for pattern in results_patterns:
        results_values.append(get_result(pattern , temp_file_path))

    inf_to_print = list()
    inf_to_print.append(args.runid)
    inf_to_print.append(args.db)
    inf_to_print.append(args.k)
    inf_to_print.append(args.thr)
    for res in results_values:
        inf_to_print.append(res)
    string_to_print = ""
    for info in inf_to_print:
        string_to_print = string_to_print + str(info) + ";"
    string_to_print = string_to_print + "\n"
    fout = open(output_path , 'a')
    fout.write(string_to_print)
    fout.close()
    if args.keepf == 0:
        os.system("rm "+str(path_counts))
    os.system("rm "+str(path_binary))
    os.system("rm " + args.output + ".csv")


run_jellyfish()
