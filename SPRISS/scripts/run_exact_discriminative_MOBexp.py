import os
import time
import sys
import numpy as np
k = 31

datasets = ["B73","Mo17"]
datasets_size = [99209208120,97965214600] #k=31

thetas = [2.0]
thetas[:] = [x / float(10**7) for x in thetas]
output_time = open("exact_time_to_compute_discriminativekmers_MOB.txt",'w')

for t,theta in enumerate(thetas):
	print(str(theta))
	output_time.write(str(theta) + " \n")
	start = time.time()
	print("Sorting candidates discriminative k-mers and related files ... ")
	for dataset in datasets:
		output_file = "MOBdatasets/" + dataset + "_exact_kmc_freqkmers_"+ str(theta*(10**8))
		os.system("sort " + output_file + ".txt > " + output_file + "_ordered.txt")
		output_file = "MOBdatasets/" + dataset + "_exact_kmc_freqkmers_"+ str(theta*(10**8)) + "_div2"
		os.system("sort " + output_file + ".txt > " + output_file + "_ordered.txt")

	for i in range(len(datasets)):
		for j in range(len(datasets)):
			if(i==j):
				continue
			os.system("python3 compute_exact_discriminative_kmers_MOB.py " + datasets[i] + " " + datasets[j] + " " + str(datasets_size[i]) + " " + str(datasets_size[j]) + " " + str(theta))
	end = time.time()
	tot_time = end - start
	output_time.write(str(tot_time) + " \n")
