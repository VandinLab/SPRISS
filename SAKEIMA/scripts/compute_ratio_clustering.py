import os

jf = open("mean_similarity_exact_Jaccard_GOS_k21.txt",'r')
bcs = open("mean_similarity_sampling50_BCdistances_GOS_k21.txt",'r')
bc = open("mean_similarity_exact_BCdistances_GOS_k21.txt",'r')

jaccard_results = []
bc_exact_results = []
bc_sampling_results = []

line = jf.readline()
while(line):
    jaccard_results.append(float(line.split(' ')[1]))
    line = bc.readline()
    bc_exact_results.append(float(line.split(' ')[1]))
    line = bcs.readline()
    bc_sampling_results.append(float(line.split(' ')[1]))
    line = jf.readline()
jf.close()
bcs.close()
bc.close()

max_bc = 0
max_bcs = 0
min_bc = 1000
min_bcs = 1000

for i in range(len(jaccard_results)):
    if(i==2):
        continue
    max_bc = max(max_bc,bc_exact_results[i]/jaccard_results[i])
    max_bcs = max(max_bcs,bc_sampling_results[i]/jaccard_results[i])
    min_bc = min(min_bc,bc_exact_results[i]/jaccard_results[i])
    min_bcs = min(min_bcs,bc_sampling_results[i]/jaccard_results[i])

print("Ratios between average similarities of macro and sub-groups, Jaccard vs ExactBC [min,max]: [" + str(min_bc) + "," + str(max_bc) + "]")
print("Ratios between average similarities of macro and sub-groups, Jaccard vs SamplingBC [min,max]: [" + str(min_bcs) + "," + str(max_bcs) + "]")

trop_diff_ratio_bc = (bc_exact_results[0]-bc_exact_results[2])/(jaccard_results[0]-jaccard_results[2])
temp_diff_ratio_bc = (bc_exact_results[1]-bc_exact_results[2])/(jaccard_results[1]-jaccard_results[2])

trop_diff_ratio_bcs = (bc_sampling_results[0]-bc_sampling_results[2])/(jaccard_results[0]-jaccard_results[2])
temp_diff_ratio_bcs = (bc_sampling_results[1]-bc_sampling_results[2])/(jaccard_results[1]-jaccard_results[2])

print("Ratio (BCs(Tr,Tr) − BCs(Tr,Te))/(Js(Tr,Tr) − Js(Tr,Te)) = " + str(trop_diff_ratio_bc))
print("Ratio (BCs(Te,Te) − BCs(Tr,Te))/(Js(Te,Te) − Js(Tr,Te)) = " + str(temp_diff_ratio_bc))
print("Ratio ((approx)BCs(Tr,Tr) − (approx)BCs(Tr,Te))/(Js(Tr,Tr) − Js(Tr,Te)) = " + str(trop_diff_ratio_bcs))
print("Ratio ((approx)BCs(Te,Te) − (approx)BCs(Tr,Te))/(Js(Te,Te) − Js(Tr,Te)) = " + str(temp_diff_ratio_bcs))
