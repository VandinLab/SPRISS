from matplotlib import pyplot as plt
import scipy.special
import random
from matplotlib.patches import Patch
import os
import numpy as np

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

sample_rate = [0.1,0.125,0.25,0.5,0.75]
runs = 5
n_samplesizes = 5

rt_file = open("running_times_vargeno.txt")
avg_rt_file = open("avg_running_times_vargeno.txt",'w')

samplingtime_vargeno = list()
calltime_vargeno = list()
for i in range(n_samplesizes):
    samplingtime_vargeno.append(np.zeros(runs))
    calltime_vargeno.append(np.zeros(runs))

line = rt_file.readline()
for run in range(runs):
    line = rt_file.readline() #run
    for i in range(n_samplesizes):
        line = rt_file.readline() #sample size
        line = rt_file.readline().split(' ')
        sample_time = float(line[2])
        samplingtime_vargeno[i][run] = sample_time
        line = rt_file.readline().split(' ')
        call_time = float(line[3])
        calltime_vargeno[i][run] = call_time

for i in range(n_samplesizes):
    avg_rt_file.write("Sample rate = " + str(sample_rate[i]) + " \n")
    avg_rt_file.write("Sampling Time " + str(np.mean(samplingtime_vargeno[i])) + " " + str(np.std(samplingtime_vargeno[i])) + " \n")
    avg_rt_file.write("Time call = " + str(np.mean(calltime_vargeno[i])) + " " + str(np.std(calltime_vargeno[i]))+ " \n")

rt_file.close()
avg_rt_file.close()

rt_file = open("running_times_pipeline.txt")
avg_rt_file = open("avg_running_times_pipeline.txt",'w')

samplingtime_pipeline = list()
calltime_pipeline = list()
for i in range(n_samplesizes):
    samplingtime_pipeline.append(np.zeros(runs))
    calltime_pipeline.append(np.zeros(runs))

line = rt_file.readline()
for run in range(runs):
    line = rt_file.readline() #run
    for i in range(n_samplesizes):
        line = rt_file.readline() #sample size
        line = rt_file.readline().split(' ')
        sample_time = float(line[2])
        samplingtime_pipeline[i][run] = sample_time
        line = rt_file.readline().split(' ')
        call_time = float(line[3])
        calltime_pipeline[i][run] = call_time

for i in range(n_samplesizes):
    avg_rt_file.write("Sample rate = " + str(sample_rate[i]) + " \n")
    avg_rt_file.write("Sampling Time " + str(np.mean(samplingtime_pipeline[i])) + " \n")
    avg_rt_file.write("Time call = " + str(np.mean(calltime_pipeline[i])) + " \n")

rt_file.close()
avg_rt_file.close()


os.system("mkdir figures")

colors = ['red','orange','black','green','blue','magenta']

#-------------------RUNNING TIMES VARGENO
rt_file = open("avg_running_times_vargeno.txt")
plt.title("Running time - Vargeno")#, fontsize=22)
plt.xlabel("Sample rate")#, fontsize=22)
plt.ylabel("Running time (sec)")#, fontsize=22)
sample_rate = [0.1,0.125,0.25,0.5,0.75]
exact_times = [19838,19838,19838,19838]
sampling_times = []
sample_times = []
sample_rate_string=["0.125","0.25","0.5","0.75"]

for i in range(len(sample_rate)):
    rt_file.readline()
    line = rt_file.readline().split(' ')
    sample_time = float(line[2])
    sample_times.append(sample_time)
    line = rt_file.readline().split(' ')
    call_time = float(line[3])
    sampling_time = call_time #+ sample_time
    if(i == 0): continue
    sampling_times.append(sampling_time)

sample_rate = [0.125,0.25,0.5,0.75]
plt.plot(sample_rate,exact_times, color = colors[4], linestyle='--', label = "Vargeno")
plt.plot(sample_rate,sampling_times, marker = "x", linestyle='-', color = colors[0] , ms=10, label = "SPRISS+Vargeno")

ax = plt.axes()
ax.grid(b=True, which='major', color='0.9', axis='y', linestyle='-')
ax.grid(b=True, which='major', color='0.9', axis='x', linestyle='-')
ax.set_xticks(sample_rate)
ax.set_xticklabels(sample_rate_string)
ax.set_xticklabels([],minor=True)
#plt.xticks(thetas_plot,thetas_strings)
#plt.yticks(fontsize=fontsize_titles)
plt.legend(loc='best', ncol=2, prop={'size': 12.5})
#plt.show()

#plt.tight_layout()
plt.savefig('figures/running_time_vargeno_senzasample.pdf',dpi=300, bbox_inches='tight')
plt.clf()
rt_file.close()

#---------------RUNNING TIMES PIPELINE
rt_file = open("avg_running_times_pipeline.txt")
plt.title("Running time - Pipeline Standard")#, fontsize=22)
plt.xlabel("Sample rate")#, fontsize=22)
plt.ylabel("Running time (sec)")#, fontsize=22)
sample_rate = [0.1,0.125,0.25,0.5,0.75]
exact_times = [51516,51516,51516,51516]
sampling_times = []
sample_rate_string=["0.125","0.25","0.5","0.75"]

for i in range(len(sample_rate)):
    rt_file.readline()
    line = rt_file.readline().split(' ')
    sample_time = float(line[2])
    line = rt_file.readline().split(' ')
    call_time = float(line[3])
    sampling_time = call_time #+ sample_time
    if(i == 0): continue
    sampling_times.append(sampling_time)

sample_rate = [0.125,0.25,0.5,0.75]
plt.plot(sample_rate,exact_times, color = colors[4], linestyle='--', label = "Pipeline")
plt.plot(sample_rate,sampling_times, marker = "x", linestyle='-', color = colors[0] , ms=10, label = "SPRISS+Pipeline")

ax = plt.axes()
ax.grid(b=True, which='major', color='0.9', axis='y', linestyle='-')
ax.grid(b=True, which='major', color='0.9', axis='x', linestyle='-')
ax.set_xticks(sample_rate)
ax.set_xticklabels(sample_rate_string)
ax.set_xticklabels([],minor=True)
#plt.xticks(thetas_plot,thetas_strings)
#plt.yticks(fontsize=fontsize_titles)
plt.legend(loc='best', ncol=2, prop={'size': 12.5})
#plt.show()

#plt.tight_layout()
plt.savefig('figures/running_time_pipeline_senzasample.pdf',dpi=300, bbox_inches='tight')
plt.clf()
rt_file.close()




#--------------- VARGENO
sample_rate = [0.1,0.125,0.25,0.5,0.75]
sample_rate_string=["0.125","0.25","0.5","0.75"]
exact_sens = []
exact_prec = []
exact_fm = []
sampling_sens = []
sampling_prec = []
sampling_fm = []

exact_file = open("vargeno_evaluations_full/summary.txt",'r')
exact_file.readline()
exact_file.readline()
line = exact_file.readline().split(' ')
values = []
for e in line:
    if(e != ''):
        values.append(e)
print(values)
exact_sens_value = float(values[-2])
exact_prec_value = float(values[-3])
exact_fm_value = float(values[-1])
exact_file.close()

for i in range(len(sample_rate)):
    avg_sampling_sens = 0.0
    avg_sampling_prec = 0.0
    avg_sampling_fm = 0.0
    for run in range(runs):
        file_name = "results/vargeno_summary_"+str(i)+"_run"+str(run)+".txt"
        sample_file = open(file_name,'r')
        sample_file.readline()
        sample_file.readline()
        line = sample_file.readline().split(' ')
        values = []
        for e in line:
            if(e != ''):
                values.append(e)
        avg_sampling_sens += float(values[-2])
        avg_sampling_prec += float(values[-3])
        avg_sampling_fm += float(values[-1])
        sample_file.close()

    if(i == 0): continue
    exact_sens.append(exact_sens_value)
    exact_prec.append(exact_prec_value)
    exact_fm.append(exact_fm_value)

    sampling_sens.append(avg_sampling_sens/runs)
    sampling_prec.append(avg_sampling_prec/runs)
    sampling_fm.append(avg_sampling_fm/runs)

######SENSITIVITY
plt.title("Sensitivity - Vargeno")#, fontsize=22)
plt.xlabel("Sample rate")#, fontsize=22)
plt.ylabel("Sensitivity")#, fontsize=22)

sample_rate = [0.125,0.25,0.5,0.75]
plt.plot(sample_rate,exact_sens, color = colors[4], linestyle='--', label = "Vargeno")
plt.plot(sample_rate,sampling_sens, marker = "x", linestyle='-', color = colors[0] , ms=10, label = "SPRISS+Vargeno")

ax = plt.axes()
ax.grid(b=True, which='major', color='0.9', axis='y', linestyle='-')
ax.grid(b=True, which='major', color='0.9', axis='x', linestyle='-')
ax.set_xticks(sample_rate)
ax.set_xticklabels(sample_rate_string)
ax.set_xticklabels([],minor=True)
#plt.xticks(thetas_plot,thetas_strings)
#plt.yticks(fontsize=fontsize_titles)
plt.legend(loc='best', ncol=2, prop={'size': 12.5})
#plt.show()

#plt.tight_layout()
plt.savefig('figures/sensitivity_vargeno.pdf',dpi=300, bbox_inches='tight')
plt.clf()

######PRECISION
plt.title("Precision - Vargeno")#, fontsize=22)
plt.xlabel("Sample rate")#, fontsize=22)
plt.ylabel("Precision")#, fontsize=22)

plt.plot(sample_rate,exact_prec, color = colors[4], linestyle='--', label = "Vargeno")
plt.plot(sample_rate,sampling_prec, marker = "x", linestyle='-', color = colors[0] , ms=10, label = "SPRISS+Vargeno")

ax = plt.axes()
ax.grid(b=True, which='major', color='0.9', axis='y', linestyle='-')
ax.grid(b=True, which='major', color='0.9', axis='x', linestyle='-')
ax.set_xticks(sample_rate)
ax.set_xticklabels(sample_rate_string)
ax.set_xticklabels([],minor=True)
#plt.xticks(thetas_plot,thetas_strings)
#plt.yticks(fontsize=fontsize_titles)
plt.legend(loc='best', ncol=2, prop={'size': 12.5})
#plt.show()

#plt.tight_layout()
plt.savefig('figures/precision_vargeno.pdf',dpi=300, bbox_inches='tight')
plt.clf()

######FM
plt.title("F-measure - Vargeno")#, fontsize=22)
plt.xlabel("Sample rate")#, fontsize=22)
plt.ylabel("F-Measure")#, fontsize=22)

plt.plot(sample_rate,exact_fm, color = colors[4], linestyle='--', label = "Vargeno")
plt.plot(sample_rate,sampling_fm, marker = "x", linestyle='-', color = colors[0] , ms=10, label = "SPRISS+Vargeno")

ax = plt.axes()
ax.grid(b=True, which='major', color='0.9', axis='y', linestyle='-')
ax.grid(b=True, which='major', color='0.9', axis='x', linestyle='-')
ax.set_xticks(sample_rate)
ax.set_xticklabels(sample_rate_string)
ax.set_xticklabels([],minor=True)
#plt.xticks(thetas_plot,thetas_strings)
#plt.yticks(fontsize=fontsize_titles)
plt.legend(loc='best', ncol=2, prop={'size': 12.5})
#plt.show()

#plt.tight_layout()
plt.savefig('figures/fm_vargeno.pdf',dpi=300, bbox_inches='tight')
plt.clf()


#--------------- PIPELINE
sample_rate = [0.1,0.125,0.25,0.5,0.75]
sample_rate_string=["0.125","0.25","0.5","0.75"]
exact_sens = []
exact_prec = []
exact_fm = []
sampling_sens = []
sampling_prec = []
sampling_fm = []

exact_file = open("work_dir_pipeline_90x/results/summary.txt",'r')
exact_file.readline()
exact_file.readline()
line = exact_file.readline().split(' ')
values = []
for e in line:
    if(e != ''):
        values.append(e)
exact_sens_value = float(values[-2])
exact_prec_value = float(values[-3])
exact_fm_value = float(values[-1])
exact_file.close()

for i in range(len(sample_rate)):

    avg_sampling_sens = 0.0
    avg_sampling_prec = 0.0
    avg_sampling_fm = 0.0
    for run in range(runs):
        file_name = "results/pipeline_summary_"+str(i)+"_run"+str(run)+".txt"
        sample_file = open(file_name,'r')
        sample_file.readline()
        sample_file.readline()
        line = sample_file.readline().split(' ')
        values = []
        for e in line:
            if(e != ''):
                values.append(e)
        avg_sampling_sens += float(values[-2])
        avg_sampling_prec += float(values[-3])
        avg_sampling_fm += float(values[-1])
        sample_file.close()

    if(i == 0): continue
    exact_sens.append(exact_sens_value)
    exact_prec.append(exact_prec_value)
    exact_fm.append(exact_fm_value)

    sampling_sens.append(avg_sampling_sens/runs)
    sampling_prec.append(avg_sampling_prec/runs)
    sampling_fm.append(avg_sampling_fm/runs)

#####SENSITIVITY
plt.title("Sensitivity - Pipeline Standard")#, fontsize=22)
plt.xlabel("Sample rate")#, fontsize=22)
plt.ylabel("Sensitivity")#, fontsize=22)

sample_rate = [0.125,0.25,0.5,0.75]
plt.plot(sample_rate,exact_sens, color = colors[4], linestyle='--', label = "Pipeline")
plt.plot(sample_rate,sampling_sens, marker = "x", linestyle='-', color = colors[0] , ms=10, label = "SPRISS+Pipeline")

ax = plt.axes()
ax.grid(b=True, which='major', color='0.9', axis='y', linestyle='-')
ax.grid(b=True, which='major', color='0.9', axis='x', linestyle='-')
ax.set_xticks(sample_rate)
ax.set_xticklabels(sample_rate_string)
ax.set_xticklabels([],minor=True)
#plt.xticks(thetas_plot,thetas_strings)
#plt.yticks(fontsize=fontsize_titles)
plt.legend(loc='best', ncol=2, prop={'size': 12.5})
#plt.show()

#plt.tight_layout()
plt.savefig('figures/sensitivity_pipeline.pdf',dpi=300, bbox_inches='tight')
plt.clf()

#####PRECISION
plt.title("Precision - Pipeline Standard")#, fontsize=22)
plt.xlabel("Sample rate")#, fontsize=22)
plt.ylabel("Precision")#, fontsize=22)

plt.plot(sample_rate,exact_prec, color = colors[4], linestyle='--', label = "Pipeline")
plt.plot(sample_rate,sampling_prec, marker = "x", linestyle='-', color = colors[0] , ms=10, label = "SPRISS+Pipeline")

ax = plt.axes()
ax.grid(b=True, which='major', color='0.9', axis='y', linestyle='-')
ax.grid(b=True, which='major', color='0.9', axis='x', linestyle='-')
ax.set_xticks(sample_rate)
ax.set_xticklabels(sample_rate_string)
ax.set_xticklabels([],minor=True)
#plt.xticks(thetas_plot,thetas_strings)
#plt.yticks(fontsize=fontsize_titles)
plt.legend(loc='best', ncol=2, prop={'size': 12.5})
#plt.show()

#plt.tight_layout()
plt.savefig('figures/precision_pipeline.pdf',dpi=300, bbox_inches='tight')
plt.clf()

######FM
plt.title("F-measure - Pipeline Standard")#, fontsize=22)
plt.xlabel("Sample rate")#, fontsize=22)
plt.ylabel("F-measure")#, fontsize=22)

plt.plot(sample_rate,exact_fm, color = colors[4], linestyle='--', label = "Pipeline")
plt.plot(sample_rate,sampling_fm, marker = "x", linestyle='-', color = colors[0] , ms=10, label = "SPRISS+Pipeline")

ax = plt.axes()
ax.grid(b=True, which='major', color='0.9', axis='y', linestyle='-')
ax.grid(b=True, which='major', color='0.9', axis='x', linestyle='-')
ax.set_xticks(sample_rate)
ax.set_xticklabels(sample_rate_string)
ax.set_xticklabels([],minor=True)
#plt.xticks(thetas_plot,thetas_strings)
#plt.yticks(fontsize=fontsize_titles)
plt.legend(loc='best', ncol=2, prop={'size': 12.5})
#plt.show()

#plt.tight_layout()
plt.savefig('figures/fm_pipeline.pdf',dpi=300, bbox_inches='tight')
plt.clf()
