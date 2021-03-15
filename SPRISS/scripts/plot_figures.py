from matplotlib import pyplot as plt
import scipy.special
import random
from matplotlib.patches import Patch
import os

os.system("mkdir figures")

SMALL_SIZE = 17
MEDIUM_SIZE = 19
BIGGER_SIZE = 20
plt.rc('font', size=SMALL_SIZE)          # controls default text sizes 
plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title 
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels 
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels 
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels 
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize 
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title 

datasets = ["HMP1","HMP2","HMP3","HMP4","HMP5","HMP6"]
n_datasets = 6
n_combinations = int(scipy.special.binom(n_datasets,2))
pair_datasets_hmp = []
for i in range(n_datasets):
    for j in range(i+1,n_datasets,1):
        pair_datasets_hmp.append(datasets[i]+"-"+datasets[j])

approx_file_reads_kmc = open("SPRISS_time.txt", 'r')
approx_file_sake = open("../../SAKEIMA/scripts/SAKEIMA_time.txt", 'r')
exact_file_kmc = open("time_frequentkmers_kmc.txt", 'r')

colors = ['red','orange','black','green','blue','magenta']
times_per_thetas_exact_kmc = [0,0,0,0]
times_per_thetas_exact_discriminative = [0,0,0,0]
times_per_thetas_reads_kmc = [0,0,0,0]
times_per_thetas_reads_kmc_discriminative = [0,0,0,0]
times_per_thetas_sake = [0,0,0,0]
n_datasets = 6

plt.xlim(2e-8, 1.2e-7)
plt.xscale("log")
thetas_plot = []
for d in range(n_datasets): #n_datasets
    #reads_time = []
    reads_time_kmc = []
    sakeima_time = []
    #exact_times = []
    exact_times_kmc = []
    reads_samplesize = []
    sakeima_samplesize = []
    thetas = []
    #line = approx_file_reads.readline() #dataset
    line = approx_file_reads_kmc.readline() #dataset
    line = approx_file_sake.readline() #dataset
    line = exact_file_kmc.readline() #dataset
    #line = exact_file.readline() #dataset
    dataset = line.split('\n')[0]
    for i in range(4): #number of thetas
        #exact_file.readline() #theta
        exact_file_kmc.readline() #theta
        #approx_file_reads.readline() #theta
        approx_file_reads_kmc.readline() #theta
        line = approx_file_sake.readline() #theta
        theta = float(line.split('\n')[0])
        thetas.append(theta)
        #line = approx_file_reads.readline()
        #line = approx_file_reads_kmc.readline()
        #reads_samplesize.append(float(line.split(' ')[1]))
        #line = approx_file_sake.readline()
        #sake_samplesize.append(float(line.split(' ')[1]))
        #line = approx_file_reads.readline()
        #time_sample_creation = float(line.split(' ')[1])
        #line = approx_file_reads.readline()
        #reads_time.append(float(line.split(' ')[1])) #+time_sample_creation)
        #times_per_thetas_reads[i] = times_per_thetas_reads[i] + float(line.split(' ')[1]) #+time_sample_creation
        line = approx_file_reads_kmc.readline()
        #time_sample_creation = float(line.split(' ')[1])
        #line = approx_file_reads_kmc.readline()
        reads_time_kmc.append(float(line.split(' ')[0])) #+time_sample_creation)
        times_per_thetas_reads_kmc[i] = times_per_thetas_reads_kmc[i] + float(line.split(' ')[0]) #+time_sample_creation
        times_per_thetas_reads_kmc_discriminative[i] = times_per_thetas_reads_kmc_discriminative[i] + float(line.split(' ')[0]) #+time_sample_creation
        line = approx_file_sake.readline()
        sakeima_time.append(float(line.split(' ')[0]))
        times_per_thetas_sake[i] = times_per_thetas_sake[i] + float(line.split(' ')[0])
        #line = exact_file.readline()
        #exact_time = float(line.split(' ')[1])
        #exact_times.append(exact_time)
        #times_per_thetas_exact[i] = times_per_thetas_exact[i] + exact_time
        line = exact_file_kmc.readline()
        exact_time = float(line.split(' ')[1])
        exact_times_kmc.append(exact_time)
        times_per_thetas_exact_kmc[i] = times_per_thetas_exact_kmc[i] + exact_time
        times_per_thetas_exact_discriminative[i] = times_per_thetas_exact_discriminative[i] + exact_time
    #plt.plot(thetas,reads_time, marker = "x", linestyle=':', color = colors[d], label = dataset+" (RS-Jellyfish) " , ms=4)
    plt.plot(thetas,exact_times_kmc, color = colors[d], linestyle='--', label = datasets[d]+" (E)")
    plt.plot(thetas,sakeima_time, marker = ".", linestyle=':', color = colors[d], ms=15)
    #plt.plot(thetas,exact_times, color = colors[d], linestyle='--', label = dataset+" (exact-Jellyfish) ")
    plt.plot(thetas,reads_time_kmc, marker = "x", linestyle='-', color = colors[d] , ms=15)
    thetas_plot = thetas


#fontsize_titles = 22
#plt.rcParams.update({'font.size': 30})
plt.title("Running time")#, fontsize=22)
plt.xlabel(r'$\theta$')#, fontsize=22)
thetas_strings = []
for t in thetas_plot:
    thetas_strings.append(str(t).replace("0",""))
ax = plt.axes()
ax.grid(b=True, which='major', color='0.9', axis='y', linestyle='-')
ax.grid(b=True, which='major', color='0.9', axis='x', linestyle='-')
ax.set_xticks(thetas_plot)
ax.set_xticklabels(thetas_strings)
ax.set_xticklabels([],minor=True)
#plt.xticks(thetas_plot,thetas_strings)
plt.ylabel("Running time (sec)")#, fontsize=22)
#plt.yticks(fontsize=fontsize_titles)
plt.legend(loc='best', ncol=2, prop={'size': 12.5})
#plt.show()

#plt.tight_layout()
plt.savefig('figures/running_time.pdf',dpi=300, bbox_inches='tight')
plt.clf()
approx_file_sake.close()
approx_file_reads_kmc.close()
exact_file_kmc.close()


#approx_file_reads = open("output_approx_distances_run0_withJelly.txt", 'r')
approx_file_reads_kmc = open("SPRISS_distances_approx.txt", 'r')
approx_file_sake = open("../../SAKEIMA/scripts/SAKEIMA_distances_approx.txt", 'r')
exact_file_kmc = open("output_exact_distances_and_runningtime.txt", 'r')

legend_elements = []
thetas = []
#line = approx_file_sake.readline() #sorting time
#line = approx_file_reads.readline() #sorting time

for i in range(4): #number of thetas
    if(i==0):
        plt.figure(figsize=(9, 8.5))
        SMALL_SIZE = 26
        MEDIUM_SIZE = 28
        BIGGER_SIZE = 40
        plt.rc('font', size=SMALL_SIZE)          # controls default text sizes 
        plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title 
        plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels 
        plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels 
        plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels 
        plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize 
        plt.rc('figure', titlesize=BIGGER_SIZE)
    else:
        #plt.figure(figsize=(10, 8))
        SMALL_SIZE = 17
        MEDIUM_SIZE = 19
        BIGGER_SIZE = 20
        plt.rc('font', size=SMALL_SIZE)          # controls default text sizes 
        plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title 
        plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels 
        plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels 
        plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels 
        plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize 
        plt.rc('figure', titlesize=BIGGER_SIZE)
    plt.xlim(0.35, 1)
    plt.ylim(0.35, 1)
    plt.plot([0,1],[0,1], color = "grey", linestyle = "-", zorder=1)
    #line = exact_file.readline() #theta
    line = exact_file_kmc.readline() #theta
    line = approx_file_sake.readline() #theta
    line = approx_file_reads_kmc.readline() #theta
    #line = approx_file_reads.readline() #theta
    theta = float(line)
    thetas.append(theta)
    colors = ['black','red','grey','darkorange','darkgoldenrod','blue','pink','lime','aquamarine','yellow','cyan','skyblue','blueviolet', 'magenta', 'green']
    for j in range(n_combinations):
        #line = exact_file.readline()
        line = exact_file_kmc.readline()
        splitting = line.split(" ")
        exact_distance = float(splitting[1])
        pair_datasets = splitting[0]
        line = approx_file_sake.readline()
        splitting = line.split(" ")
        approx_distance = float(splitting[1])
        plt.scatter(exact_distance,approx_distance, marker = ".", color = colors[j], label = pair_datasets_hmp[j]+" (SK) ", s=100, zorder=2)
        #line = approx_file_reads.readline()
        line = approx_file_reads_kmc.readline()
        splitting = line.split(" ")
        approx_distance = float(splitting[1])
        plt.scatter(exact_distance,approx_distance, marker = "x", color = colors[j], label = pair_datasets_hmp[j]+" (SP) ", s=100, zorder=2)
        if(i==0):
            legend_elements.append(Patch(facecolor=colors[j],label=pair_datasets_hmp[j]))
    #line = exact_file.readline() #distance time
    #times_per_thetas_exact[i] = times_per_thetas_exact[i] + float(line.split(' ')[2])
    line = exact_file_kmc.readline() #distance time
    times_per_thetas_exact_kmc[i] = times_per_thetas_exact_kmc[i] + float(line.split(' ')[1])
    #line = exact_file.readline() #std distance time
    line = approx_file_sake.readline() #distace time
    times_per_thetas_sake[i] = times_per_thetas_sake[i] + float(line.split(' ')[0])
    #line = approx_file_reads.readline() #distace time
    #times_per_thetas_reads[i] = times_per_thetas_reads[i] + float(line.split(' ')[1])
    line = approx_file_reads_kmc.readline() #distace time
    times_per_thetas_reads_kmc[i] = times_per_thetas_reads_kmc[i] + float(line.split(' ')[0])
    plt.title("Exact vs estimated BC dist. (" + r'$\theta = $' + str(theta) + ")")
    plt.xlabel('BC distance (exact)')
    plt.ylabel('BC distance (sampling)')
    #plt.legend(handles=legend_elements, loc='center right', bbox_to_anchor=(1, 0.5))
    if(i==0):
        plt.legend(handles=legend_elements, loc='best',prop={'size': 14}, ncol=2)
    if(i==1):
        plt.legend(handles=legend_elements, loc='best',prop={'size': 9}, ncol=2)
    #plt.show()
    ax = plt.axes()
    ax.grid(b=True, which='major', color='0.9', axis='y', linestyle='-')
    ax.grid(b=True, which='major', color='0.9', axis='x', linestyle='-')
    plt.savefig("figures/theta"+str(i+1)+".pdf",dpi=300, bbox_inches='tight')
    plt.close()
    plt.clf()


approx_file_sake.close()
approx_file_reads_kmc.close()
exact_file_kmc.close()


#tempi insieme
plt.figure(figsize=(9, 8.5))
SMALL_SIZE = 26
MEDIUM_SIZE = 28
BIGGER_SIZE = 40
plt.rc('font', size=SMALL_SIZE)          # controls default text sizes 
plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title 
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels 
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels 
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels 
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize 
plt.rc('figure', titlesize=BIGGER_SIZE)
plt.xlim(2e-8, 1.2e-7)
plt.xscale("log")
colors = ['red','green','blue']
#plt.plot(thetas,times_per_thetas_exact, color = colors[2], linestyle='--', label = "Exact")
plt.plot(thetas,times_per_thetas_exact_kmc, color = colors[2], linestyle='--', label = "Exact")
#plt.plot(thetas,times_per_thetas_reads, marker = "x", linestyle=':', color = colors[0], label = "Reads Sampling - Jellyfish" , ms=4)
plt.plot(thetas,times_per_thetas_reads_kmc, marker = "x", linestyle='-', color = colors[0], label = "SPRISS" , ms=15)
plt.plot(thetas,times_per_thetas_sake, marker = ".", linestyle=':', color = colors[1], label = "SAKEIMA", ms=15)
plt.title("Running time")
plt.xlabel(r'$\theta$')
plt.ylabel("Running time (sec)")
plt.legend(loc='best',prop={'size': 28})
ax = plt.axes()
ax.grid(b=True, which='major', color='0.9', axis='y', linestyle='-')
ax.grid(b=True, which='major', color='0.9', axis='x', linestyle='-')
ax.set_xticks(thetas_plot)
ax.set_xticklabels(thetas_strings)
ax.set_xticklabels([],minor=True)
#plt.show()
plt.savefig('figures/all_running_time.pdf',dpi=300, bbox_inches='tight')
plt.close()
plt.clf()


#sample size
SMALL_SIZE = 17
MEDIUM_SIZE = 19
BIGGER_SIZE = 20
plt.rc('font', size=SMALL_SIZE)          # controls default text sizes 
plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title 
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels 
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels 
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels 
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize 
plt.rc('figure', titlesize=BIGGER_SIZE)
sample_sizes_file = open("samplesize_comparison.txt",'r')

colors = ['red','orange','black','green','blue','magenta']
n_datasets = 6
plt.xlim(2e-8, 1.2e-7)
plt.ylim(0, 1)
plt.xscale("log")
for d in range(n_datasets): #n_datasets
    reads_samplesize = []
    sakeima_samplesize = []
    thetas = []
    line = sample_sizes_file.readline() #dataset
    dataset = line.split('\n')[0]
    for i in range(4): #number of thetas
        line = sample_sizes_file.readline() #theta
        theta = float(line.split('\n')[0])
        thetas.append(theta)
        line = sample_sizes_file.readline()
        reads_samplesize.append(float(line.split(' ')[1]))
        line = sample_sizes_file.readline()
        sakeima_samplesize.append(float(line.split(' ')[1]))
    plt.plot(thetas,reads_samplesize, marker = "x", linestyle='-', color = colors[d], label = datasets[d] + " - (SP)", ms=10)
    plt.plot(thetas,sakeima_samplesize, marker = ".", linestyle=':', color = colors[d], label = datasets[d] + " - (SK)", ms=10)
plt.title("Fraction reads (SP) vs k-mers (SK)")
plt.xlabel(r'$\theta$')
ax = plt.axes()
ax.grid(b=True, which='major', color='0.9', axis='y', linestyle='-')
ax.grid(b=True, which='major', color='0.9', axis='x', linestyle='-')
ax.set_xticks(thetas_plot)
ax.set_xticklabels(thetas_strings)
ax.set_xticklabels([],minor=True)
plt.ylabel("Fractions")
plt.legend(loc='best',prop={'size': 12}, ncol=2)
#plt.show()
plt.savefig('figures/sample_size.pdf',dpi=300, bbox_inches='tight')
plt.clf()
sample_sizes_file.close()


rates_file_spriss = open("SPRISS_quality.txt",'r')
rates_file_sake = open("../../SAKEIMA/scripts/SAKEIMA_quality.txt",'r')

colors = ['red','orange','black','green','blue','magenta']
n_datasets = 6
data_spriss = []
data_sakeima = []
for i in range(n_datasets):
    data_spriss.append([[],[],[]])
    data_sakeima.append([[],[],[]])
#datasets = []
thetas = []
for d in range(n_datasets): #n_datasets
    line = rates_file_spriss.readline() #dataset
    dataset = line.split('\n')[0]
    #datasets.append(dataset)
    line = rates_file_sake.readline() #dataset
    thetas = []
    for i in range(4): #number of thetas
        line = rates_file_spriss.readline() #theta
        theta = float(line.split('\n')[0])
        thetas.append(theta)
        line = rates_file_sake.readline() #theta
        line = rates_file_spriss.readline()
        data_spriss[d][0].append(float(line.split(' ')[1]))
        line = rates_file_sake.readline()
        data_sakeima[d][0].append(float(line.split(' ')[1]))
        line = rates_file_spriss.readline()
        data_spriss[d][1].append(float(line.split(' ')[1]))
        line = rates_file_sake.readline()
        data_sakeima[d][1].append(float(line.split(' ')[1]))
        line = rates_file_spriss.readline()
        data_spriss[d][2].append(float(line.split(' ')[1]))
        line = rates_file_sake.readline()
        data_sakeima[d][2].append(float(line.split(' ')[1]))

for i in range(3):
    plt.xscale("log")
    for d in range(n_datasets):
        plt.plot(thetas,data_spriss[d][i], marker = "x", linestyle='-', color = colors[d], label = datasets[d] + " - (SP)", ms=10)
        plt.plot(thetas,data_sakeima[d][i], marker = ".", linestyle=':', color = colors[d], label = datasets[d] + " - (SK)", ms=10)
    plt.xlabel(r'$\theta$')
    if(i==1):
        plt.xlim(2e-8, 1.2e-7)
        plt.title("Average deviation")
        plt.ylabel("Average deviation")
        ax = plt.axes()
        ax.grid(b=True, which='major', color='0.9', axis='y', linestyle='-')
        ax.grid(b=True, which='major', color='0.9', axis='x', linestyle='-')
        ax.set_xticks(thetas_plot)
        ax.set_xticklabels(thetas_strings)
        ax.set_xticklabels([],minor=True)
        plt.legend(loc='best', prop={'size': 12}, ncol=2)
        plt.savefig('figures/avg_dev.pdf',dpi=300, bbox_inches='tight')
    elif(i==0):
        plt.xlim(2e-8, 1.2e-7)
        plt.title("Maximum deviation")
        plt.ylabel("Maximum deviation")
        ax = plt.axes()
        ax.grid(b=True, which='major', color='0.9', axis='y', linestyle='-')
        ax.grid(b=True, which='major', color='0.9', axis='x', linestyle='-')
        ax.set_xticks(thetas_plot)
        ax.set_xticklabels(thetas_strings)
        ax.set_xticklabels([],minor=True)
        plt.savefig('figures/max_dev.pdf',dpi=300, bbox_inches='tight')
    else:
        plt.xlim(2e-8, 1.2e-7)
        plt.title("False negatives rate")
        plt.ylabel("False negatives rate")
        ax = plt.axes()
        ax.grid(b=True, which='major', color='0.9', axis='y', linestyle='-')
        ax.grid(b=True, which='major', color='0.9', axis='x', linestyle='-')
        ax.set_xticks(thetas_plot)
        ax.set_xticklabels(thetas_strings)
        ax.set_xticklabels([],minor=True)
        plt.legend(loc='best', prop={'size': 10}, ncol=2)
        plt.savefig('figures/fn_rate.pdf',dpi=300, bbox_inches='tight')
    #plt.show()
    plt.clf()

rates_file_spriss.close()
rates_file_sake.close()


rates_file_discr = open("fnrates_discriminative_kmers_run0.txt", 'r')

n_datasets = 6
n_pair = (n_datasets-1)*n_datasets
lists = []
pair_datasets = []
for i in range(n_pair):
    lists.append([])
    pair_datasets.append("")

thetas = []
for t in range(4): #number of thetas
    line = rates_file_discr.readline() #theta
    theta = float(line)
    thetas.append(theta)
    for i in range(n_pair):
        line = rates_file_discr.readline()
        splitting = line.split(" ")
        rate = float(splitting[2])
        pair_datasets[i] = splitting[0]
        lists[i].append(rate)
    line = rates_file_discr.readline() #time

colors = ['black','red','grey','darkorange','blue','pink']
#datasets = ['SRS024075','SRS024388','SRS011239','SRS075404','SRS043663','SRS062761']
for i in range(n_datasets):
    d1 = datasets[i]
    plt.xlim(2e-8, 1.2e-7)
    plt.xscale("log")
    for j in range(n_datasets-1):
        plt.plot(thetas,lists[i*(n_datasets-1)+j], marker = "x", color = colors[j], label = pair_datasets[i*(n_datasets-1)+j], ms=10)
    plt.title("False negatives rate ("+d1+",·)")
    plt.xlabel(r'$\theta$')
    plt.ylabel("False negatives rate")
    plt.legend(loc='best',prop={'size': 11})
    ax = plt.axes()
    ax.grid(b=True, which='major', color='0.9', axis='y', linestyle='-')
    ax.grid(b=True, which='major', color='0.9', axis='x', linestyle='-')
    ax.set_xticks(thetas_plot)
    ax.set_xticklabels(thetas_strings)
    ax.set_xticklabels([],minor=True)
    #plt.show()
    plt.savefig("figures/fn_rate_discriminative_d"+str(i+1)+".pdf",dpi=300,bbox_inches='tight')
    plt.clf()
rates_file_discr.close()


times_per_thetas_exact_discriminative = [0,0,0,0]
times_per_thetas_reads_kmc_discriminative = [0,0,0,0]
exact_time_discr = open("time_countsfor_discriminativekmers_kmc.txt", 'r')
approx_time_discr = open("SPRISS_time.txt", 'r')
for j in range(n_datasets):
    line = exact_time_discr.readline() #dataset
    line = approx_time_discr.readline() #dataset
    for i in range(4): #number of thetas
        line = exact_time_discr.readline() #theta
        line = approx_time_discr.readline() #theta
        line = exact_time_discr.readline()
        times_per_thetas_exact_discriminative[i] = times_per_thetas_exact_discriminative[i] + float(line.split(' ')[1])
        line = approx_time_discr.readline()
        times_per_thetas_reads_kmc_discriminative[i] = times_per_thetas_reads_kmc_discriminative[i] + float(line.split(' ')[0])
exact_time_discr.close()
approx_time_discr.close()

exact_time_discr = open("exacttime_compute_discriminativekmers.txt", 'r')
approx_time_discr = open("approxtime_compute_discriminativekmers.txt", 'r')
for i in range(4): #number of thetas
    line = exact_time_discr.readline() #theta
    line = approx_time_discr.readline() #theta
    line = exact_time_discr.readline()
    times_per_thetas_exact_discriminative[i] = times_per_thetas_exact_discriminative[i] + float(line.split(' ')[0])
    line = approx_time_discr.readline()
    times_per_thetas_reads_kmc_discriminative[i] = times_per_thetas_reads_kmc_discriminative[i] + float(line.split(' ')[0])
exact_time_discr.close()
approx_time_discr.close()

colors = ['red','green','blue']
plt.xlim(2e-8, 1.2e-7)
plt.xscale("log")
plt.plot(thetas,times_per_thetas_exact_discriminative, color = colors[2], linestyle='--', label = "Exact")
plt.plot(thetas,times_per_thetas_reads_kmc_discriminative, marker = "x", linestyle='-', color = colors[0], label = "SPRISS" , ms=10)
plt.title("Running time")
plt.xlabel(r'$\theta$')
plt.ylabel("Running time (sec)")
ax = plt.axes()
ax.grid(b=True, which='major', color='0.9', axis='y', linestyle='-')
ax.grid(b=True, which='major', color='0.9', axis='x', linestyle='-')
ax.set_xticks(thetas_plot)
ax.set_xticklabels(thetas_strings)
ax.set_xticklabels([],minor=True)
plt.legend(loc='center right',prop={'size': 13})
#plt.show()
plt.savefig("figures/all_running_time_discriminative.pdf",dpi=300,bbox_inches='tight')
plt.clf()

'''
##############Mo17 e B73 OLD
rates_file_discr = open("fnrates_discriminative_kmers_MOB_run0.txt", 'r')

n_datasets = 2
n_pair = (n_datasets-1)*n_datasets
lists = []
pair_datasets = []
for i in range(n_pair):
    lists.append([])
    pair_datasets.append("")

thetas = []
for t in range(3): #number of thetas
    line = rates_file_discr.readline() #theta
    theta = float(line)
    thetas.append(theta)
    for i in range(n_pair):
        line = rates_file_discr.readline()
        splitting = line.split(" ")
        rate = float(splitting[2])
        pair_datasets[i] = splitting[0]
        lists[i].append(rate)
        line = rates_file_discr.readline() #false positive
    line = rates_file_discr.readline() #time

colors = ['black','red']
plt.xlim(9e-8, 2.2e-7)
plt.xscale("log")
for i in range(n_datasets):
    for j in range(n_datasets-1):
        plt.plot(thetas,lists[i*(n_datasets-1)+j], marker = "x", color = colors[i], label = pair_datasets[i*(n_datasets-1)+j])
plt.title("False negatives rate",fontsize=17)
plt.xlabel(r'$\theta$',fontsize=17)
plt.xticks(fontsize=14)
plt.ylabel("False negatives rate",fontsize=16)
plt.yticks(fontsize=14)
plt.legend(loc='best',prop={'size': 9})
#plt.show()
plt.savefig("fn_rate_discriminative_Rep1.pdf",dpi=300)
plt.clf()
rates_file_discr.close()

times_per_thetas_exact_discriminative = [0,0,0]
times_per_thetas_reads_kmc_discriminative = [0,0,0]
exact_time_discr = open("time_countsfor_discriminativekmers_MOB.txt", 'r')
approx_time_discr = open("approx_counts_for_discriminative_MOB_time_run0.txt", 'r')
for j in range(n_datasets):
    line = exact_time_discr.readline() #dataset
    line = approx_time_discr.readline() #dataset
    for i in range(3): #number of thetas
        line = exact_time_discr.readline() #theta
        line = approx_time_discr.readline() #theta
        line = exact_time_discr.readline()
        times_per_thetas_exact_discriminative[i] = times_per_thetas_exact_discriminative[i] + float(line.split(' ')[1])
        line = approx_time_discr.readline()
        line = approx_time_discr.readline()
        line = approx_time_discr.readline()
        times_per_thetas_reads_kmc_discriminative[i] = times_per_thetas_reads_kmc_discriminative[i] + float(line.split(' ')[1])
exact_time_discr.close()
approx_time_discr.close()

exact_time_discr = open("exacttime_compute_discriminativekmers_MOB.txt", 'r')
approx_time_discr = open("approxtime_compute_discriminativekmers_MOB.txt", 'r')
for i in range(3): #number of thetas
    line = exact_time_discr.readline() #theta
    line = approx_time_discr.readline() #theta
    line = exact_time_discr.readline()
    times_per_thetas_exact_discriminative[i] = times_per_thetas_exact_discriminative[i] + float(line.split(' ')[0])
    line = approx_time_discr.readline()
    times_per_thetas_reads_kmc_discriminative[i] = times_per_thetas_reads_kmc_discriminative[i] + float(line.split(' ')[0])
exact_time_discr.close()
approx_time_discr.close()

colors = ['red','green','blue']
plt.xlim(9e-8, 2.2e-7)
plt.xscale("log")
plt.plot(thetas,times_per_thetas_exact_discriminative, color = colors[2], linestyle='--', label = "Exact")
plt.plot(thetas,times_per_thetas_reads_kmc_discriminative, marker = "x", linestyle='-', color = colors[0], label = "SPRISS" , ms=4)
plt.title("Running time",fontsize=17)
plt.xlabel(r'$\theta$',fontsize=17)
plt.xticks(fontsize=14)
plt.ylabel("Running time (s)",fontsize=16)
plt.legend(loc='best',prop={'size': 10})
plt.yticks(fontsize=12)
#plt.show()
plt.savefig("runningtime_discriminative_Rep1.pdf",dpi=300)
plt.clf()


########### MOB FINAL RESULTS
rates_file_discr = open("MOB_results.txt", 'r')
n_sample_size = 2
line = rates_file_discr.readline()
theta = float(line)
line = rates_file_discr.readline()
exact_time = float(line.split(' ')[1])
exact_times = []
approx_times = []
sample_sizes = []
fn_rates_1 = [] #B73-Mo17
fn_rates_2 = [] #Mo17-B73
for i in range(n_sample_size):
    exact_times.append(exact_time)
    line = rates_file_discr.readline()
    sample_size = float(line.split(' ')[1])
    sample_sizes.append(sample_size)
    line = rates_file_discr.readline()
    approx_time = float(line.split(' ')[1])
    approx_times.append(approx_time)
    line = rates_file_discr.readline()
    #samples_time = float(line.split(' ')[1]) + float(line.split(' ')[2])
    line = rates_file_discr.readline()
    fn_rate_1 = float(line.split(' ')[2])
    fn_rates_1.append(fn_rate_1)
    line = rates_file_discr.readline()
    fn_rate_2 = float(line.split(' ')[2])
    fn_rates_2.append(fn_rate_2)
rates_file_discr.close()

colors = ['red','green','blue']
#plt.figure(figsize=(9, 8.5))
plt.xlim(3, 12)
plt.plot(sample_sizes,exact_times, color = colors[2], linestyle='--', label = "Exact")
plt.plot(sample_sizes,approx_times, marker = "x", linestyle='-', color = colors[0], label = "SPRISS" , ms=10)
plt.title("Running time",fontsize=17)
plt.xlabel("Number of reads (%)",fontsize=17)
plt.xticks(fontsize=12)
plt.ylabel("Running time (s)",fontsize=14)
plt.legend(loc='best',prop={'size': 14})
plt.yticks(fontsize=9)
#plt.show()
#splt.subplots_adjust(left=0.9, bottom=0.9)
plt.savefig("runningtime_MOB_discriminative.pdf",dpi=300)
plt.clf()
plt.close()

colors = ['red','green','blue']
#plt.figure(figsize=(9, 8.5))
plt.xlim(3, 12)
colors = ['black','red']
plt.plot(sample_sizes,fn_rates_1, color = 'green', marker = "x", linestyle='-', label = "B73-Mo17", ms=10)
plt.plot(sample_sizes,fn_rates_2, marker = "x", linestyle='-', color = 'magenta', label = "Mo17-B73" , ms=10)
plt.title("False negatives rate",fontsize=17)
plt.xlabel("Number of reads (%)",fontsize=17)
plt.xticks(fontsize=12)
plt.ylabel("False negatives rate",fontsize=14)
plt.legend(loc='best',prop={'size': 14})
plt.yticks(fontsize=9)
#plt.show()
#splt.subplots_adjust(left=0.9, bottom=0.9)
plt.savefig("fn_MOB_discriminative.pdf",dpi=300)
plt.clf()
plt.close()
'''
