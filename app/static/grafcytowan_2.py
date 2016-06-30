import numpy as np
import matplotlib.pyplot as plt
import urllib2
import random

CITATION_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_phys-cite.txt"

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

"""
Provided code for application portion of module 1
Helper class for implementing efficient version
of DPA algorithm
"""

class DPATrial:
    """
    Simple class to encapsulate optimized trials for DPA algorithm

    Maintains a list of node numbers with multiple instances of each number.
    The number of instances of each node number are
    in the same proportion as the desired probabilities

    Uses random.choice() to select a node number from this list for each trial.
    """

    def __init__(self, num_nodes):
        """
        Initialize a DPATrial object corresponding to a
        complete graph with num_nodes nodes

        Note the initial list of node numbers has num_nodes copies of
        each node number
        """
        self._num_nodes = num_nodes
        self._node_numbers = [node for node in range(num_nodes) for dummy_idx in range(num_nodes)]


    def run_trial(self, num_nodes):
        """
        Conduct num_node trials using by applying random.choice()
        to the list of node numbers

        Updates the list of node numbers so that the number of instances of
        each node number is in the same ratio as the desired probabilities

        Returns:
        Set of nodes
        """

        # compute the neighbors for the newly-created node
        new_node_neighbors = set()
        for dummy_idx in range(num_nodes):
            new_node_neighbors.add(random.choice(self._node_numbers))

        # update the list of node numbers so that each node number
        # appears in the correct ratio
        self._node_numbers.append(self._num_nodes)
        self._node_numbers.extend(list(new_node_neighbors))

        #update the number of nodes
        self._num_nodes += 1
        return new_node_neighbors

def make_complete_graph(num_nodes):
	"""
	Takes the number of nodes num_nodes and returns a dictionary corresponding to a complete directed graph with the specified number of nodes.
	"""
	graph = dict()
	if num_nodes <=0 :
		return graph
	else:
		for node in range(num_nodes):
			zbior = set(range(num_nodes))
			zbior.difference_update(set([node]))
			graph[node] = zbior
		return graph

#n=27770
#m=13
n = 10
m = 4
DPAobject = DPATrial(m)
DPAgraph = make_complete_graph(m)
for item in range(m,n):
	neighbors = DPAobject.run_trial(m)
	DPAgraph[DPAobject._num_nodes - 1] = neighbors

#print DPAgraph

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

normed_graph  = in_degree_distribution_normed(DPAgraph)
x_list = normed_graph.keys()
y_list = normed_graph.values()
plt.loglog(x_list, y_list, 'ro')
plt.title('log-log plot of normalized in-degree distribution\n of the DPA graph ')
plt.xlabel('in-degrees of nodes')
plt.ylabel('number of nodes of the given in-degree')
plt.savefig('q4.png')
plt.show()
