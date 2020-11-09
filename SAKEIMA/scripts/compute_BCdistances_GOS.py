import os
import time
import math
import random
import sys
import numpy as np

method = sys.argv[1]

def get_dataset_name(i):
	prefix = "JCVI_SMPL_11032830000"
	true_index = i+8
	suffix = ""
	if(true_index<=9):
		suffix = suffix + "0" + str(true_index)
	else:
		if(i==35):
			suffix = suffix + str(52)
		elif(i==36):
			suffix = suffix + str(56)
		else:
			suffix = suffix + str(true_index)
	dataset_name = "datasetGOS/" + prefix + suffix #"datasetGOS/" + ...
	return dataset_name

k = 21
n_dataset = 37

distances = []
times = [0,0,0,0,0] #for 5 runs
for i in range(n_dataset):
	for j in range(i+1,n_dataset,1):
		distances.append([])

n_runs = 1
if(method == "sampling"):
	n_runs = 5

of = open(method+"_BCdistances_GOS_k"+str(k)+".txt",'w')
for run in range(n_runs):
	#compute frequent kmers
	start = time.time()
	for i in range(n_dataset):
		dataset_name = get_dataset_name(i)
		print(dataset_name)
		if(method == "sampling"):
			dataset_all = open(dataset_name+".fa",'r')
			dataset_name = dataset_name + "_wuk_sampling"
			sample = open(dataset_name+".fa",'w')
			line = dataset_all.readline()
			while(line):
				read = dataset_all.readline()
				flip = random.random()
				if(flip < 0.50):
					sample.write(line)
					sample.write(read)
				line = dataset_all.readline()
			sample.close()
		output_file = dataset_name + "_allcounts_filtered"
		cmd = "python run_jellyfish.py -L 2 -k "+str(k)+" -db " + dataset_name + ".fa -o " + output_file + " -thr 32 -keep 1"
		os.system(cmd)
	end = time.time()
	counting_time = end - start

	start = time.time()
	#sorting
	print("Sorting ...")
	for i in range(n_dataset):
		dataset_name = get_dataset_name(i)
		filetosort = dataset_name + "_allcounts_filtered"
		if(method == "sampling"):
			filetosort = dataset_name + "_wuk_sampling_allcounts_filtered"
		os.system("sort " + filetosort + ".txt > " + filetosort + "_ordered.txt")
	
	#compute distances
	print("Compute BC distances ... ")
	z = 0
	for i in range(n_dataset):
		for j in range(i+1,n_dataset,1):
			dataset1_name = get_dataset_name(i)
			dataset2_name = get_dataset_name(j)
			if(method == "sampling"):
				dataset1_name = dataset1_name + "_wuk_sampling"
				dataset2_name = dataset2_name + "_wuk_sampling"
			dataset1 = open(dataset1_name+"_allcounts_filtered_ordered.txt",'r')
			dataset2 = open(dataset2_name+"_allcounts_filtered_ordered.txt",'r')
			sum1 = 0.0
			sum2 = 0.0
			sum12 = 0.0
			line1 = dataset1.readline()
			line2 = ""
			while line1:
				splitted_line1 = line1.split(' ')
				kmer1 = splitted_line1[0]
				line2 = dataset2.readline()
				if(line2 == ''):
					break
				while line2:
					splitted_line2 = line2.split(' ')
					kmer2 = splitted_line2[0]
					if(kmer1 > kmer2):
						sum2 = sum2 + float(splitted_line2[1])
						line2 = dataset2.readline()
					elif(kmer1 == kmer2):
						sum12 = sum12 + float(min(float(splitted_line1[1]),float(splitted_line2[1])))
						sum1 = sum1 + float(splitted_line1[1])
						sum2 = sum2 + float(splitted_line2[1])
						line1 = dataset1.readline()
						line2 = dataset2.readline()
						if(line1 == ''):
							break
						splitted_line1 = line1.split(' ')
						kmer1 = splitted_line1[0]
					else:
						sum1 = sum1 + float(splitted_line1[1])
						line1 = dataset1.readline()
						if (line1 == ''):
							break
						splitted_line1 = line1.split(' ')
						kmer1 = splitted_line1[0]			
			if(line1 != ''):
				splitted_line1 = line1.split(' ')
				sum1 = sum1 + float(splitted_line1[1])
				line1 = dataset1.readline()
				while(line1):
					splitted_line1 = line1.split(' ')
					sum1 = sum1 + float(splitted_line1[1])
					line1 = dataset1.readline()

			if(line2 != ''):
				splitted_line2 = line2.split(' ')
				sum2 = sum2 + float(splitted_line2[1])
				line2 = dataset2.readline()
				while(line2):
					splitted_line2 = line2.split(' ')
					sum2 = sum2 + float(splitted_line2[1])
					line2 = dataset2.readline()
			fact = sum12/(sum1 + sum2)
			bc_dist = 1.0 - 2.0 * fact
			print(dataset1_name + "-" + dataset2_name + " " + str(bc_dist))
			if(method == "exact"):
				of.write(dataset1_name + "-" + dataset2_name + " " + str(bc_dist) + " \n")
			else:
				distances[z].append(bc_dist)
				z = z + 1
			dataset1.close()
			dataset2.close()
	end = time.time()
	if(method == "sampling"):
		times[run] = counting_time + (end-start)
	else:
		print("Tot_time: " + str(counting_time + (end-start)))
		of.write("Tot_time: " + str(counting_time + (end-start)) + " \n")
	
	#clean the folder
	for i in range(n_dataset):
		dataset_name = get_dataset_name(i)
		filetosort = dataset_name + "_allcounts_filtered"
		if(method == "sampling"):
			filetosort = dataset_name + "_wuk_sampling_allcounts_filtered"
		os.system("rm " + filetosort + ".txt")

if(method == "sampling"):
	z = 0
	for i in range(n_dataset):
		for j in range(i+1,n_dataset,1):
			dataset1_name = get_dataset_name(i)
			dataset2_name = get_dataset_name(j)
			mean = np.mean(distances[z])
			std = np.std(distances[z])
			z = z + 1
			of.write(dataset1_name + "-" + dataset2_name + " " + str(mean) + " " + str(std) + " \n")
	mean = np.mean(times)
	std = np.std(times)
	of.write("Tot_time: "  + str(mean) + " " + str(std) + " \n")
of.close()
