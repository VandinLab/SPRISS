import numpy as np

datasets = ['SRS024075','SRS024388','SRS011239','SRS075404','SRS043663','SRS062761']
thetas = [2.5,5.0,7.5,10.0]
thetas[:] = [x / float(10**8) for x in thetas]
n_runs = 5

times = []
for i in range(len(datasets)):
	times.append([])
	for j in range(len(thetas)):
		times[i].append([])

times_file = open("SPRISS_time.txt",'w')
for run in range(n_runs):
	of = open("approx_mining_time_run"+str(run)+".txt",'r')
	for i,dataset in enumerate(datasets):
		line = of.readline()
		for t,theta in enumerate(thetas):
			of.readline()
			of.readline()
			of.readline()
			line = of.readline()
			time = float(line.split(' ')[1])
			times[i][t].append(time)
	of.close()
for i,dataset in enumerate(datasets):
	times_file.write(dataset + " \n")
	for t,theta in enumerate(thetas):
		times_file.write(str(theta) + " \n")
		time_list = times[i][t]
		mean = np.mean(time_list)
		std = np.std(time_list)
		times_file.write(str(mean) + " " + str(std) + " \n")
times_file.close()

distances = []
times = []
for t,theta in enumerate(thetas):
	distances.append([])
	times.append([])
	for i in range(len(datasets)):
		for j in range(i+1,len(datasets),1):
			distances[t].append([])

distances_file = open("SPRISS_distances_approx.txt",'w')
for run in range(n_runs):
	of = open("output_approx_distances_run"+str(run)+".txt",'r')
	for t,theta in enumerate(thetas):
		line = of.readline()
		z = 0
		for i in range(len(datasets)):
			for j in range(i+1,len(datasets),1):
				line = of.readline()
				dist = float(line.split(' ')[1])
				distances[t][z].append(dist)
				z = z + 1
		line = of.readline()
		time = float(line.split(' ')[1])
		times[t].append(time)
	of.close()
for t,theta in enumerate(thetas):
	distances_file.write(str(theta) + " \n")
	z = 0
	for i in range(len(datasets)):
		for j in range(i+1,len(datasets),1):
			dist_list = distances[t][z]
			z = z + 1
			mean = np.mean(dist_list)
			std = np.std(dist_list)
			distances_file.write(datasets[i]+"-"+datasets[j] + " "+  str(mean) + " " + str(std) + " \n")
	mean = np.mean(times[t])
	std = np.std(times[t])
	distances_file.write(str(mean) + " " + str(std) + " \n")
distances_file.close()

rates = []
for i in range(len(datasets)):
	rates.append([])
	for j in range(len(thetas)):
		rates[i].append([])
		for k in range(3):
			rates[i][j].append([])
quality_file = open("SPRISS_quality.txt",'w')
for run in range(n_runs):
	of = open("rates_and_deviations_run"+str(run)+".txt",'r')
	for i,dataset in enumerate(datasets):
		line = of.readline()
		for t,theta in enumerate(thetas):
			line = of.readline()
			line = of.readline()
			max_dev = float(line.split(' ')[1])
			rates[i][t][0].append(max_dev)
			line = of.readline()
			avg_dev = float(line.split(' ')[1])
			rates[i][t][1].append(avg_dev)
			line = of.readline()
			fnrate = float(line.split(' ')[1])
			rates[i][t][2].append(fnrate)
			line = of.readline()
			line = of.readline()
	of.close()
for i,dataset in enumerate(datasets):
	quality_file.write(dataset + " \n")
	for t,theta in enumerate(thetas):
		quality_file.write(str(theta) + " \n")
		max_dev_list = rates[i][t][0]
		avg_dev_list = rates[i][t][1]
		fnrate_list = rates[i][t][2]
		mean = np.mean(max_dev_list)
		std = np.std(max_dev_list)
		quality_file.write("Max_dev= " + str(mean) + " " + str(std) + " \n")
		mean = np.mean(avg_dev_list)
		std = np.std(avg_dev_list)
		quality_file.write("Avg_dev= " + str(mean) + " " + str(std) + " \n")
		mean = np.mean(fnrate_list)
		std = np.std(fnrate_list)
		quality_file.write("FalseNegative_rate= " + str(mean) + " " + str(std) + " \n")
quality_file.close()
		
