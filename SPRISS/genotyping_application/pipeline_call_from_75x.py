import os
import time

start=time.time()
os.system("./pipeline_script.sh 75x.fastq work_dir_pipeline_75x")
end=time.time()
print("Time " + str(end-start))
