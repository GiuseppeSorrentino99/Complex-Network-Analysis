import numpy as np
from collections import namedtuple,defaultdict
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
import math
import random as rd
import operator
from networkx.algorithms.community import naive_greedy_modularity_communities
g = nx.read_gml("lesmiserables.gml")

no_nodes = g.number_of_nodes()
no_edges = g.number_of_edges()

print("number of nodes:" + str (no_nodes))
print("number of edges:" + str (no_edges))
degrees = nx.degree(g)
degrees_values = []
for node, deg in degrees:
    degrees_values.append(deg)
mean_degree = np.mean(degrees_values)
print("il grado medio della rete sarà : " + str(mean_degree))
degree_centralities = nx.degree_centrality(g)
sorted_nodes = dict(sorted(degree_centralities.items(), key=operator.itemgetter(1),reverse=True))
sorted_nodes = list(sorted_nodes.keys())
print("i 5 nodi con la degree centrality più alta sono:")
print(sorted_nodes[0])
print(sorted_nodes[1])
print(sorted_nodes[2])
print(sorted_nodes[3])
print(sorted_nodes[4])
betweennes_centralities = nx.betweenness_centrality(g)
sorted_nodes = dict(sorted(betweennes_centralities.items(), key=operator.itemgetter(1),reverse=True))
sorted_nodes = list(sorted_nodes.keys())
print("i 5 nodi con la betweennes centrality più alta sono:")
print(sorted_nodes[0])
print(sorted_nodes[1])
print(sorted_nodes[2])
print(sorted_nodes[3])
print(sorted_nodes[4])
closeness_centralities = nx.closeness_centrality(g)
sorted_nodes = dict( sorted(closeness_centralities.items(), key=operator.itemgetter(1),reverse=True))
sorted_nodes = list(sorted_nodes.keys())
print("i 5 nodi con la closeness centrality più alta sono:")
print(sorted_nodes[0])
print(sorted_nodes[1])
print(sorted_nodes[2])
print(sorted_nodes[3])
print(sorted_nodes[4])
eigenvector_centralities = nx.eigenvector_centrality(g)
sorted_nodes = dict(sorted(eigenvector_centralities.items(), key=operator.itemgetter(1),reverse=True))
sorted_nodes = list(sorted_nodes.keys())
print("i 5 nodi con la eigenvector centrality più alta sono:")
print(sorted_nodes[0])
print(sorted_nodes[1])
print(sorted_nodes[2])
print(sorted_nodes[3])
print(sorted_nodes[4])
cores = []
i = 0
copied_core = nx.read_gml("lesmiserables.gml")
dim = copied_core.number_of_nodes()
flag = True
while(copied_core.number_of_nodes() > 0 ):
    if(flag):
        lista = []
    degree_centralities = nx.degree_centrality(copied_core)
    labels = dict(sorted(degree_centralities.items(), key=operator.itemgetter(1),reverse=False))
    labels = list(labels.keys())
    flag = True
    for j in range(0,len(labels),1):
        val = copied_core.degree(labels[j])
        if (val <= i):
            lista.append(labels[j])
            copied_core.remove_node(labels[j])
            flag = False
    if(flag):
        i = i+1
        cores.append(lista)
print("il valore di K è: "+ str(len(cores)-1))
nx.number_connected_components(g)
iter = []
#t = 1/dim
t = 0.1
threshold = dim * t
threshold_string = str(t*100) + "%" + " dei nodi, ovvero " + str(math.floor(threshold)) + " nodi"
print("vediamo quanti nodi devo rimuovere per avere la componente gigante con meno del " + threshold_string)
#Visto che la rete è randomica, per avere dei valori significativi devo ripetere più volte l'esperimento
for k in range(1,100,1):
    g = nx.read_gml("lesmiserables.gml")
    count = 0
    flag = 0
    dim = g.number_of_nodes()
    for i in range(dim):
        #print("----------------------------------------------------------------------------------------------------------------------------")
        n = g.number_of_nodes()
        rand = rd.randint(1,n-1)
        labels = list(g.nodes())
        rem = labels[rand]
        g.remove_node(rem)
        count= count +1
        Gcc = sorted(nx.connected_components(g), key=len, reverse=True)
        giant = g.subgraph(Gcc[0])
        #for j in range(len(Gcc)):
        #    print(len(Gcc[j]))
        if giant.number_of_nodes() <= threshold:
            break
    perc_rimossi = math.floor(count/dim * 100)
    iter.append(perc_rimossi)
iter_array = np.array(iter)
mean = round(np.mean(iter_array))
perc_rimossi_string = str(mean) +"%"
print("la percentuale di nodi rimossi a causa dei failure è:" + perc_rimossi_string)
nx.number_connected_components(g)
#devo ora simulare degli attacchi mirati, quindi prendo essenzialmente i nodi con betweenness più alta. Quelli saranno i nodi da rimuovere
copied_g = nx.read_gml("lesmiserables.gml")
information_centralities = nx.information_centrality(copied_g)
sorted_nodes = dict( sorted(information_centralities.items(), key=operator.itemgetter(1),reverse=True))
sorted_nodes=list(sorted_nodes.keys())
y = nx.number_connected_components(copied_g)
count_attack = 0
flag_attack = 0
dim_attack = copied_g.number_of_nodes()
#t = 1/dim
t = 0.1
threshold_attack = dim_attack * t
threshold_string_attack = str(int(t*100)) + "%" + " dei nodi, ovvero " + str(math.floor(threshold_attack)) + " nodi"
print("vediamo quanti nodi devo attaccare per avere la componente gigante con meno del " + threshold_string_attack)
rem_attack = sorted_nodes[0]
for i in sorted_nodes:
    copied_g.remove_node(rem_attack)
    count_attack= count_attack +1
    Gcc_attack = sorted(nx.connected_components(copied_g), key=len, reverse=True)
    # for j in range(len(Gcc_attack)):
    #       print(len(Gcc_attack[j]))
    giant_attack = copied_g.subgraph(Gcc_attack[0])
    dimensione_giant_attack = giant_attack.number_of_nodes()
    if dimensione_giant_attack <= threshold_attack:
        break
    information_centralities = nx.information_centrality(giant_attack)
    sorted_nodes = dict( sorted(information_centralities.items(), key=operator.itemgetter(1),reverse=True))
    resorted=list(sorted_nodes.keys())
    #print(resorted)
    rem_attack = resorted[0]
    # print(sorted_nodes.get(rem_attack))
    #print(rem_attack)

print("ho rimosso: " + str(count_attack) + " nodi")
perc_rimossi = math.floor(count_attack/dim_attack * 100)
perc_rimossi_string = str(perc_rimossi) + "%"
print("la percentuale di nodi rimossi nell'attacco è:" + perc_rimossi_string)
