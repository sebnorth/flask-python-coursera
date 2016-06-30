"""
Provided code for Application portion of Module 2
"""

# general imports
import urllib2
import random
import time
import math

# CodeSkulptor import
#import simpleplot
#import codeskulptor
#codeskulptor.set_timeout(60)

# Desktop imports
#import matplotlib.pyplot as plt


############################################
# Provided code

def copy_graph(graph):
    """
    Make a copy of a graph
    """
    new_graph = {}
    for node in graph:
        new_graph[node] = set(graph[node])
    return new_graph

def delete_node(ugraph, node):
    """
    Delete a node from an undirected graph
    """
    neighbors = ugraph[node]
    ugraph.pop(node)
    for neighbor in neighbors:
        ugraph[neighbor].remove(node)
    
def targeted_order(ugraph):
    """
    Compute a targeted attack order consisting
    of nodes of maximal degree
    
    Returns:
    A list of nodes
    """
    # copy the graph
    new_graph = copy_graph(ugraph)
    
    order = []    
    while len(new_graph) > 0:
        max_degree = -1
        for node in new_graph:
            if len(new_graph[node]) > max_degree:
                max_degree = len(new_graph[node])
                max_degree_node = node
        
        neighbors = new_graph[max_degree_node]
        new_graph.pop(max_degree_node)
        for neighbor in neighbors:
            new_graph[neighbor].remove(max_degree_node)

        order.append(max_degree_node)
    return order
    
def fast_targeted_order(ugraph):
    """
    ???
    """
    new_graph = copy_graph(ugraph)
    num = len(new_graph.keys())
    DegreeSets = dict()
    for item in range(num):
        DegreeSets[item] = set([])
    for item_k in new_graph.keys():
        nejbor_num = len(new_graph[item_k])
        DegreeSets[nejbor_num].add(item_k)
    wynik = [0 for _ in range(num)]
    i = 0
    for k in range(num-1,-1,-1):
        while DegreeSets[k]:
            u = DegreeSets[k].pop()
            for nejbor in new_graph[u]:
                d = len(new_graph[nejbor])
                if d:
                    DegreeSets[d].remove(nejbor)
                    DegreeSets[d-1].add(nejbor)
            wynik[i] = u
            i = i + 1
            delete_node(new_graph, u)
    return wynik	
		
				


##########################################################
# Code for loading computer network graph

NETWORK_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_rf7.txt"


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


    
    
    





