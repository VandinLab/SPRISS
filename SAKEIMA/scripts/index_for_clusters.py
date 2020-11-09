import numpy as np
import seaborn as sns
import matplotlib.pylab as plt
import sys
import pandas as pd

textfile = sys.argv[1]

#color_map = plt.cm.get_cmap('autumn')
#reversed_color_map = color_map.reversed()

infile = open(textfile,'r')
n_datasets = 37
matrix = np.zeros((37,37))
indici = [6,5,3,7,2,4,13,12,11,9,8,10,28,36,32,35,34,33,1,27,26,31,29,30,24,23,22,19,17,14,0,18,20,21,16,15,25]
#nomi_dataset = ['GS02','GS03','GS04','GS05','GS06','GS07','GS08','GS09','GS10','GS11','GS12','GS13','GS14','GS15','GS16','GS17','GS18','GS19','GS20','GS21','GS22','GS23','GS25','GS26','GS27','GS28','GS29','GS30','GS31','GS32','GS33','GS34','GS35','GS36','GS37','GS47','GS51']
nomi_dataset = ['TN1','TN2','TN3','TN4','TN5','TN6','TS1','TS2','TS3','E1','E2','TS4','TG1','TO1','TO2','TO3','TO4','TO5','NC1','TG2','TG3','TO6','NC2','TO7','TG4','TG5','TG6','TG7','TG8','NC3','NC4','TG11','TG12','TG13','TG14','TG15','TG16']
etichette = []
palette = sns.color_palette()
palette.append((1,1,1))
index_of_white = len(palette)-1
#print(palette)

sns.palplot(palette)
#plt.show()

tropical = []
temperate = []
tropical_and_temperate = []
tropical_galapagos = []
tropical_ocean = []
temperate_north = []
temperate_south = []
estuary = []

for i in range(len(nomi_dataset)):
    etichette.append('')

#color_dict = {}
for i in range(n_datasets):
    index_i = indici[i]
    d1 = nomi_dataset[i]
    for j in range(i+1,n_datasets,1):
        line = infile.readline()
        index_j = indici[j]
        d2 = nomi_dataset[j]
        similarity = 1 - float(line.split(' ')[1])
        if(d1[0:2] == "TN" and d2[0:2] == "TN"):
            temperate_north.append(similarity)
            temperate.append(similarity)
        elif(d1[0:2] == "TS" and d2[0:2] == "TS"):
            temperate_south.append(similarity)
            temperate.append(similarity)
        elif(d1[0:1] == "E" and d2[0:1] == "E"):
            estuary.append(similarity)
            temperate.append(similarity)
        elif(d1[0:2] == "TG" and d2[0:2] == "TG"):
            tropical_galapagos.append(similarity)
            tropical.append(similarity)
        elif(d1[0:2] == "TO" and d2[0:2] == "TO"):
            tropical_ocean.append(similarity)
            tropical.append(similarity)
        elif((d1[0:2] == "TN" or d1[0:2] == "TS" or d1[0:1] == "E") and (d2[0:2] == "TG" or d2[0:2] == "TO")):
            tropical_and_temperate.append(similarity)
        elif((d2[0:2] == "TN" or d2[0:2] == "TS" or d2[0:1] == "E") and (d1[0:2] == "TG" or d1[0:2] == "TO")):
            tropical_and_temperate.append(similarity)

of = open("mean_similarity_"+textfile,'w')
of.write("Tropical: " + str(sum(tropical)/len(tropical)) + " \n")
of.write("Temperate: " + str(sum(temperate)/len(temperate)) + " \n")
of.write("Tropical-Temperate: " + str(sum(tropical_and_temperate)/len(tropical_and_temperate)) + " \n")
of.write("Tropical_Galapagos: " + str(sum(tropical_galapagos)/len(tropical_galapagos)) + " \n")
of.write("Tropical_Ocean: " + str(sum(tropical_ocean)/len(tropical_ocean)) + " \n")
of.write("Temperate_North: " + str(sum(temperate_north)/len(temperate_north)) + " \n")
of.write("Temperate_South: " + str(sum(temperate_south)/len(temperate_south)) + " \n")
of.write("Estuary: " + str(sum(estuary)/len(estuary)) + " \n")
#popolo in base all original gos study
#gap_2 = 2
#gap_3 = 3
#final_matrix = []
#final_matrix.append(matrix[33-gap_3])0
#final_matrix.append(matrix[20-gap_2])1
#final_matrix.append(matrix[6-gap_2])2
#final_matrix.append(matrix[4-gap_2])3
#final_matrix.append(matrix[7-gap_2])4
#final_matrix.append(matrix[3-gap_2])5
#final_matrix.append(matrix[2-gap_2])6
#final_matrix.append(matrix[5-gap_2])7
#final_matrix.append(matrix[12-gap_2])8
#final_matrix.append(matrix[11-gap_2])9
#final_matrix.append(matrix[13-gap_2])10
#final_matrix.append(matrix[10-gap_2])11
#final_matrix.append(matrix[9-gap_2])12
#final_matrix.append(matrix[8-gap_2])13
#final_matrix.append(matrix[32-gap_3])14
#final_matrix.append(matrix[35]) #G47 15
#final_matrix.append(matrix[37-gap_3])16
#final_matrix.append(matrix[31-gap_3])17
#final_matrix.append(matrix[34-gap_3])18
#final_matrix.append(matrix[30-gap_3])19
#final_matrix.append(matrix[35-gap_3])20
#final_matrix.append(matrix[36-gap_3])21
#final_matrix.append(matrix[29-gap_3])22
#final_matrix.append(matrix[28-gap_3])23
#final_matrix.append(matrix[27-gap_3])24
#final_matrix.append(matrix[36]) #G51 25
#final_matrix.append(matrix[22-gap_2])26
#final_matrix.append(matrix[21-gap_2])27
#final_matrix.append(matrix[14-gap_2])28
#final_matrix.append(matrix[25-gap_3])29
#final_matrix.append(matrix[26-gap_3])30
#final_matrix.append(matrix[23-gap_2])31
#final_matrix.append(matrix[16-gap_2])32
#final_matrix.append(matrix[19-gap_2])33
#final_matrix.append(matrix[18-gap_2])34
#final_matrix.append(matrix[17-gap_2])35
#final_matrix.append(matrix[15-gap_2])36

#print(final_matrix)
#ax = sns.heatmap(matrix, linewidth=0.5, vmin = 0.0, vmax = 1.0, cmap = 'gist_ncar', xticklabels=etichette, yticklabels=etichette)
#ax.invert_yaxis()
#plt.title("Similarity = 1 - BCdistance")
#plt.show()

'''
color_dict = {}
for i in range(37):
    if(i==9 or i==8):
        color_dict[i] = palette[5]
    elif(10<=i<=13):
        color_dict[i] = palette[1]
    elif(2<=i<=7):
        color_dict[i] = palette[6]
    elif(30<=i<=36):
        color_dict[i] = palette[7]
    elif(i==0 or i==1 or i==14 or i==29):
        color_dict[i] = palette[index_of_white]
    else:
        color_dict[i] = palette[8]

# Convert the dictionary into a Series
color_rows = pd.Series(color_dict)
color_rows.head()


#ax = sns.clustermap(matrix, linewidth=0.5, vmin = 0.0, vmax = 1.0, cmap='gist_ncar',xticklabels=etichette, yticklabels=etichette, dendrogram_ratio=(.1, .2),cbar_pos=(0.03, .2, .03, .4), col_colors=[color_rows], row_colors=[color_rows], col_cluster=False)
ax = sns.clustermap(matrix, linewidth=0.5, vmin = 0.0, vmax = 1.0, cmap='gist_ncar',xticklabels=etichette, yticklabels=etichette, dendrogram_ratio=(.1, .1), col_colors=[color_rows], row_colors=[color_rows])
ax.fig.suptitle('Similarity = 1 - BCdistance (without unique k-mers)')
plt.show()
'''
'''
ax = sns.heatmap(matrix, linewidth=0.5, vmin = 0.0, vmax = 1.0, cmap = 'gist_ncar', xticklabels=etichette, yticklabels=etichette)
ax.invert_yaxis()
plt.title("Similarity = 1 - BCdistance (without unique k-mers)")
plt.xlabel("TG=Tropical Galapagos TO=Tropical Open Ocean TN=Temperate North TS=Temperate South E=Estuary NC=Non-Classified")
plt.show()
'''
