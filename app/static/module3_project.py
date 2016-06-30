"""
Template for Project 3
Student will implement four functions:

slow_closest_pairs(cluster_list)
fast_closest_pair(cluster_list) - implement fast_helper()
hierarchical_clustering(cluster_list, num_clusters)
kmeans_clustering(cluster_list, num_clusters, num_iterations)

where cluster_list is a list of clusters in the plane
"""

import math
import alg_cluster



def pair_distance(cluster_list, idx1, idx2):
    """
    Helper function to compute Euclidean distance between two clusters
    in cluster_list with indices idx1 and idx2
    
    Returns tuple (dist, idx1, idx2) with idx1 < idx2 where dist is distance between
    cluster_list[idx1] and cluster_list[idx2]
    """
    return (cluster_list[idx1].distance(cluster_list[idx2]), min(idx1, idx2), max(idx1, idx2))


def slow_closest_pairs(cluster_list):
    """
    Compute the set of closest pairs of cluster in list of clusters
    using O(n^2) all pairs algorithm
    
    Returns the set of all tuples of the form (dist, idx1, idx2) 
    where the cluster_list[idx1] and cluster_list[idx2] have minimum distance dist.   
    
    """
    num = len(cluster_list)
    set_closest_pairs = set([])
    temp_min_distance = pair_distance(cluster_list, 0, 1)[0]
    for index_i in range(num):
        for index_j in range(index_i+1,num):
            distance = pair_distance(cluster_list, index_i, index_j)[0]
            if distance < temp_min_distance:
                temp_min_distance = distance
    for index_i in range(num):
        for index_j in range(index_i+1,num):
            distance, idx1, idx2 = pair_distance(cluster_list, index_i, index_j)
            if 	distance == temp_min_distance:
                set_closest_pairs.update(set([(distance, idx1, idx2)]) )			
    return set_closest_pairs

def fast_closest_pair(cluster_list):
    """
    Compute a closest pair of clusters in cluster_list
    using O(n log(n)) divide and conquer algorithm
    
    Returns a tuple (distance, idx1, idx2) with idx1 < idx 2 where
    cluster_list[idx1] and cluster_list[idx2]
    have the smallest distance dist of any pair of clusters
    """    
    def fast_helper_3(cluster_list, horiz_order, vert_order):
        """
        helper
        """
        q_tuples = [(cluster_list[idx].distance(cluster_list[idy]),idx, idy) for idx in horiz_order for idy in horiz_order if not idx == idy]
        q_min = min([item[0] for item in q_tuples])
        q_indices = [ (item[1], item[2]) for item in q_tuples if item[0] == q_min ]
        return (q_min, min(q_indices[0]), max(q_indices[0]))
    
    def fast_helper(cluster_list, horiz_order, vert_order):
        """
        Divide and conquer method for computing distance between closest pair of points
        Running time is O(n * log(n))
        
        horiz_order and vert_order are lists of indices for clusters
        ordered horizontally and vertically
        
        Returns a tuple (distance, idx1, idx2) with idx1 < idx 2 where
        cluster_list[idx1] and cluster_list[idx2]
        have the smallest distance dist of any pair of clusters
    
        """
        # num = len(horiz_order)
        if len(horiz_order) <= 3:
            return fast_helper_3(cluster_list, horiz_order, vert_order)   
        # base case
        else:
            if len(horiz_order) % 2 == 1:
                num_m = len(horiz_order)/2 + 1
            else:
                num_m = len(horiz_order)/2
            mid = .5 * (cluster_list[num_m-1].horiz_center() + cluster_list[num_m].horiz_center())
            horiz_order_left = horiz_order[:num_m]
            horiz_order_right = horiz_order[num_m:]
            horiz_order_left_set = set(horiz_order_left)
            horiz_order_right_set = set(horiz_order_right)
            #vert_order_left = [item for item in vert_order if item in horiz_order_left]
            #vert_order_right = [item for item in vert_order if item in horiz_order_right]               
        # divide
            distance_left, idx1_left, idx2_left = fast_helper(cluster_list, horiz_order_left, [idx for idx in vert_order if idx in horiz_order_left_set])
            distance_right, idx1_right, idx2_right = fast_helper(cluster_list, horiz_order_right, [idx for idx in vert_order if idx in horiz_order_right_set])
        # conquer
            if distance_left <= distance_right:
                distance, idx1, idx2 = distance_left, idx1_left, idx2_left
            else:
                distance, idx1, idx2 = distance_right, idx1_right, idx2_right
            vert_s = [idx for idx in vert_order if abs(cluster_list[idx].horiz_center() - mid) < 50*distance]
            num_s = len(vert_s)
            for idx in range(num_s - 1):
                for idy in range(idx + 1, 1 + min(idx + 3, num_s - 1)):
                    if min(distance, pair_distance(cluster_list, vert_s[idx], vert_s[idy])[0]) < distance:
                        distance, idx1, idx2 = pair_distance(cluster_list, vert_s[idx], vert_s[idy])         
        return (distance, idx1, idx2)
            
    # compute list of indices for the clusters ordered in the horizontal direction
    hcoord_and_index = [(cluster_list[idx].horiz_center(), idx) 
                        for idx in range(len(cluster_list))]    
    hcoord_and_index.sort()
    horiz_order = [hcoord_and_index[idx][1] for idx in range(len(hcoord_and_index))]
     
    # compute list of indices for the clusters ordered in vertical direction
    vcoord_and_index = [(cluster_list[idx].vert_center(), idx) 
                        for idx in range(len(cluster_list))]    
    vcoord_and_index.sort()
    vert_order = [vcoord_and_index[idx][1] for idx in range(len(vcoord_and_index))]

    # compute answer recursively
    answer = fast_helper(cluster_list, horiz_order, vert_order) 
    return (answer[0], min(answer[1:]), max(answer[1:]))
    

def hierarchical_clustering(cluster_list, num_clusters):
    """
    Compute a hierarchical clustering of a set of clusters
    Note: the function mutates cluster_list
    
    Input: List of clusters, number of clusters
    Output: List of clusters whose length is num_clusters
    """
    while len(cluster_list) > num_clusters:
        # print len(cluster_list)
        closest_pair_i,  closest_pair_j = fast_closest_pair(cluster_list)[1:]
        cluster_list[closest_pair_i].merge_clusters(cluster_list[closest_pair_j])
        cluster_list.remove(cluster_list[closest_pair_j])
    return cluster_list



    
def kmeans_clustering(cluster_list, num_clusters, num_iterations):
    """
    Compute the k-means clustering of a set of clusters
    
    Input: List of clusters, number of clusters, number of iterations
    Output: List of clusters whose length is num_clusters
    """
    cluster_list_k = []
    population_counties_list = [item.total_population() for item in cluster_list]
    dummy_k = num_clusters
    while dummy_k>0:
        max_population = max(population_counties_list)
        idx = population_counties_list.index(max_population)
        cluster_list_k.append(cluster_list[idx])
        population_counties_list[idx] = -1
        dummy_k-=1
    cluster_list_k.reverse()    
    for iteration in range(num_iterations):
        if iteration:
            pass
        # print iteration
        temp_clusters = [alg_cluster.Cluster(set([]), item.horiz_center(), item.vert_center(), 0, 0.0) for item in cluster_list_k]
        for index in range(len(cluster_list)):
            min_index = 0
            min_value = 100000000.0
            for idx in range(num_clusters):
                if cluster_list[index].distance(cluster_list_k[idx]) < min_value:
                    min_index = idx
                    min_value = cluster_list[index].distance(cluster_list_k[idx])
            temp_clusters[min_index].merge_clusters(cluster_list[index])		
        for idx in range(num_clusters):
            cluster_list_k[idx] =  temp_clusters[idx]
    return temp_clusters

def gen_random_clusters(num_clusters):
    out = []
    for item in range(num_clusters):
        out.append([0,2*random.random() - 1, 2*random.random() - 1, 1, 0])
    out_clusters = []
    for line in out:
        out_clusters.append(alg_cluster.Cluster(set([line[0]]), line[1], line[2], line[3], line[4]))
    return out_clusters



