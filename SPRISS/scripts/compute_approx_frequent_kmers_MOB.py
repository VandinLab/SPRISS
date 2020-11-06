import math
import os
import time
import subprocess
import sys
import numpy as np
import random

run = sys.argv[1]

k = 31
datasets = ["B73","Mo17"]
datasets_size = [99209208120,97965214600] #k=31
tot_reads = [450950946, 445296430]
avg_read_length = [250.0,250.0]
max_read_length = [250,250]
thetas = [2.0]
thetas[:] = [x / float(10**7) for x in thetas]

delta = 0.1

of = open("approx_counts_for_discriminative_MOB_time_run"+run+".txt",'w')
for i,dataset in enumerate(datasets):
	print(dataset)
	of.write(dataset + " \n")
	#start = time.time()
	dataset_path = "MOBdatasets/" + dataset + ".fastq"
	original_dataset = open(dataset_path,'r')
	#content = original_dataset.readlines()
	original_dataset.close()
	#end = time.time()
	#loading_time = end - start
	#print("Loading dataset time: " + str(loading_time))
	#of.write("Loading dataset time: " + str(loading_time) + " \n")
	for j,theta in enumerate(thetas):
		print(str(theta))
		of.write(str(theta) + " \n")
		start_sample = time.time()
		output_file = "MOBdatasets/" + dataset + "_kmc_" + str(k) + "-mers_" + str(j) + "_db"
		epsilon = theta - 2.0/datasets_size[i]
		l = math.floor((0.04/theta)/(avg_read_length[i]-k+1))
		m = math.ceil((2/((epsilon*l*(avg_read_length[i]-k+1))**2)) * ( math.floor(math.log2(min(2*l*(max_read_length[i]-k+1) ,4**31))) + math.log(2.0/delta)  ) )
		ml = int(m*l)
		sample_size = float(ml)/float(tot_reads[i])
		print("Sample_size= " + str(sample_size))
		of.write("Sample_size= " + str(sample_size) + " \n")
		sample_path =  "MOBdatasets/" + dataset + "_kmc_sample.fastq"
		sample = open(sample_path, 'w')
		#random_positions = np.random.randint(0, high=tot_reads[i], size=ml)
		#sample_size = 0
		#for pos in random_positions:
		#	sample_size = sample_size + (len(content[pos*4+1])-1-k+1)
		#	sample.write(content[pos*4])
		#	sample.write(content[pos*4+1])
		#	sample.write(content[pos*4+2])
		#	sample.write(content[pos*4+3])
		dataset_path = "MOBdatasets/" + dataset + ".fastq"
		original_dataset = open(dataset_path,'r')
		line = original_dataset.readline()
		while(line):
			flip = random.random()
			if(flip < sample_size):
				sample.write(line)
				line = original_dataset.readline()
				sample.write(line) #read
				line = original_dataset.readline()
				sample.write(line)
				line = original_dataset.readline()
				sample.write(line)
			else:
				line = original_dataset.readline() #read
				line = original_dataset.readline()
				line = original_dataset.readline()
			line = original_dataset.readline()
		original_dataset.close()
		sample.close()
		end_sample = time.time()
		print("Time_sample_creation= " + str(end_sample-start_sample))
		of.write("Time_sample_creation= " + str(end_sample-start_sample) + " \n")
		start_mining = time.time()
		cmd = "./../bin/kmc -k"+str(k)+" -cs"+str(datasets_size[i])+" -m200 -ci1 -t32 " + sample_path + " " + output_file + " work_dir/"
		print(cmd)
		os.system(cmd)
		end_mining = time.time()
		counting_time = end_mining - start_mining
		start_dump1 = time.time()
		denominator = m*l*(avg_read_length[i]-k+1)
		kmer_counts_file =  "MOBdatasets/" + dataset + "_kmc_" + str(k) + "-mers_" + str(j) + ".txt"
		cmd = "./../bin/kmc_dump -ci1 -theta" + str(theta) + " -epsilon" +str(epsilon) + " -n_bags" + str(int(m)) + " -denominator" +str(denominator) + " " + output_file + " " + kmer_counts_file
		print(cmd)
		os.system(cmd)
		end_dump1 = time.time()
		dump1_time = end_dump1 - start_dump1		
		print("Counting_time_discr= " + str(counting_time+dump1_time))
		of.write("Counting_time_discr= " + str(counting_time+dump1_time) + " \n")
	#content.clear()
of.close()

