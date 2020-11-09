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
parser.add_argument("-dt","--dbtot", type=float ,help="dataset size (>0). Computed if not given")
parser.add_argument("-t","--theta", type=float ,help="frequency threshold (in (0,1))")
parser.add_argument("-l","--lambd", type=float ,help="desired fraction between sample size and dataset size (in (0,2))")
parser.add_argument("-e","--epsilon", type=float ,help="approximation accuracy parameter (in (0,1), def. theta + 2/dbtot)")
parser.add_argument("-ell", type=float ,help="size of bags to sample (>0, def. 1/theta - 1)")
parser.add_argument("-d","--delta", type=float ,help="approximation confidence parameter (in (0,1), def. 0.1)",default=0.1)
parser.add_argument("-v","--verbose", help="increase output verbosity (def. false)")
args = parser.parse_args()


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
        counter = counter + float(get_result(str(i)+" sampling pass: finished and inserted ",path,0))
    print "sampling passes: finished and inserted "+str(counter)
    return counter

def get_dbtot(numthreads, path):
    counter = 0.0
    for i in range(numthreads):
        counter = counter + float(get_result(str(i)+" dataset size: ",path,0))
    return counter


def get_total_positions(dataset):
    print "computing size of "+str(dataset)+"..."
    jellyfish_path = "../bin/jellyfish"
    work_dir_path = "work_dir/"
    if not os.path.exists(work_dir_path):
        os.system("mkdir "+str(work_dir_path))
    temp_file_path = work_dir_path+"out_temp.txt"
    if not args.output:
        path_counts = work_dir_path+"counts_SAKEIMA_"+str(args.k)+".txt"
    else:
        path_counts = args.output
    path_binary = work_dir_path+"SAKEIMA_"+str(args.k)+".mf"
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
if not args.theta:
    if not args.lambd:
        print "Argument theta or lambda is needed"
        parser.print_help(sys.stderr)
        exit()
else:
    if args.theta <= 0 or args.theta >= 1:
        print "Argument theta needs to be in (0,1)"
        parser.print_help(sys.stderr)
        exit()
if args.epsilon:
    if args.theta <= 0 or args.theta >= 1:
        print "Argument epsilon needs to be in (0,1)"
        parser.print_help(sys.stderr)
        exit()
if args.delta <= 0 or args.delta >= 1:
    print "Argument delta needs to be in (0,1)"
    parser.print_help(sys.stderr)
    exit()
if args.lambd:
    if args.lambd <= 0 or args.lambd >= 2:
        print "Argument lambd needs to be in (0,2)"
        parser.print_help(sys.stderr)
        exit()
if args.thr <= 0:
    print "Argument thr needs to be > 0"
    parser.print_help(sys.stderr)
    exit()
if args.epsilon:
    if args.ell <= 0:
        print "Argument ell needs to be > 0"
        parser.print_help(sys.stderr)
        exit()
if args.epsilon:
    if args.dbtot <= 0:
        print "Argument dbtot needs to be > 0"
        parser.print_help(sys.stderr)
        exit()




if not args.dbtot:
    args.dbtot = get_total_positions(args.db)

def bound(epsilon , ell):
    return 2.0 / (ell * epsilon)**2 * (math.floor(math.log(2.0 * ell , 2.0)) + math.log(2.0/args.delta) )
def bound_inv(m , ell):
    return 1.0/ell * math.sqrt(2.0 / m * (math.floor(math.log(2.0*ell,2.0)) + math.log(2.0/args.delta)))
def default_value_epsilon(theta , db_size):
    return theta - 2.0 / db_size
def default_value_theta(epsilon , db_size):
    return epsilon + 2.0 / db_size
def default_value_ell(theta):
    return math.ceil(1.0 / theta) - 1.0
def find_lowest_theta(sample_size):
    min_supp = 1.0
    theta = min_supp / args.dbtot;
    target_epsilon = default_value_epsilon(theta , args.dbtot)
    ell = default_value_ell(theta)
    m = max(1.0 , math.floor(sample_size / ell))
    current_epsilon = bound_inv(m , ell)
    while current_epsilon > target_epsilon:
        min_supp = min_supp + 1.0
        theta = min_supp / args.dbtot;
        target_epsilon = default_value_epsilon(theta , args.dbtot)
        ell = default_value_ell(theta)
        m = max(1.0 , math.floor(sample_size / ell))
        current_epsilon = bound_inv(m , ell)
    return theta
def find_lowest_ell(epsilon , sample_size):
    ell = 100.0
    m = math.floor(sample_size / ell)
    eps = bound_inv(m , ell)
    while eps > epsilon:
        ell = math.ceil(ell * 1.1)
        m = math.floor(sample_size / ell)
        eps = bound_inv(m , ell)
    while eps <= epsilon:
        ell = ell - 1.0
        m = math.floor(sample_size / ell)
        eps = bound_inv(m , ell)
    ell = ell + 1.0
    if ell <= 0.0 or (ell * epsilon) >= 1.0:
        return -1
    return ell

if not args.lambd:
    if not args.ell:
        args.ell = default_value_ell(args.theta)
    if not args.epsilon:
        args.epsilon = default_value_epsilon(args.theta , args.dbtot)
    m = math.ceil(bound(args.epsilon , args.ell))
    sample_size = m * args.ell
    args.lambd = sample_size / args.dbtot
else:
    sample_size = math.ceil(args.lambd * float(args.dbtot))
    if not args.ell:
        if not args.epsilon:
            if not args.theta:
                args.theta = find_lowest_theta(sample_size)
                args.epsilon = default_value_epsilon(args.theta , args.dbtot)
                args.ell = default_value_ell(args.theta)
            else:
                args.epsilon = default_value_epsilon(args.theta , args.dbtot)
                args.ell = find_lowest_ell(args.epsilon , sample_size)
                if args.ell < 0:
                    print "Impossible to compute the approximation. use a lower value for theta or a larger sample size."
                    exit()
        else:
            args.ell = find_lowest_ell(args.epsilon , sample_size)
            if args.ell < 0:
                print "Impossible to compute the approximation. use a lower value for epsilon or a larger sample size."
                exit()
            if not args.theta:
                args.theta = default_value_theta(args.epsilon , args.dbtot)
            else:
                if args.epsilon >= args.theta:
                    print "Impossible to compute the approximation. set theta < "+str(args.epsilon)
                    exit()

    else:
        m = math.floor(sample_size / args.ell)
        args.epsilon = bound_inv(m , args.ell)
        if not args.theta:
            args.theta = default_value_theta(args.epsilon , args.dbtot)
        else:
            if args.epsilon >= args.theta:
                print "Impossible to compute the approximation. set theta < "+str(args.epsilon)
                exit()

print "lambda = "+str(args.lambd)
print "theta = "+str(args.theta)
print "epsilon = "+str(args.epsilon)
print "ell = "+str(args.ell)


def run_sakeima():
    global sample_size
    jellyfish_path = "../bin/jellyfish"
    work_dir_path = "work_dir/"
    if not os.path.exists(work_dir_path):
        os.system("mkdir "+str(work_dir_path))
    temp_file_path = work_dir_path+"out_temp.txt"
    if not args.output:
        path_counts = work_dir_path+"counts_SAKEIMA_"+str(args.k)+".txt"
    else:
        path_counts = args.output
    path_binary = work_dir_path+"SAKEIMA_"+str(args.k)+".mf"
    path_reads = args.db
    param = args.lambd
    k = args.k
    thr = args.thr
    cmd = jellyfish_path+" count -m "+str(args.k)+" -s 1M -t "+str(thr)+" --lambda "+str(param)+" -o "+str(path_binary)+" -C "+str(path_reads)+" > "+str(temp_file_path)
    print "counting k-mers of "+str(path_reads)+"..."
    if args.verbose:
        print cmd
    os.system(cmd)
    time.sleep(3)
    results_patterns = ("Total running time  " , "Writing  " , "Peak Memory (MB):  ")
    for pattern in results_patterns:
        get_result(pattern , temp_file_path)

    sample_size_old = sample_size
    m = round(sample_size / args.ell)
    sample_size = get_tot(thr , temp_file_path)
    m_old = m
    m = round(sample_size / args.ell)

    if args.verbose:
        print "ratio = "+str(sample_size / args.dbtot)
        print "ratio 2 = "+str(sample_size / sample_size_old)
        print "m_old = "+str(m_old)
        print "m_new = "+str(m)

    ell = int(math.floor(sample_size / m))
    sample_size = int(sample_size)
    theta = args.theta
    cmd = jellyfish_path+" dump -o "+str(path_counts)+" --bagsell "+str(ell)+" --totalkmers "+str(sample_size)+" --theta "+str(theta)+" "+str(path_binary)+" > "+str(temp_file_path)
    print "writing k-mers of "+str(path_reads)+" to "+str(path_counts)+"..."
    if args.verbose:
        print cmd
    os.system(cmd)
    time.sleep(3)
    patterns = list()
    results_patterns = ("Running time for dumping  "," results = ")
    for pattern in results_patterns:
        get_result(pattern , temp_file_path)


run_sakeima()
