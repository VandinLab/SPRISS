import os
datasets = ['SRS024075','SRS024388','SRS011239','SRS075404','SRS043663','SRS062761']
os.system("mkdir work_dir")

for dataset in datasets:
	os.system("mkdir " + dataset)

n_runs = 5
for run in range(n_runs):
	print("Run " + str(run) + " ...")
	print("Estimating frequent k-mers ...")
	os.system("python3 compute_frequentkmers_withsakeima.py " + str(run))
	print("Estimating Bray-Curtis distances ...")
	os.system("python3 compute_approx_distances_withsakeima.py " + str(run))
	print("Computing deviations and false negative rates ...")
	os.system("python3 compute_deviations_fn_rates_withsakeima.py " + str(run))
print("Averaging SAKEIMA results ...")
os.system("python3 averaging_SAKEIMA.py " + str(n_runs))

