"""
Provided code for Application portion of Module 1

Imports physics citation graph 
"""


# general imports
import urllib2
import numpy as np
import matplotlib.pyplot as plt

# Set timeout for CodeSkulptor if necessary
#import codeskulptor
#codeskulptor.set_timeout(20)


###################################
# Code for loading citation graph

CITATION_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_phys-cite.txt"

EX_GRAPH1 = {0 : set([1,4,5]),
             1 : set([2,6]),
             2 : set([3]),
             3 : set([0]),
             4 : set([1]),
             5 : set([2]),
             6 : set([])}
             
EX_GRAPH7 = {0: set([1, 2, 3, 4]), 
          1: set([0, 2, 3, 4]), 
          2: set([0, 1, 3, 4]), 
          3: set([0, 1, 2, 4]), 
          4: set([0, 1, 2, 3]), 
          5: set([2, 3, 4]), 
          6: set([0, 1, 4]), 
          7: set([0, 1, 2, 3]), 
          8: set([0, 1, 4, 7]), 
          9: set([2, 4]), 
          10: set([1, 2, 4]), 
          11: set([1, 3, 4, 7]), 
          12: set([0, 2, 3]), 
          13: set([0, 2, 4, 10]), 
          14: set([0, 2, 3, 4, 13])}

def load_graph(graph_url):
    """
    Function that loads a graph given the URL
    for a text representation of the graph
    
    Returns a dictionary that models a graph
    """
    graph_file = urllib2.urlopen(graph_url)
    graph_text = graph_file.read()
    graph_lines = graph_text.split('\n')
    graph_lines = graph_lines[ : -1]
    
    print "Loaded graph with", len(graph_lines), "nodes"
    
    answer_graph = {}
    for line in graph_lines:
        neighbors = line.split(' ')
        node = int(neighbors[0])
        answer_graph[node] = set([])
        for neighbor in neighbors[1 : -1]:
            answer_graph[node].add(int(neighbor))

    return answer_graph

    
# citation_graph = load_graph(CITATION_URL)

def compute_in_degrees(digraph):
	"""
	Takes a directed graph digraph (represented as a dictionary) and computes the in-degrees for the nodes in the graph.
	"""
	graph = dict()
	if digraph == {}:
		return graph
	else:
		nodes = digraph.keys()
		for node in nodes:
			in_degree = 0
			for node_tail in nodes:
				if node in digraph[node_tail]:
					in_degree+=1
				graph[node] = in_degree
		return graph		

def in_degree_distribution(digraph):
	"""
	Takes a directed graph digraph (represented as a dictionary) and computes the unnormalized distribution of the in-degrees of the graph. 
	"""
	graph = compute_in_degrees(digraph)
	degree_distribution = dict()
	for value in graph.values():
		if degree_distribution.has_key(value):
			degree_distribution[value]+=1
		else:
			degree_distribution[value] = 1
	return degree_distribution

def in_degree_distribution_normed(digraph):
	graph_normed = {}
	graph = in_degree_distribution(digraph)
	suma = sum(graph.values())
	for key in graph.keys():
		graph_normed[key] = float(graph[key])/suma
	return graph_normed

normed_graph  = in_degree_distribution_normed(EX_GRAPH7)
x_list = normed_graph.keys()
y_list = normed_graph.values()
plt.loglog(x_list, y_list, 'ro')
plt.title('log-log plot of normalized in-degree distribution\n of the citation graph ')  
plt.xlabel('in-degrees of nodes')  
plt.ylabel('number of nodes of the given in-degree')  
plt.savefig('q1.png')  
plt.show()


