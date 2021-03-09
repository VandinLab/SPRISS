import math
import os
import time
import subprocess
import sys
import numpy as np

os.system("g++ -o create_sample create_sample.cpp")

run = sys.argv[1]

datasets = ['SRS024075','SRS024388','SRS011239','SRS075404','SRS043663','SRS062761']
tot_reads = [138050470.0,119684324.0,123832980.0,122090110.0,130805974.0,118081524.0]
datasets_size = [8819242497,7924744349,8135441782,7754975225,9156418180,8265706595] #k31
avg_read_length = [93.88419019380541,96.21372036842386,95.69689105596845,93.51845561984399,99.99999990672346,99.9999992404889]
max_read_length = [95,101,101,101,100,100]

k = 31
delta = 0.1
thetas = [2.5,5.0,7.5,10.0]
thetas[:] = [x / float(10**8) for x in thetas]
of = open("approx_mining_time_run"+run+".txt",'w')

for i,dataset in enumerate(datasets):
	print(dataset)
	of.write(dataset + " \n")
	#start = time.time()
	dataset_path = dataset + "/" + dataset + ".fastq"
	#old sample creation
	#original_dataset = open(dataset_path,'r')
	#content = original_dataset.readlines()
	#original_dataset.close()
	#end = time.time()
	#loading_time = end - start
	#print("Loading dataset time: " + str(loading_time))
	#of.write("Loading dataset time: " + str(loading_time) + " \n")
	for j,theta in enumerate(thetas):
		print(str(theta))
		of.write(str(theta) + " \n")
		start_sample = time.time()
		output_file = dataset + "/" + dataset + "_kmc_" + str(k) + "-mers_" + str(j) + "_db"
		epsilon = theta - 2.0/datasets_size[i]
		l = math.floor((0.9/theta)/(avg_read_length[i]-k+1))
		m = math.ceil((2/((epsilon*l*(avg_read_length[i]-k+1))**2)) * ( math.floor(math.log2(min(2*l*(max_read_length[i]-k+1) ,4**31))) + math.log(2.0/delta)  ) )
		ml = int(m*l)
		sample_size = float(ml)/float(tot_reads[i])
		print("Sample_size= " + str(sample_size))
		of.write("Sample_size= " + str(sample_size) + " \n")
		sample_path =  dataset + "/" + dataset + "_kmc_sample.fastq"
		cmd = "./create_sample " + dataset_path + " " + sample_path + " " + str(int(tot_reads[i])) + " " + str(ml)
		print(cmd)
		os.system(cmd)
		#old sample creation
		#sample = open(sample_path, 'w')
		#random_positions = np.random.randint(0, high=tot_reads[i], size=ml)
		#sample_size = 0
		#for pos in random_positions:
		#	sample_size = sample_size + (len(content[pos*4+1])-1-k+1)
		#	sample.write(content[pos*4])
		#	sample.write(content[pos*4+1])
		#	sample.write(content[pos*4+2])
		#	sample.write(content[pos*4+3])
		#sample.close()
		end_sample = time.time()
		#cmd = "wc -l " + sample_path
		#print(cmd)
		#os.system(cmd)
		print("Time_sample_creation= " + str(end_sample-start_sample))
		of.write("Time_sample_creation= " + str(end_sample-start_sample) + " \n")
		start_mining = time.time()
		cmd = "./../bin/kmc -k"+str(k)+" -cs"+str(datasets_size[i])+" -m200 -ci1 -t1 " + sample_path + " " + output_file + " work_dir/"
		print(cmd)
		os.system(cmd)
		end_mining = time.time()
		counting_time = end_mining - start_mining
		start_dump1 = time.time()
		denominator = m*l*(avg_read_length[i]-k+1)
		kmer_counts_file =  dataset + "/" + dataset + "_kmc_" + str(k) + "-mers_" + str(j) + ".txt"
		cmd = "./../bin/kmc_dump -ci1 -theta" + str(theta) + " -epsilon" +str(epsilon) + " -n_bags" + str(int(m)) + " -denominator" +str(denominator) + " " + output_file + " " + kmer_counts_file
		print(cmd)
		os.system(cmd)
		end_dump1 = time.time()
		dump1_time = end_dump1 - start_dump1
		#start_dump2 = time.time()
		#kmer_counts_file =  dataset + "/" + dataset + "_kmc_" + str(k) + "-mers_" + str(j) + "_all.txt"
		#cmd = "./../bin/kmc_dump -ci1 -theta" + str(theta) + " -epsilon" +str(epsilon) + " -n_bags" + str(int(m)) + " -denominator" +str(denominator) + " -all" + str(1) + " " +  output_file + " " + kmer_counts_file
		#print(cmd)
		#os.system(cmd)
		#end_dump2 = time.time()
		#dump2_time = end_dump2 - start_dump2
		#print("Counting_time= " + str(counting_time+dump1_time))
		#of.write("Counting_time= " + str(counting_time+dump1_time) + " \n")
		print("Total_time= " + str(counting_time+dump1_time+(end_sample-start_sample)))
		of.write("Total_time= " + str(counting_time+dump1_time+(end_sample-start_sample)) + " \n")
	#content.clear()
of.close()


