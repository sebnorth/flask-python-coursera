'''
project for module 2
'''

from collections import deque
import alg_application2_provided
import numpy as np


EX_GRAPH1 = {0 : set([1,3,4,5]),
             1 : set([0,2,4]),
             2 : set([1,3,5]),
             3 : set([0,2]),
             4 : set([0,1]),
             5 : set([0,2]),
             6 : set([])}
             
def bfs_visited(ugraph, start_node):
	'''
	code that implements breadth-first search
	'''
	visited = set([])
	kolejka = deque()
	visited.update(set([start_node]))
	kolejka.append(start_node)
	while kolejka:
		item = kolejka.pop()
		for nejbor in ugraph[item]:
			if not nejbor in visited:
				visited.update(set([nejbor]))
				kolejka.append(nejbor)
	return visited			

# print bfs_visited(EX_GRAPH1, 0)

def cc_visited(ugraph):
	'''
	Takes the undirected graph ugraph and returns a list of sets, where each set consists of all the nodes (and nothing else) in a connected component, and there is exactly one set in the list for each connected component in ugraph and nothing else. 
	'''
	remaining_nodes = set(ugraph.keys())
	ccc = list()
	while remaining_nodes:
		node = remaining_nodes.pop()
		skladowa = bfs_visited(ugraph, node)
		ccc.append(skladowa)
		remaining_nodes.difference_update(skladowa)
	return ccc

# print cc_visited(EX_GRAPH1)

def largest_cc_size(ugraph):
	'''
	Takes the undirected graph ugraph and returns the size (an integer) of the largest connected component in ugraph
	'''
	cc_lista = cc_visited(ugraph)
	len_lista = [len(item) for item in cc_lista]
	if len_lista:
		return max(len_lista)
	else:
		return 0	
	

# print largest_cc_size(EX_GRAPH1)

def compute_resilience(ugraph, attack_order):
	'''
	For each node in the list, the function removes the given node and its edges from the graph and then computes the size of the largest connected component for the resulting graph
	'''
	resilience = list()
	graph = ugraph
	resilience.append(largest_cc_size(graph))
	for item in attack_order:
		for nejbor in graph[item]:
			graph[nejbor].difference_update(set([item]))
		try:
			del graph[item]
		except KeyError:
			pass
		resilience.append(largest_cc_size(graph))
	return resilience
	
# print compute_resilience(EX_GRAPH1, [0,1,2,3,4,5,6])	
# print alg_application2_provided.fast_targeted_order(EX_GRAPH1)	
