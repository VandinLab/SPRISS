import os

os.system("mkdir work_dir")

n_runs = 5
for run in range(n_runs):
	print("Run " + str(run) + " ...")
	print("Estimating frequent k-mers ...")
	os.system("python3 compute_approx_frequent_kmers.py " + str(run))
	#print("Estimating Bray-Curtis distances ...")
	#os.system("python3 compute_approx_distances.py " + str(run))
	print("Compute approximation of discriminative k-mers ...")
	os.system("python3 run_approx_discriminative_exp.py")
	print("Computing false negatives rates for discriminative k-mers ...")
	os.system("python3 compute_fnrates_discriminative_kmers.py "  + str(run))
	print("Computing deviations and false negative rates ...")
	os.system("python3 compute_deviations_fn_rates.py " + str(run))

	#print("Estimating frequent k-mers from MOB datasets...")
	#os.system("python3 compute_approx_frequent_kmers_MOB.py " + str(run))
	#print("Compute approximation of discriminative k-mers ...")
	#os.system("python3 run_approx_discriminative_MOBexp.py " + str(run))
	#print("Computing deviations and false negative rates ...")
	#os.system("python3 compute_fnrates_discriminative_kmers_MOB.py " + str(run))

os.system("python3 samplesize_comparison.py")
os.system("python3 averaging_SPRISS.py")
