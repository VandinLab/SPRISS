import sys
import os
import time
import numpy as np
import math

datasets = ['SRS024075','SRS024388','SRS011239','SRS075404','SRS043663','SRS062761']
datasets_size = [8819242497,7924744349,8135441782,7754975225,9156418180,8265706595] #k=31
thetas = [2.5,5.0,7.5,10.0]
thetas[:] = [x / float(10**8) for x in thetas]
k = 31
results = open("time_frequentkmers_kmc.txt",'w')
results_discriminative = open("time_countsfor_discriminativekmers_kmc.txt",'w')

print("Compute all k-mers counts ...")
for i,dataset in enumerate(datasets):
	print(dataset)
	input_db =  dataset + "/" + dataset + ".fastq"
	output_file = dataset +"/exact_kmc_all_kmers_db"
	cmd = "./../bin/kmc -v -k"+str(k)+" -cs"+str(datasets_size[i])+" -m200 -ci1 -t16 " + input_db + " " + output_file + " work_dir_exact/"
	print(cmd)
	os.system(cmd)
	kmer_counts_file = dataset +"/exact_kmc_all_kmers.txt"
	cmd = "./../bin/kmc_dump -ci1 " + output_file + " " + kmer_counts_file
	print(cmd)
	os.system(cmd)

print("Compute frequent k-mers counts ...")
for i,dataset in enumerate(datasets):
	print(dataset)
	results.write(dataset + " \n")
	results_discriminative.write(dataset + " \n")
	for theta in thetas:
		print(str(theta))
		results.write(str(theta) + " \n")
		results_discriminative.write(str(theta) + " \n")
		start_kmc = time.time()
		input_db = dataset + "/" + dataset + ".fastq"
		output_file = dataset +"/exact_kmc_freqkmers_"+ str(theta*(10**8)) + "_db"
		cmd = "./../bin/kmc -k"+str(k)+" -cs"+str(datasets_size[i])+" -m200 -ci1 -t1 " + input_db + " " + output_file + " work_dir_exact/"
		print(cmd)
		os.system(cmd)
		end_kmc = time.time()
		counting_time = end_kmc - start_kmc
		start_kmcdump = time.time()
		lowercount = int(math.ceil(theta*datasets_size[i]))
		kmer_counts_file = dataset +"/exact_kmc_freqkmers_"+ str(theta*(10**8)) + ".txt"
		cmd = "./../bin/kmc_dump -ci" + str(lowercount) + " " + output_file + " " + kmer_counts_file
		print(cmd)
		os.system(cmd)
		end_kmcdump = time.time()
		dumping_time = end_kmcdump - start_kmcdump
		print("Counting_time= " + str(counting_time+dumping_time))
		results.write("Counting_time= " + str(counting_time+dumping_time) + " \n")
		
		start_kmcdump_discr = time.time()
		lowercount = int(math.ceil((theta/2.0)*datasets_size[i]))
		kmer_counts_file_discr = dataset +"/exact_kmc_freqkmers_"+ str(theta*(10**8)) + "_div2.txt"
		cmd = "./../bin/kmc_dump -ci" + str(lowercount) + " " + output_file + " " + kmer_counts_file_discr
		print(cmd)
		os.system(cmd)
		end_kmcdump_discr = time.time()
		dumping_time_discr = end_kmcdump_discr - start_kmcdump_discr
		print("Counting_time_discr= " + str(2*counting_time+dumping_time+dumping_time_discr))
		results_discriminative.write("Counting_time_discr= " + str(2*counting_time+dumping_time+dumping_time_discr) + " \n")
		
results.close()
results_discriminative.close()

