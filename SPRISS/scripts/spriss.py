import math
import os
import time
import subprocess
import sys
import numpy as np

os.system("g++ -o create_sample create_sample.cpp")

dataset_ext = sys.argv[1]
dataset = dataset_ext.split(".")[0]
k = int(sys.argv[2])
delta = float(sys.argv[3])
theta = float(sys.argv[4])
epsilon = float(sys.argv[5])
l = int(sys.argv[6])
of = open("running_times.txt",'w')

#statistics of the dataset
print("Computing statistics of the dataset ... ")
df = open(dataset_ext,'r')
line = df.readline() #1
datasets_size = 0
tot_reads = 0.0
avg_read_length = 0.0
max_read_length = 0
while(line):
	line = df.readline() #2 (read)
	tot_reads = tot_reads + 1
	avg_read_length += (len(line)-1)
	max_read_length = max(max_read_length,len(line)-1)
	datasets_size = datasets_size + (len(line)-1 -k +1)
	line = df.readline() #3
	line = df.readline() #4
	line = df.readline() #1
avg_read_length = float(avg_read_length)/float(tot_reads)
print(str(datasets_size) + " " + str(k)+"-mers")
print(str(tot_reads) + " reads")
print(str(avg_read_length) + " avg_read_length")
print(str(max_read_length) + " max_read_length")
df.close()

if(epsilon < 0):
	epsilon = theta - 2.0/datasets_size
if(l < 0):
	l = math.floor((0.9/theta)/(avg_read_length-k+1))
print(dataset_ext + " k=" + str(k) + " delta=" + str(delta) + " theta=" + str(theta) + " epsilon=" + str(epsilon) + " l=" + str(l))

#sampling and frequent k-mers estimates
print("Computing sampling and frequent k-mers estimates ... ")
print(dataset)
of.write(dataset + " \n")
print(str(theta))
of.write(str(theta) + " \n")

#sampling
start_sample = time.time()
output_file = dataset + "_kmc_" + str(k) + "-mers_db"
l = math.floor((0.9/theta)/(avg_read_length-k+1))
m = math.ceil((2/((epsilon*l*(avg_read_length-k+1))**2)) * ( math.floor(math.log2(min(2*l*(max_read_length-k+1) ,4**31))) + math.log(2.0/delta)  ) )
ml = int(m*l)
sample_rate = float(ml)/float(tot_reads)
print("sample_rate= " + str(sample_rate))
of.write("sample_rate= " + str(sample_rate) + " \n")
if(sample_rate >= 1.0):
	sys.exit("Sample size greater than the dataset size. The dataset could be too small (so the sampling strategy is not useful), or try to change values of k end/or theta and/or epsilon and/or l")

sample_path =  dataset + "_sample.fastq"
cmd = "./create_sample " + dataset_ext + " " + sample_path + " " + str(int(tot_reads)) + " " + str(ml)
print(cmd)
os.system(cmd)
end_sample = time.time()
print("Time_sample_creation= " + str(end_sample-start_sample))
of.write("Time_sample_creation= " + str(end_sample-start_sample) + " \n")

#frequent k-mers estimation
start_mining = time.time()
cmd = "./../bin/kmc -k"+str(k)+" -cs"+str(datasets_size)+" -m200 -ci1 -t1 " + sample_path + " " + output_file + " work_dir/"
print(cmd)
os.system(cmd)
end_mining = time.time()
counting_time = end_mining - start_mining
start_dump1 = time.time()
denominator = m*l*(avg_read_length-k+1)
kmer_counts_file = dataset + "_frequent_" + str(k) + "-mers_estimates.txt"
cmd = "./../bin/kmc_dump -ci1 -theta" + str(theta) + " -epsilon" +str(epsilon) + " -n_bags" + str(int(m)) + " -denominator" +str(denominator) + " " + output_file + " " + kmer_counts_file
print(cmd)
os.system(cmd)
end_dump1 = time.time()
dump1_time = end_dump1 - start_dump1

print("Total_time= " + str(counting_time+dump1_time+(end_sample-start_sample)))
of.write("Total_time= " + str(counting_time+dump1_time+(end_sample-start_sample)) + " \n")
of.close()

