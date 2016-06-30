import random
import numpy as np 
import module2_project
import alg_application2_provided
import time

def make_ER_graph_1(num_nodes, prob):
	'''
	wersja dla grafow nieskierowanych, podwojne losowanie
	'''
	graph = dict()
	if num_nodes <=0 :
		return graph
	else:
		for node_s in range(num_nodes):
			graph[node_s] = set([])
		for node_s in range(num_nodes):
			zbior = set(range(num_nodes))
			zbior.difference_update(set([node_s]))
			for node_f in zbior:
				random_number = random.random()
				if random_number < prob:
					graph[node_s].add(node_f)
					graph[node_f].add(node_s)
		return graph			

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

def make_ER_graph_2(num_nodes, prob):
	'''
	wersja dla grafow nieskierowanych, podwojne losowanie
	'''
	ugraph = make_complete_graph(num_nodes)
	for nodei in range(num_nodes):
		for nodej in range(nodei+1, num_nodes):
			random_number = random.random()
			if random_number >= prob:
					ugraph[nodei].remove(nodej)
					ugraph[nodej].remove(nodei)
	return ugraph				
			

"""
Provided code for application portion of module 2

Helper class for implementing efficient version
of UPA algorithm
"""

import random

class UPATrial:
    """
    Simple class to encapsulate optimizated trials for the UPA algorithm
    
    Maintains a list of node numbers with multiple instance of each number.
    The number of instances of each node number are
    in the same proportion as the desired probabilities
    
    Uses random.choice() to select a node number from this list for each trial.
    """

    def __init__(self, num_nodes):
        """
        Initialize a UPATrial object corresponding to a 
        complete graph with num_nodes nodes
        
        Note the initial list of node numbers has num_nodes copies of
        each node number
        """
        self._num_nodes = num_nodes
        self._node_numbers = [node for node in range(num_nodes) for dummy_idx in range(num_nodes)]


    def run_trial(self, num_nodes):
        """
        Conduct num_nodes trials using by applying random.choice()
        to the list of node numbers
        
        Updates the list of node numbers so that each node number
        appears in correct ratio
        
        Returns:
        Set of nodes
        """
        
        # compute the neighbors for the newly-created node
        new_node_neighbors = set()
        for _ in range(num_nodes):
            new_node_neighbors.add(random.choice(self._node_numbers))
        
        # update the list of node numbers so that each node number 
        # appears in the correct ratio
        self._node_numbers.append(self._num_nodes)
        for dummy_idx in range(len(new_node_neighbors)):
            self._node_numbers.append(self._num_nodes)
        self._node_numbers.extend(list(new_node_neighbors))
        
        #update the number of nodes
        self._num_nodes += 1
        return new_node_neighbors
        
def graph_size(ugraph, num_nodes):
	size = 0
	for node in range(num_nodes):
		size+=len(ugraph[node])
	return size / 2	
		
def random_order(ugraph):
	node_list = ugraph.keys()
	random_list = list()
	while node_list:
		node = random.choice(node_list)
		random_list.append(node)
		node_list.remove(node)
	return random_list	
	

def UPA_generator(m,n):
	UPAobject = UPATrial(m)
	UPAgraph = make_complete_graph(m)
	for item in range(m,n):
		neighbors = UPAobject.run_trial(m)
		UPAgraph[UPAobject._num_nodes - 1] = neighbors
		for node in neighbors:
			UPAgraph[node].add(UPAobject._num_nodes - 1)
	return UPAgraph


NETWORK_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_rf7.txt"

import matplotlib.pyplot as plt



t0 = time.clock()

def Question3():
	wynik = list()
	for step in range(10, 1000, 10):
		start = time.clock()
		UPA_graph = UPA_generator(5,step)
		UPA_fast_order = alg_application2_provided.fast_targeted_order(UPA_graph)
		stop = time.clock()
		wynik.append(stop-start)
	xvals = range(10, 1000, 10)
	yvals1 = wynik
	wynik = list()
	for step in range(10, 1000, 10):
		start = time.clock()
		UPA_graph = UPA_generator(5,step)
		UPA_fast_order = alg_application2_provided.targeted_order(UPA_graph)
		stop = time.clock()
		wynik.append(stop-start)
	xvals = range(10, 1000, 10)
	yvals2 = wynik
	#yvals = [1000*item for item in wynik]
	plt.plot(xvals, yvals1, '-b', label='fast_targeted_order')
	plt.plot(xvals, yvals2, '-r', label='targeted_order')
	plt.legend(loc='upper right')
	plt.title('desktop Python time plotting')  
	plt.xlabel('number of nodes')  
	plt.ylabel('time')  
	plt.show()

Question3()

print time.clock() - t0, "seconds process time"


