import os
import time

os.system("g++ -o create_sample create_sample.cpp")
sample_sizes = [155221129,194026412,388052824,776105649,1164158473]
rt_file = open("running_times_pipeline.txt",'w')

rt_file.write("PIPELINE STANDARD" + " \n")
for run in range(5):
    print("Run " + str(run))
    rt_file.write("Run " + str(run) + " \n")
    for i in range(len(sample_sizes)):
        print("Calling ...")
        print("Sample rate = " + str(sample_sizes[i]/1552211298.0))
        rt_file.write("Sample rate = " + str(sample_sizes[i]/1552211298.0) + " \n")

        start_s=time.time()
        print("Creating the sample ...")
        os.system("./create_sample 75x.fastq 75x_sample_ps_"+str(i)+".fastq 1552211298 "+str(sample_sizes[i]))
        end_s=time.time()
        print("Sampling Time " + str(end_s-start_s))
        rt_file.write("Sampling Time " + str(end_s-start_s) + " \n")

        start_2=time.time()
        os.system("./pipeline_script.sh 75x_sample_ps_"+str(i)+".fastq work_dir_pipeline_75x_sample_"+str(i))
        end=time.time()
        print("Time call = " + str(end-start_2))
        rt_file.write("Time call = " + str(end-start_2) + " \n")

        os.system("rm 75x_sample_ps_"+str(i)+".fastq")
        os.system("mv work_dir_pipeline_75x_sample_"+str(i)+"/results/summary.txt results/pipeline_summary_"+str(i)+"_run"+str(run)+".txt")
        os.system("rm -r work_dir_pipeline_75x_sample_"+str(i))
rt_file.close()
