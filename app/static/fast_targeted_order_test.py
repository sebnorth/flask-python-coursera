import unittest

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


EX_GRAPH1 = {0 : set([1,2]),
             1 : set([0,2]),
             2 : set([0,1])}
             
NETWORK_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_rf7.txt"
import alg_application2_provided
CN_graph = alg_application2_provided.load_graph(NETWORK_URL)		
CN_fast_order = fast_targeted_order(CN_graph)	
#EX_fast_order = fast_targeted_order(EX_GRAPH1)

class TestStringMethods(unittest.TestCase):

  def test_upper(self):
      self.assertEqual('foo'.upper(), 'FOO')

  def test_isupper(self):
      self.assertTrue('FOO'.isupper())
      self.assertFalse('Foo'.isupper())

  def test_split(self):
      s = 'hello world'
      self.assertEqual(s.split(), ['hello', 'world'])
      # check that s.split fails when the separator is not a string
      with self.assertRaises(TypeError):
          s.split(2)

if __name__ == '__main__':
    unittest.main()
