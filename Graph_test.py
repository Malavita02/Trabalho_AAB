# -*- coding: utf-8 -*-
"""
Created on Wed May 25 20:06:19 2022

@author: carin
"""

# -*- coding: utf-8 -*-

    
import unittest
import Graph

class TestGrafo(unittest.TestCase):
    
    def test_shortest_path(self):
        
        A1=Graph.Graph()
        A1.create_graph({'1': {'2': 1}, '2': {'3': 1}, '3': {'2': 1, '4': 1}, '4': {'2':1}})
        a1 = A1.shortest_path('1', '4')
        self.assertEqual(a1, ['1', '2', '3', '4'], 'Resultado diferente do suposto')
        
    
    def test_distance(self):
        
        D1=Graph.Graph()
        D1.create_graph({'1': {'2': 1}, '2': {'3': 1}, '3': {'2': 1, '4': 1}, '4': {'2':1}})
        d1 = D1.distance('1','3')
        self.assertEqual(d1, 2 , 'Resultado diferente do suposto')

    def test_length(self):
        
        T1=Graph.Graph()
        T1.create_graph({'1': {'2': 1}, '2': {'3': 1}, '3': {'2': 1, '4': 1}, '4': {'2':1}})
        t1 = T1.length()
        self.assertEqual(t1, (4, 5) , 'Resultado diferente do suposto')
    

    def test_get_nodes(self):
        
        GN1=Graph.Graph()
        GN1.create_graph({'1': {'2': 1}, '2': {'3': 1}, '3': {'2': 1, '4': 1}, '4': {'2':1}})
        gn1 = GN1.get_nodes()
        self.assertEqual(gn1, ['1', '2', '3', '4'], 'Resultado diferente do suposto')
        
    
    def test_get_edges(self):
        
        GA1=Graph.Graph()
        GA1.create_graph({'1': {'2': 1}, '2': {'3': 1}, '3': {'2': 1, '4': 1}, '4': {'2':1}})
        a1 = GA1.get_edges()
        self.assertEqual(a1, [('1', '2'), ('2', '3'), ('3', '2'), ('3', '4'), ('4', '2')], 'Resultado diferente do suposto') 
        






    
if __name__ == "__main__":
    unittest.main()