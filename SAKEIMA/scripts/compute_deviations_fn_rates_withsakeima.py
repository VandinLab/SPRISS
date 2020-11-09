import os
import time
import sys

run = sys.argv[1]

datasets = ['SRS024075','SRS024388','SRS011239','SRS075404','SRS043663','SRS062761']
datasets_size = [8819242497,7924744349,8135441782,7754975225,9156418180,8265706595] #k31
k = 31
thetas = [2.5,5.0,7.5,10.0]
thetas[:] = [x / float(10**8) for x in thetas]
results_file = open("rates_and_deviations_run"+run+".txt",'w')

avgdevmax = 0.0
max_max = 0.0
max_false_negative = 0.0
avg_avg = 0.0
n_avg = 0

for i,dataset in enumerate(datasets):
	print(dataset)
	results_file.write(dataset + " \n")
	for t,theta in enumerate(thetas):
		print(str(theta))
		results_file.write(str(theta) + " \n")
		start = time.time() 
		exact_freq_file = "../../KMC/scripts/" + dataset +"/exact_kmc_freqkmers_"+ str(theta*(10**8))+"_ordered.txt"
		approx_freq_file = dataset + "/freqkmers_sakeima_" + str(k) + "_" + str(t) + "_ordered.txt"
		dataset1 = open(exact_freq_file,'r')
		dataset2 = open(approx_freq_file,'r')
		
		max_dev = 0.0
		avg_dev = 0.0
		size_true_positive = 0.0
		size_false_positive = 0.0
		size_freqkmers_exact = 0.0
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
					size_false_positive = size_false_positive + 1
					line2 = dataset2.readline()
				elif(kmer1 == kmer2):
					exact_freq = float(splitted_line1[1])/datasets_size[i]
					approx_freq = float(splitted_line2[2])
					max_dev = max(max_dev,abs(exact_freq-approx_freq))
					avg_dev = avg_dev + abs(exact_freq-approx_freq)
					size_true_positive = size_true_positive + 1
					size_freqkmers_exact = size_freqkmers_exact + 1
					line1 = dataset1.readline()
					line2 = dataset2.readline()
					if(line1 == ''):
						break
					splitted_line1 = line1.split(' ')
					kmer1 = splitted_line1[0]
				else:
					size_freqkmers_exact = size_freqkmers_exact + 1
					size_false_negative = size_false_negative + 1
					line1 = dataset1.readline()
					if (line1 == ''):
						break
					splitted_line1 = line1.split(' ')
					kmer1 = splitted_line1[0]

		if(line1 != ''):
			splitted_line1 = line1.split(' ')
			size_freqkmers_exact = size_freqkmers_exact + 1
			size_false_negative = size_false_negative + 1
			line1 = dataset1.readline()
			while(line1):
				splitted_line1 = line1.split(' ')
				size_freqkmers_exact = size_freqkmers_exact + 1
				size_false_negative = size_false_negative + 1
				line1 = dataset1.readline()

		if(line2 != ''):
			splitted_line2 = line2.split(' ')
			size_false_positive = size_false_positive + 1
			line2 = dataset2.readline()
			while(line2):
				splitted_line2 = line2.split(' ')
				size_false_positive = size_false_positive + 1
				line2 = dataset2.readline()

		false_negative_rate = float(size_false_negative)/float(size_freqkmers_exact)
		false_positive_rate = float(size_false_positive)/(float(size_false_positive)+float(size_true_positive))
		avg_dev = avg_dev/size_true_positive
		print("Max_dev= " + str(max_dev))
		results_file.write("Max_dev= " + str(max_dev) + " \n")
		print("Avg_dev= " + str(avg_dev))
		results_file.write("Avg_dev= " + str(avg_dev) + " \n")
		print("False_negative_rate= " + str(false_negative_rate))
		results_file.write("False_negative_rate= " + str(false_negative_rate) + " \n")
		print("False_positive_rate= " + str(false_positive_rate))
		results_file.write("False_positive_rate= " + str(false_positive_rate) + " \n")
		avgdevmax = max(avgdevmax,avg_dev)
		avg_avg = avg_avg + avg_dev
		n_avg = n_avg + 1
		max_max = max(max_max,max_dev)
		max_false_negative = max(max_false_negative,false_negative_rate)
		end = time.time()
		tot_time = (end - start)
		print("Time= " + str(tot_time))
		results_file.write("Time= " + str(tot_time) + " \n")
print("Max_max= " + str(max_max) + " Max_avg= " + str(avgdevmax) + " Avg_avg= " + str(avg_avg/n_avg) + " Max_false_negative= " + str(max_false_negative))
results_file.write("Max_max= " + str(max_max) + " Max_avg= " + str(avgdevmax) + " Max_false_negative= " + str(max_false_negative) + " \n")
results_file.close()

