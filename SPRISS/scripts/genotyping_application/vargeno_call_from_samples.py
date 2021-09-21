import os
import time

sample_sizes = [155221129,194026412,388052824,776105649,1164158473]
rt_file = open("running_times_vargeno.txt",'w')

'''
print("Indexing ...")
start_1=time.time()
os.system("./../vargeno/vargeno index hg19.fa hg19Common.vcf prefix")
end=time.time()
print("Time index = " + str(end-start_1))
rt_file.write("Time index = " + str(end-start_1) + " \n")
'''
os.system("mkdir results")
rt_file.write("VARGENO" + " \n")
for run in range(5):
    print("Run " + str(run))
    rt_file.write("Run " + str(run) + " \n")
    for i in range(len(sample_sizes)):
        print("Calling ...")
        print("Sample rate = " + str(sample_sizes[i]/1552211298.0))
        rt_file.write("Sample rate = " + str(sample_sizes[i]/1552211298.0) + " \n")

        start_s=time.time()
        print("Creating the sample ...")
        os.system("./create_sample 75x.fastq 75x_sample"+str(i)+".fastq 1552211298 "+str(sample_sizes[i]))
        end_s=time.time()
        print("Sampling Time " + str(end_s-start_s))
        rt_file.write("Sampling Time " + str(end_s-start_s) + " \n")

        start_2=time.time()
        os.system("./../vargeno/vargeno geno prefix 75x_sample"+str(i)+".fastq hg19Common.vcf vargeno_output_sample.vcf")
        end=time.time()
        print("Time call = " + str(end-start_2))
        rt_file.write("Time call = " + str(end-start_2) + " \n")

        print("Evalutation ...")
        os.system("./../rtg-tools-3.12.1/rtg bgzip vargeno_output_sample.vcf")
        os.system("./../rtg-tools-3.12.1/rtg index -f vcf vargeno_output_sample.vcf.gz")
        os.system("./../rtg-tools-3.12.1/rtg vcfeval -t hg19.sdf -b NA12878.vcf.gz --bed-regions=ConfidentRegions.bed.gz -c vargeno_output_sample.vcf.gz -f QUAL -o vargeno_evaluations_sample_"+str(i))

        os.system("rm 75x_sample"+str(i)+".fastq")
        os.system("rm vargeno_output_sample*")
        os.system("mv vargeno_evaluations_sample_"+str(i)+"/summary.txt results/vargeno_summary_"+str(i)+"_run"+str(run)+".txt")
        os.system("rm -r vargeno_evaluations_sample_"+str(i))
rt_file.close()
