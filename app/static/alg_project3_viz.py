"""
Example code for creating and visualizing
cluster of county-based cancer risk data

Note that you must download the file
http://www.codeskulptor.org/#alg_clusters_matplotlib.py
to use the matplotlib version of this code
"""

# Flavor of Python - desktop or CodeSkulptor
DESKTOP = True

import math
import random
import urllib2
import alg_cluster
import time
import matplotlib.pyplot as plt

DESKTOP = True

# conditional imports
if DESKTOP:
    import module3_project     # desktop project solution
    import alg_clusters_matplotlib
else:
    #import userXX_XXXXXXXX as alg_project3_solution   # CodeSkulptor project solution
    import alg_clusters_simplegui
    import codeskulptor
    codeskulptor.set_timeout(30)


###################################################
# Code to load data tables

# URLs for cancer risk data tables of various sizes
# Numbers indicate number of counties in data table

DIRECTORY = "http://commondatastorage.googleapis.com/codeskulptor-assets/"
DATA_3108_URL = DIRECTORY + "data_clustering/unifiedCancerData_3108.csv"
DATA_896_URL = DIRECTORY + "data_clustering/unifiedCancerData_896.csv"
DATA_290_URL = DIRECTORY + "data_clustering/unifiedCancerData_290.csv"
DATA_111_URL = DIRECTORY + "data_clustering/unifiedCancerData_111.csv"
DATA_24_URL = DIRECTORY + "data_clustering/unifiedCancerData_24.csv"


def load_data_table(data_url):
    """
    Import a table of county-based cancer risk data
    from a csv format file
    """
    data_file = urllib2.urlopen(data_url)
    data = data_file.read()
    data_lines = data.split('\n')
    print "Loaded", len(data_lines), "data points"
    data_tokens = [line.split(',') for line in data_lines]
    return [[tokens[0], float(tokens[1]), float(tokens[2]), int(tokens[3]), float(tokens[4])] 
            for tokens in data_tokens]


############################################################
# Code to create sequential clustering
# Create alphabetical clusters for county data

def sequential_clustering(singleton_list, num_clusters):
    """
    Take a data table and create a list of clusters
    by partitioning the table into clusters based on its ordering
    
    Note that method may return num_clusters or num_clusters + 1 final clusters
    """
    
    cluster_list = []
    cluster_idx = 0
    total_clusters = len(singleton_list)
    cluster_size = float(total_clusters)  / num_clusters
    
    for cluster_idx in range(len(singleton_list)):
        new_cluster = singleton_list[cluster_idx]
        if math.floor(cluster_idx / cluster_size) != \
           math.floor((cluster_idx - 1) / cluster_size):
            cluster_list.append(new_cluster)
        else:
            cluster_list[-1] = cluster_list[-1].merge_clusters(new_cluster)
            
    return cluster_list
                

#####################################################################
# Code to load cancer data, compute a clustering and 
# visualize the results


def gen_random_clusters(num_clusters):
    out = []
    for item in range(num_clusters):
        out.append([0,2*random.random() - 1, 2*random.random() - 1, 1, 0])
    out_clusters = []
    for line in out:
        out_clusters.append(alg_cluster.Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))
    return out_clusters

def run_example():
    """
    Load a data table, compute a list of clusters and 
    plot a list of clusters

    Set DESKTOP = True/False to use either matplotlib or simplegui
    """
    data_table = load_data_table(DATA_24_URL)
    
    # data_table = gen_random_clusters(100)[0]
    
    #singleton_list = []
    #for line in data_table:
        #singleton_list.append(alg_cluster.Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))
    singleton_list = gen_random_clusters(100)
        
    #cluster_list = sequential_clustering(singleton_list, 15)	
    #print "Displaying", len(cluster_list), "sequential clusters"

    cluster_list = module3_project.hierarchical_clustering(singleton_list, 10)
    print "Displaying", len(cluster_list), "hierarchical clusters"

    #cluster_list = alg_project3_solution.kmeans_clustering(singleton_list, 9, 5)	
    #print "Displaying", len(cluster_list), "k-means clusters"

            
    # draw the clusters using matplotlib or simplegui
    
    if DESKTOP:
        alg_clusters_matplotlib.plot_clusters(data_table, cluster_list, True)
    else:
        alg_clusters_simplegui.PlotClusters(data_table, cluster_list)
    
# run_example()

def Question1():
	wynik = list()
	for step in range(2, 201):
		start = time.clock()
		cluster_list = gen_random_clusters(step)
		module3_project.slow_closest_pairs(cluster_list)
		stop = time.clock()
		wynik.append(stop-start)
	xvals = range(2, 201)
	yvals1 = wynik
	wynik = list()
	for step in range(2, 201):
		start = time.clock()
		cluster_list = gen_random_clusters(step)
		module3_project.fast_closest_pair(cluster_list)
		stop = time.clock()
		wynik.append(stop-start)
	xvals = range(2, 201)
	yvals2 = wynik
	#yvals = [1000*item for item in wynik]
	plt.plot(xvals, yvals1, '-b', label='slow_closest_pairs')
	plt.plot(xvals, yvals2, '-r', label='fast_closest_pair')
	plt.legend(loc='upper right')
	plt.title('comparison of the running times of two functions')  
	plt.xlabel('the number of initial clusters')  
	plt.ylabel('the running time of the function in seconds')  
	plt.show()


# Question1()

def Question2():
    data_table = load_data_table(DATA_3108_URL)
    singleton_list = []
    for line in data_table:
        singleton_list.append(alg_cluster.Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))
    cluster_list = module3_project.hierarchical_clustering(singleton_list, 15)
    print "Displaying", len(cluster_list), "hierarchical clusters" 
    # draw the clusters using matplotlib or simplegui
    
    if DESKTOP:
        alg_clusters_matplotlib.plot_clusters(data_table, cluster_list, True)
    else:
        alg_clusters_simplegui.PlotClusters(data_table, cluster_list)   
    
# Question2()

def Question3():
    data_table = load_data_table(DATA_3108_URL)
    singleton_list = []
    for line in data_table:
        singleton_list.append(alg_cluster.Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))
    cluster_list = module3_project.kmeans_clustering(singleton_list, 15, 5)	
    print "Displaying", len(cluster_list), "k-means clusters"
    
    # draw the clusters using matplotlib or simplegui
    
    if DESKTOP:
        alg_clusters_matplotlib.plot_clusters(data_table, cluster_list, True)
    else:
        alg_clusters_simplegui.PlotClusters(data_table, cluster_list)   
    
# Question3()

def Question5():
    data_table = load_data_table(DATA_111_URL)
    singleton_list = []
    for line in data_table:
        singleton_list.append(alg_cluster.Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))
    cluster_list = module3_project.hierarchical_clustering(singleton_list, 9)
    print "Displaying", len(cluster_list), "hierarchical clusters" 
    # draw the clusters using matplotlib or simplegui
    
    if DESKTOP:
        alg_clusters_matplotlib.plot_clusters(data_table, cluster_list, True)
    else:
        alg_clusters_simplegui.PlotClusters(data_table, cluster_list)   
    
# Question5()

def Question6():
    data_table = load_data_table(DATA_111_URL)
    singleton_list = []
    for line in data_table:
        singleton_list.append(alg_cluster.Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))
    cluster_list = module3_project.kmeans_clustering(singleton_list, 9, 5)	
    print "Displaying", len(cluster_list), "k-means clusters"
    
    # draw the clusters using matplotlib or simplegui
    
    if DESKTOP:
        alg_clusters_matplotlib.plot_clusters(data_table, cluster_list, True)
    else:
        alg_clusters_simplegui.PlotClusters(data_table, cluster_list)   
    
# Question6()

def compute_distortion(cluster_list):
    data_table = load_data_table(DATA_111_URL)
    sumax = 0
    for cluster in cluster_list:
        sumax+= cluster.cluster_error(data_table)
    return sumax

def Question7():
    data_table = load_data_table(DATA_111_URL)
    singleton_list = []
    for line in data_table:
        singleton_list.append(alg_cluster.Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))
    cluster_list = module3_project.hierarchical_clustering(singleton_list, 9)
    suma =  compute_distortion(cluster_list)
    napis = 'hierarchical_clustering ' + str(suma)
    for line in data_table:
        singleton_list.append(alg_cluster.Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))
    cluster_list = module3_project.kmeans_clustering(singleton_list, 9, 5)	
    suma =  compute_distortion(cluster_list)
    napis+= ' kmeans_clustering ' + str(suma)
    return napis

#print Question7()  


def compute_distortion_url(cluster_list, url):
    data_table = load_data_table(url)
    sumax = 0
    for cluster in cluster_list:
        sumax+= cluster.cluster_error(data_table)
    return sumax
    
def Question8(url):
    data_table = load_data_table(url)
    wynik = []
    singleton_list = []
    for line in data_table:
        singleton_list.append(alg_cluster.Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))
    cluster_list = singleton_list
    distortion_vector = []
    while len(cluster_list) > 5:
        # print len(cluster_list)
        if len(cluster_list) <=20:
            suma = compute_distortion_url(cluster_list, url)
            distortion_vector.append(suma)
        closest_pair_i,  closest_pair_j = module3_project.fast_closest_pair(cluster_list)[1:]
        cluster_list[closest_pair_i].merge_clusters(cluster_list[closest_pair_j])
        cluster_list.remove(cluster_list[closest_pair_j])
    wynik.append(distortion_vector)
    singleton_list = []
    for line in data_table:
        singleton_list.append(alg_cluster.Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))
    cluster_list = singleton_list
    distortion_vector = []
    for idx in range(6,21):
		singleton_list = []
		for line in data_table:
			singleton_list.append(alg_cluster.Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))
		cluster_list = module3_project.kmeans_clustering(singleton_list, idx, 5)
		suma = compute_distortion_url(cluster_list, url)
		distortion_vector.append(suma)
    wynik.append(distortion_vector)
    return wynik
	
#print Question8(DATA_111_URL)[0]

def Question8_graph(url):
	xvals = range(6,21)
	yvals1 = Question8(url)[0]
	yvals1.reverse()
	yvals2 = Question8(url)[1]
	plt.plot(xvals, yvals1, '-b', label='hierarchical_clustering')
	plt.plot(xvals, yvals2, '-r', label='k-means clustering')
	plt.legend(loc='upper right')
	if url == DATA_111_URL:
		plt.title(' DATA_111_URL ' + 'dataset')
	elif url == DATA_290_URL:
		plt.title(' DATA_290_URL ' + 'dataset')
	else:
		plt.title(' DATA_896_URL ' + 'dataset') 
	plt.xlabel('the number of output clusters')  
	plt.ylabel('the distortion')  
	plt.show()

# url = DATA_111_URL
# url = DATA_290_URL
# url = DATA_896_URL
# Question8_graph(url)
