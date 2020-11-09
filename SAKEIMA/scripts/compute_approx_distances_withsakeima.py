import os
import time
import sys

run = sys.argv[1]

datasets = ['SRS024075','SRS024388','SRS011239','SRS075404','SRS043663','SRS062761']
datasets_size = [8819242497,7924744349,8135441782,7754975225,9156418180,8265706595] #k=31
k = 31
thetas = [2.5,5.0,7.5,10.0]
thetas[:] = [x / float(10**8) for x in thetas]
output = open("output_approx_distances_run"+run+"_withsakeima.txt",'w')

sorting_times = [0,0,0,0]
for dataset in datasets:
	print("Sorting approx k-mers: " + dataset)
	for j,theta in enumerate(thetas):
		print(str(theta))
		start = time.time()
		output_file = dataset+"/freqkmers_sakeima_" + str(k) + "_" + str(j)
		os.system("sort " + output_file + ".txt > " + output_file + "_ordered.txt")
		end = time.time()
		sorting_time = end-start
		sorting_times[j] = sorting_times[j] + sorting_time

for t,theta in enumerate(thetas):
	print(str(theta))
	output.write(str(theta) + " \n")
	start = time.time()
	for i in range(len(datasets)):
		for j in range(i+1,len(datasets),1):
			dataset1_path = datasets[i] + "/freqkmers_sakeima_" + str(k) + "_" + str(t) + "_ordered.txt"
			dataset2_path = datasets[j] + "/freqkmers_sakeima_"  + str(k) + "_" + str(t) + "_ordered.txt"
			dataset1 = open(dataset1_path,'r')
			dataset2 = open(dataset2_path,'r')
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
			dist = 1.0 - 2.0 * fact
			output.write(datasets[i] + "-" + datasets[j] + " " + str(dist) + "\n")
			print(datasets[i] + "-" + datasets[j] + " " + str(dist))
	end = time.time()
	print("Sorting_and_Distances_time= " + str(end - start + sorting_times[t]))
	output.write("Sorting_and_Distances_time= " + str(end - start + sorting_times[t]) + " \n")
output.close()
