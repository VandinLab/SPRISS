import os
import time
import sys

run = sys.argv[1]

datasets = ["B73","Mo17"]
datasets_size = [99209208120,97965214600] #k=31

thetas = [2.0]
thetas[:] = [x / float(10**7) for x in thetas]
results_file = open("fnrates_discriminative_kmers_MOB_run"+run+".txt",'w')
k=31

for t,theta in enumerate(thetas):
	start = time.time()
	print(str(theta))
	results_file.write(str(theta) + " \n")
	for i in range(len(datasets)):
		for j in range(len(datasets)):
			if(i==j):
				continue
			exact_discr_file = "MOBdatasets/exact_discriminative_kmers_"+datasets[i]+"-"+datasets[j]+"_"+str(theta*(10**8))+".txt"
			approx_discr_file = "MOBdatasets/approx_discriminative_kmers_"+datasets[i]+"-"+datasets[j]+"_"+str(theta*(10**8))+".txt"
			dataset1 = open(exact_discr_file,'r')
			dataset2 = open(approx_discr_file,'r')
			dataset1.readline()
			dataset1.readline()
			dataset2.readline()
			dataset2.readline()
			size_discr_exact = 0.0
			size_false_negative = 0.0
			size_false_positive = 0.0
			size_true_positive = 0.0
			ndiv2 = 0
			ninf = 0
			
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
						size_discr_exact = size_discr_exact + 1
						size_true_positive = size_true_positive + 1
						line1 = dataset1.readline()
						line2 = dataset2.readline()
						if(line1 == ''):
							break
						splitted_line1 = line1.split(' ')
						kmer1 = splitted_line1[0]
					else:
						size_discr_exact = size_discr_exact + 1
						size_false_negative = size_false_negative + 1
						if(line1.split(' ')[1]=="inf"):
							ninf = ninf + 1
						else:
							ndiv2 = ndiv2 + 1
						line1 = dataset1.readline()
						if (line1 == ''):
							break
						splitted_line1 = line1.split(' ')
						kmer1 = splitted_line1[0]

			if(line1 != ''):
				splitted_line1 = line1.split(' ')
				size_discr_exact = size_discr_exact + 1
				size_false_negative = size_false_negative + 1
				if(line1.split(' ')[1]=="inf"):
					ninf = ninf + 1
				else:
					ndiv2 = ndiv2 + 1
				line1 = dataset1.readline()
				while(line1):
					splitted_line1 = line1.split(' ')
					size_discr_exact = size_discr_exact + 1
					size_false_negative = size_false_negative + 1
					if(line1.split(' ')[1]=="inf"):
						ninf = ninf + 1
					else:
						ndiv2 = ndiv2 + 1
					line1 = dataset1.readline()
			
			if(line2 != ''):
				splitted_line2 = line2.split(' ')
				size_false_positive = size_false_positive + 1
				line2 = dataset2.readline()
				while(line2):
					splitted_line2 = line2.split(' ')
					size_false_positive = size_false_positive + 1
					line2 = dataset2.readline()
			
			print("ndiv2% = " + str(float(ndiv2)/(ndiv2+ninf)))
			print("ninf% = " + str(float(ninf)/(ndiv2+ninf)))
			false_negative_rate = float(size_false_negative)/float(size_discr_exact)
			print(datasets[i]+"-"+datasets[j]+" false_negative_rate= " + str(false_negative_rate))
			results_file.write(datasets[i]+"-"+datasets[j]+" false_negative_rate= " + str(false_negative_rate) + " \n")
			false_positive_rate = float(size_false_positive)/(float(size_false_positive)+float(size_true_positive))
			print(datasets[i]+"-"+datasets[j]+" false_positive_rate= " + str(false_positive_rate))
			results_file.write(datasets[i]+"-"+datasets[j]+" false_positive_rate= " + str(false_positive_rate) + " \n")
	end = time.time()
	tot_time = (end - start)
	print("Time= " + str(tot_time))
	results_file.write("Time= " + str(tot_time) + " \n")
results_file.close()

