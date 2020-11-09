import os

os.system("python3 plot_clustering_single.py Jaccard")
os.system("python3 plot_clustering_single.py BCsampling")
os.system("python3 plot_clustering_single.py BCexact")

os.system("python3 index_for_clusters.py exact_Jaccard_GOS_k21.txt")
os.system("python3 index_for_clusters.py exact_BCdistances_GOS_k21.txt")
os.system("python3 index_for_clusters.py sampling50_BCdistances_GOS_k21.txt")

os.system("python3 compute_ratio_clustering.py > ratios_clustering_results_50.txt")
