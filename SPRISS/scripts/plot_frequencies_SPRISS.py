import math
import numpy
import time
import matplotlib
from matplotlib import pyplot as plt
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')
#import matplotlib.pyplot as plt

SMALL_SIZE = 14
MEDIUM_SIZE = 17
BIGGER_SIZE = 23
plt.rc('font', size=SMALL_SIZE)          # controls default text sizes 
plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title 
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels 
plt.rc('xtick', labelsize=18)    # fontsize of the tick labels 
plt.rc('ytick', labelsize=18)    # fontsize of the tick labels 
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize 
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title 

fin1 = open("SRS024075/SRS024075_kmc_31-mers_0_freq_ordered.txt",'r')
fin2 = open("SRS024075/exact_kmc_all_kmers.txt",'r')

data = dict()
#sample_size = 0.0

for line in fin1:
    items = line.split(' ')
    kmer = items[0]
    freq = float(items[2])
    #sample_size += freq
    data[kmer] = freq
    #break

total_positions = 8819242497.0
data_list = list()
for line in fin2:
    items = line.split(' ')
    kmer = items[0]
    count_exact = float(items[1])
    #total_positions += count_exact
    if kmer in data:
        data_list.append( (count_exact, data[kmer]) )
    #break

data_list.sort()
exact_frequencies = list()
unbiased_frequencies = list()
x = range(1,len(data_list)+1)
#print x
for tuple_ in data_list:
    exact_frequencies.append(tuple_[0] / total_positions)
    unbiased_frequencies.append(tuple_[1] )

#if, ax1 = plt.subplots(figsize=(7, 5))
plt.title("SPRISS - exact vs estimated frequency", fontsize=19)
plt.xlabel("Exact frequency")
plt.ylabel("Frequency estimated by SPRISS")
ax = plt.axes()
ax.grid(b=True, which='major', color='0.9', axis='y', linestyle='-')
ax.grid(b=True, which='major', color='0.9', axis='x', linestyle='-')
#ax1.grid(b=True, which='major', color='0.9', axis='y', linestyle='-')
#ax1.grid(b=True, which='major', color='0.9', axis='x', linestyle='-')
shape = '.'
label_ = r'$(f_\mathcal{D},f_\mathcal{S})$'
#ax1.plot(exact_frequencies, unbiased_frequencies,  ms =5,c='green',label=label_, marker=shape,zorder=9, lw = 0.0, mew = 0.0)#'TopKWY')#,color='b')
plt.plot(exact_frequencies,unbiased_frequencies,ms =5,c='green',label=label_, marker=shape,zorder=9, lw = 0.0, mew = 0.0)
#label_ = r'$f_A$'
#ax1.plot(x, unbiased_frequencies, ms =4,c='green',label=label_, marker=shape,zorder=7, lw = 0.0, mew = 0.0)#'TopKWY')#,color='b')
#ax1.plot([10**-9,10**-4] , [10**-9,10**-4] , label=None,zorder=3,c='grey',lw=1.0)
plt.plot([10**-9,10**-4],[10**-9,10**-4], color = "grey", linestyle = "-", zorder=1)
#ax1.set_xlim(0.,1.)
#ax1.set_ylim(0.,1.)
#ax1.set_ylim(1.0 * 10**-9,10**-4)
#ax1.set_xlim(1.0 * 10**-9,10**-4)
plt.xlim(10**-9, 10**-4)
plt.xscale("log")
plt.ylim(10**-9, 10**-4)
plt.yscale("log")
print("done")
#ax1.set_yscale('log')
#ax1.set_xscale('log')
#plt.legend()
#box = ax1.get_position()
#ax1.set_position([box.x0, box.y0, box.width * 0.95, box.height])
plt.legend(loc='best',numpoints=1, prop={'size': 16})
#ax1.legend(loc='best', bbox_to_anchor=(1, 0.5))
plt.savefig('frequencies_bounds.png',dpi=300,bbox_inches='tight')
#plt.savefig('frequencies_bounds.pdf',dpi=50)

