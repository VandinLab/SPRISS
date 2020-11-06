import os
import time
import sys

run = sys.argv[1]

datasets = ['SRS024075','SRS024388','SRS011239','SRS075404','SRS043663','SRS062761']
datasets_size = [8819242497,7924744349,8135441782,7754975225,9156418180,8265706595] #k31
k = 31
thetas = [2.5,5.0,7.5,10.0]
thetas[:] = [x / float(10**8) for x in thetas]
results_file = open("fnrates_discriminative_kmers_run"+run+".txt",'w')

for t,theta in enumerate(thetas):
	start = time.time()
	print(str(theta))
	results_file.write(str(theta) + " \n")
	for i in range(len(datasets)):
		for j in range(len(datasets)):
			if(i==j):
				continue
			exact_discr_file = "discriminative_kmers/exact_discriminative_kmers_"+datasets[i]+"-"+datasets[j]+"_"+str(theta*(10**8))+".txt"
			approx_discr_file = "discriminative_kmers/approx_discriminative_kmers_"+datasets[i]+"-"+datasets[j]+"_"+str(theta*(10**8))+".txt"
			dataset1 = open(exact_discr_file,'r')
			dataset2 = open(approx_discr_file,'r')
			dataset1.readline()
			dataset1.readline()
			dataset2.readline()
			dataset2.readline()
			size_discr_exact = 0.0
			size_false_negative = 0.0
		
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
						size_discr_exact = size_discr_exact + 1
						line1 = dataset1.readline()
						line2 = dataset2.readline()
						if(line1 == ''):
							break
						splitted_line1 = line1.split(' ')
						kmer1 = splitted_line1[0]
					else:
						size_discr_exact = size_discr_exact + 1
						size_false_negative = size_false_negative + 1
						line1 = dataset1.readline()
						if (line1 == ''):
							break
						splitted_line1 = line1.split(' ')
						kmer1 = splitted_line1[0]

			if(line1 != ''):
				splitted_line1 = line1.split(' ')
				size_discr_exact = size_discr_exact + 1
				size_false_negative = size_false_negative + 1
				line1 = dataset1.readline()
				while(line1):
					splitted_line1 = line1.split(' ')
					size_discr_exact = size_discr_exact + 1
					size_false_negative = size_false_negative + 1
					line1 = dataset1.readline()
			'''
			if(line2 != ''):
				splitted_line2 = line2.split(' ')
				size_false_positive = size_false_positive + 1
				line2 = dataset2.readline()
				while(line2):
					splitted_line2 = line2.split(' ')
					size_false_positive = size_false_positive + 1
					line2 = dataset2.readline()
			'''
			false_negative_rate = float(size_false_negative)/float(size_discr_exact)
			print(datasets[i]+"-"+datasets[j]+" false_negative_rate= " + str(false_negative_rate))
			results_file.write(datasets[i]+"-"+datasets[j]+" false_negative_rate= " + str(false_negative_rate) + " \n")
	end = time.time()
	tot_time = (end - start)
	print("Time= " + str(tot_time))
	results_file.write("Time= " + str(tot_time) + " \n")
results_file.close()

