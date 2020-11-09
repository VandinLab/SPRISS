import os
import time

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

of = open("exact_Jaccard_GOS_k"+str(k)+".txt",'w')
for run in range(1):	
	#compute distances
	print("Compute exact Jaccard distances ... ")
	for i in range(n_dataset):
		for j in range(i+1,n_dataset,1):
			dataset1_name = get_dataset_name(i)
			dataset2_name = get_dataset_name(j)
			dataset1 = open(dataset1_name+"_allcounts_filtered_ordered.txt",'r')
			dataset2 = open(dataset2_name+"_allcounts_filtered_ordered.txt",'r')
			num = 0.0
			den = 0.0
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
						count = int(splitted_line2[1])
						if(count > 1):
							den += 1.0
						line2 = dataset2.readline()
					elif(kmer1 == kmer2):
						count1 = int(splitted_line1[1])
						count2 = int(splitted_line2[1])
						if((count1 > 1) and (count2 > 1)):
							num += 1.0
						if((count1 > 1) or (count2 > 1)):
							den += 1.0
						line1 = dataset1.readline()
						line2 = dataset2.readline()
						if(line1 == ''):
							break
						splitted_line1 = line1.split(' ')
						kmer1 = splitted_line1[0]
					else:
						count = int(splitted_line1[1])
						if(count > 1):
							den += 1.0
						line1 = dataset1.readline()
						if (line1 == ''):
							break
						splitted_line1 = line1.split(' ')
						kmer1 = splitted_line1[0]			
			if(line1 != ''):
				splitted_line1 = line1.split(' ')
				count = int(splitted_line1[1])
				if(count > 1):
					den += 1.0
				line1 = dataset1.readline()
				while(line1):
					splitted_line1 = line1.split(' ')
					count = int(splitted_line1[1])
					if(count > 1):
						den += 1.0
					line1 = dataset1.readline()

			if(line2 != ''):
				splitted_line2 = line2.split(' ')
				count = int(splitted_line2[1])
				if(count > 1):
					den += 1.0
				line2 = dataset2.readline()
				while(line2):
					splitted_line2 = line2.split(' ')
					count = int(splitted_line2[1])
					if(count > 1):
						den += 1.0
					line2 = dataset2.readline()
			fact = num/den
			dist = 1.0 - fact
			print(dataset1_name + "-" + dataset2_name + " " + str(dist))
			of.write(dataset1_name + "-" + dataset2_name + " " + str(dist) + " \n")
			dataset1.close()
			dataset2.close()
of.close()


