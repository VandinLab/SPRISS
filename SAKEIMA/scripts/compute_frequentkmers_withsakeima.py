import math
import os
import time
import subprocess
import sys

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
of = open("sakeima_results_run"+run+".txt",'w')

for i,dataset in enumerate(datasets):
	print(dataset)
	of.write(dataset + " \n")
	for j,theta in enumerate(thetas):
		print(str(theta))
		of.write(str(theta) + " \n")
		start = time.time()
		input_db = "../../KMC/scripts/"+dataset+"/"+dataset+".fastq"
		output_file = dataset+"/freqkmers_tmp_sakeima_" + str(k) + "_" + str(j) + ".txt"
		epsilon = theta - 2.0/datasets_size[i]
		cmd = "python run_SAKEIMA.py -k 31 -db " + input_db + " -o " + output_file + " -thr 1 -t " + str(theta) + " -dt " + str(datasets_size[i])
		print(cmd)
		os.system(cmd)
		end = time.time()
		print("Count_time: " + str(end-start))
		of.write("Count_time: " + str(end-start) + " \n")
		#write frequent kmers
		allkmers = open(dataset+"/freqkmers_tmp_sakeima_" + str(k) + "_" + str(j) + ".txt",'r')
		freqkmers = open(dataset+"/freqkmers_sakeima_" + str(k) + "_" + str(j) + ".txt",'w')
		line = allkmers.readline()
		while(line):
			splitted = line.split(';')
			kmer = splitted[1]
			support = float(splitted[0])
			unbiased_frequency = float(splitted[2])
			freqkmers.write(kmer + " " + str(support) + " " + str(unbiased_frequency) + " \n")
			line = allkmers.readline()
		allkmers.close()
		freqkmers.close()
of.close()
