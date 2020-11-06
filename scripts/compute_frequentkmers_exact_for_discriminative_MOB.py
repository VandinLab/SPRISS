import sys
import os
import time
import numpy as np
import math

k = 31
datasets = ["B73","Mo17"]
datasets_size = [99209208120,97965214600] #k=31
thetas = [2.0]
thetas[:] = [x / float(10**7) for x in thetas]
results = open("counting_time_Mo17_B73.txt",'w')

print("Compute frequent k-mers counts ...")
for i,dataset in enumerate(datasets):
	print(dataset)
	results.write(dataset + " \n")
	start_kmc = time.time()
	input_db = "MOBdatasets/" + dataset + ".fastq"
	output_file = "MOBdatasets/" + dataset + "_exact_kmc_freqkmers_db"
	cmd = "./../bin/kmc -k"+str(k)+" -cs"+str(datasets_size[i])+" -m200 -ci2 -t32 " + input_db + " " + output_file + " work_dir_exact_MOB/"
	print(cmd)
	os.system(cmd)
	end_kmc = time.time()
	counting_time = end_kmc - start_kmc
	for theta in thetas:
		print(str(theta))
		results.write(str(theta) + " \n")
		start_kmcdump = time.time()
		lowercount = int(math.ceil(theta*datasets_size[i]))
		kmer_counts_file = "MOBdatasets/" + dataset + "_exact_kmc_freqkmers_"+ str(theta*(10**8)) + ".txt"
		cmd = "./../bin/kmc_dump -ci" + str(lowercount) + " " + output_file + " " + kmer_counts_file
		print(cmd)
		os.system(cmd)
		end_kmcdump = time.time()
		dumping_time1 = end_kmcdump - start_kmcdump
		#print("Counting_time= " + str(counting_time+dumping_time))
		#results.write("Counting_time= " + str(counting_time+dumping_time) + " \n")
		start_kmcdump = time.time()
		lowercount = int(math.ceil((theta/2.0)*datasets_size[i]))
		kmer_counts_file_discr = "MOBdatasets/" + dataset + "_exact_kmc_freqkmers_"+ str(theta*(10**8)) + "_div2.txt"
		cmd = "./../bin/kmc_dump -ci" + str(lowercount) + " " + output_file + " " + kmer_counts_file_discr
		print(cmd)
		os.system(cmd)
		end_kmcdump = time.time()
		dumping_time2 = end_kmcdump - start_kmcdump
		print("Counting_time_discr= " + str(2*counting_time+dumping_time1+dumping_time2))
		results.write("Counting_time_discr= " + str(2*counting_time+dumping_time1+dumping_time2) + " \n")
results.close()

