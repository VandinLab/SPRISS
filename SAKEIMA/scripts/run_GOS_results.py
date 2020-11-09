import os

os.system("mkdir work_dir_GOS")

print("Estimating Bray-Curtis distances with sampling ...")
os.system("python3 compute_BCdistances_GOS.py sampling")
print("Computing exact Bray-Curtis distances ...")
os.system("python3 compute_BCdistances_GOS.py exact")
print("Computing exact Jaccard distances ...")
os.system("python3 compute_Jaccard_GOS.py")

