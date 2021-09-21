import os
import time

print("Indexing ...")
start_1=time.time()
os.system("./../vargeno/vargeno index hg19.fa hg19Common.vcf prefix")
end=time.time()
print("Time index = " + str(end-start_1))

print("Calling ...")
start_2=time.time()
os.system("./../vargeno/vargeno geno prefix 75x.fastq hg19Common.vcf vargeno_output_full.vcf")
end=time.time()
print("Time call = " + str(end-start_2))

print("Evalutation ...")
os.system("./../rtg-tools-3.12.1/rtg bgzip vargeno_output_full.vcf")
os.system("./../rtg-tools-3.12.1/rtg index -f vcf vargeno_output_full.vcf.gz")
os.system("./../rtg-tools-3.12.1/rtg vcfeval -t hg19.sdf -b NA12878.vcf.gz --bed-regions=ConfidentRegions.bed.gz -c vargeno_output_full.vcf.gz -f QUAL -o vargeno_evaluations_full")
