import math
import os
import time
import subprocess
import sys
import numpy as np

datasets = ['SRS024075','SRS024388','SRS011239','SRS075404','SRS043663','SRS062761']
tot_reads = [138050470.0,119684324.0,123832980.0,122090110.0,130805974.0,118081524.0]
datasets_size = [8819242497,7924744349,8135441782,7754975225,9156418180,8265706595] #k31
avg_read_length = [93.88419019380541,96.21372036842386,95.69689105596845,93.51845561984399,99.99999990672346,99.9999992404889]
max_read_length = [95,101,101,101,100,100]

k = 31
delta = 0.1
thetas = [2.5,5.0,7.5,10.0]
thetas[:] = [x / float(10**8) for x in thetas]

output = open("samplesize_comparison.txt",'w')

min_ss_1 = 10**25
min_ss_2 = 10**25

for i,dataset in enumerate(datasets):
        output.write(dataset + " \n")
        for j,theta in enumerate(thetas):
                output.write(str(theta) + " \n")
                epsilon = theta - 2.0/datasets_size[i]
                #sample size with union bound
                m = math.ceil( (2.0/(epsilon**2))*(((max_read_length[i]-k+1)/(avg_read_length[i]-k+1))**2)*(math.log(2*(4**31)) + math.log(1.0/delta))  )
                min_ss_1 = min(min_ss_1,m)
                #sample size with pseudodimension without bags
                m = math.ceil( (2.0/(epsilon**2))*(((max_read_length[i]-k+1)/(avg_read_length[i]-k+1))**2)*(math.floor(math.log2(min(2*(max_read_length[i]-k+1) ,4**31))) + math.log(1.0/delta))  )
                min_ss_2 = min(min_ss_2,m)
                #sample size with pseudodimension with bags - SPRISS
                l = math.floor((0.9/theta)/(avg_read_length[i]-k+1))
                m = math.ceil((2/((epsilon*l*(avg_read_length[i]-k+1))**2)) * ( math.floor(math.log2(min(2*l*(max_read_length[i]-k+1) ,4**31))) + math.log(2.0/delta)  ) )
                ml = int(m*l)
                factor =float(ml)/float(tot_reads[i])
                output.write("SPRISS_samplesize= " + str(factor) + " \n")
                #sample size - SAKEIMA
                l = math.floor(0.9/theta)
                m = math.ceil((2/((epsilon*l)**2)) * ( math.floor(math.log2(min(2*l,4**31))) + math.log(4.0/delta)  ) )
                ml = int(m*l)
                factor =float(ml)/float(datasets_size[i])
                output.write("SAKEIMA_samplesize= " + str(factor) + " \n")                
output.write("Minimum sample size with union bound m: " + str(min_ss_1) + " \n")
output.write("Minimum sample size with pseudodimension without bags m: " +str(min_ss_2) + " \n")
