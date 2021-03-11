import os

os.system("mkdir work_dir_exact")
print("Compute exact k-mers counts ...")
os.system("python3 compute_frequentkmers_exact.py")
print("Compute exact distances ...")
os.system("python3 compute_exact_distances.py")
print("Compute exact discriminative k-mers ...")
os.system("python3 run_exact_discriminative_exp.py")
'''
os.system("mkdir work_dir_exact_MOB")
print("Compute exact k-mers counts ...")
os.system("python3 compute_frequentkmers_exact_for_discriminative_MOB.py")
print("Compute exact discriminative k-mers ...")
os.system("python3 run_exact_discriminative_MOBexp.py")
'''
