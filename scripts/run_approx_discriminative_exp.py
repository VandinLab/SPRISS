import os
import time
import sys
import numpy as np

datasets = ['SRS024075','SRS024388','SRS011239','SRS075404','SRS043663','SRS062761']
datasets_size = [8819242497,7924744349,8135441782,7754975225,9156418180,8265706595] #k=31
thetas = [2.5,5.0,7.5,10.0]
thetas[:] = [x / float(10**8) for x in thetas]
k = 31
output_time = open("approxtime_compute_discriminativekmers.txt",'w')

times = [0,0,0,0]
for t,theta in enumerate(thetas):
	print(str(theta) + " \n")
	output_time.write(str(theta) + " \n")
	start = time.time()
	print("Sorting candidates discriminative k-mers and related files ... ")
	for dataset in datasets:
		output_file = dataset+"/"+dataset + "_kmc_" + str(k) + "-mers_" + str(t)
		os.system("sort " + output_file + ".txt > " + output_file + "_ordered.txt")
		output_file = dataset + "/" + dataset + "_kmc_" + str(k) + "-mers_" + str(t) + "_all"
		os.system("sort " + output_file + ".txt > " + output_file + "_ordered.txt")
	for i in range(len(datasets)):
		for j in range(len(datasets)):
			if(i==j):
				continue
			os.system("python3 compute_approx_discriminative_kmers.py " + datasets[i] + " " + datasets[j] + " " + str(datasets_size[i]) + " " + str(datasets_size[j]) + " " + str(theta) + " " + str(t))
	end = time.time()
	times[t] = end - start
	output_time.write(str(times[t]) + " \n")
