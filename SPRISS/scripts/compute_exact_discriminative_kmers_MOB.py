import os
import time
import sys
import numpy as np

dataset1_name = sys.argv[1]
dataset2_name = sys.argv[2]
dataset_size1 = float(sys.argv[3])
dataset_size2 = float(sys.argv[4])
theta = float(sys.argv[5])
output = open("MOBdatasets/exact_discriminative_kmers_"+dataset1_name+"-"+dataset2_name+"_"+str(theta*(10**8))+".txt",'w')

print("Computing exact discriminative k-mers " + dataset1_name + "-" + dataset2_name + " ...")
dataset1_path = "MOBdatasets/" + dataset1_name + "_exact_kmc_freqkmers_"+ str(theta*(10**8))+"_ordered.txt"
dataset2_path = "MOBdatasets/" + dataset2_name + "_exact_kmc_freqkmers_"+ str(theta*(10**8))+"_div2_ordered.txt"			
output.write(dataset1_name + " + \n")
output.write(dataset2_name + " - \n")

dataset1 = open(dataset1_path,'r')
dataset2 = open(dataset2_path,'r')
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
			line2 = dataset2.readline()
		elif(kmer1 == kmer2):
			if(float(splitted_line1[1])/dataset_size1 >= 2*(float(splitted_line2[1])/dataset_size2)):
				output.write(kmer1 + " " + str((float(splitted_line1[1])/dataset_size1)/(float(splitted_line2[1])/dataset_size2)) + " \n")
			line1 = dataset1.readline()
			line2 = dataset2.readline()
			if(line1 == ''):
				break
			splitted_line1 = line1.split(' ')
			kmer1 = splitted_line1[0]
		else:
			kmer1 = splitted_line1[0]
			output.write(kmer1 + " inf \n")
			line1 = dataset1.readline()
			if (line1 == ''):
				break
			splitted_line1 = line1.split(' ')
			kmer1 = splitted_line1[0]

	if(line1 != ''):
		splitted_line1 = line1.split(' ')
		kmer1 = splitted_line1[0]
		output.write(kmer1 + " inf \n")
		line1 = dataset1.readline()
		while(line1):
			splitted_line1 = line1.split(' ')
			kmer1 = splitted_line1[0]
			output.write(kmer1 + " inf \n")
			line1 = dataset1.readline()

	'''
	if(line2 != ''):
		splitted_line2 = line2.split(' ')
		line2 = dataset2.readline()
		while(line2):
			splitted_line2 = line2.split(' ')
			line2 = dataset2.readline()
	'''
output.close()
