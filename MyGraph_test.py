# -*- coding: utf-8 -*-

    
import unittest
import MyGraph

class TestGrafo(unittest.TestCase):
    
    def test_shortest_path(self):
        
        A1=MyGraph.MyGraph({1: [2], 2: [3], 3: [2, 4], 4: [2]})
        a1 = A1.shortest_path(1, 4)
        self.assertEqual(a1, [1, 2, 3, 4], 'Resultado diferente do suposto')
        
    
    def test_distance(self):
        
        D1=MyGraph.MyGraph({1: [2], 2: [3], 3: [2, 4], 4: [2]})
        d1 = D1.distance(1, 3)
        self.assertEqual(d1, 2 , 'Resultado diferente do suposto')

    def test_length(self):
        
        T1=MyGraph.MyGraph({1: [2], 2: [3], 3: [2, 4], 4: [2]})
        t1 = T1.length()
        self.assertEqual(t1, (4, 5) , 'Resultado diferente do suposto')
    
    def test_get_nodes(self):
        
        GN1=MyGraph.MyGraph({1: [2], 2: [3], 3: [2, 4], 4: [2]})
        gn1 = GN1.get_nodes()
        self.assertEqual(gn1, [1, 2, 3, 4], 'Resultado diferente do suposto')
        
    
    def test_get_edges(self):
        
        GA1=MyGraph.MyGraph({1: [2], 2: [3], 3: [2, 4], 4: [2]})
        a1 = GA1.get_edges()
        self.assertEqual(a1, [(1, 2), (2, 3), (3, 2), (3, 4), (4, 2)], 'Resultado diferente do suposto') 
        

    def test_has_cycle(self):
        
        C1=MyGraph.MyGraph({1: [2], 2: [3], 3: [2, 4], 4: [2]})
        c1 = C1.has_cycle()
        self.assertEqual(c1, True, 'Resultado diferente do suposto')

    def test_get_successors(self):
        
        GS1=MyGraph.MyGraph({1: [2], 2: [3], 3: [2, 4], 4: [2]})
        gs1 = GS1.get_successors(2)
        self.assertEqual(gs1, [3], 'Resultado diferente do suposto')
        
    def test_get_predecessors(self):
        
        GA1=MyGraph.MyGraph({1: [2], 2: [3], 3: [2, 4], 4: [2]})
        ga1 = GA1.get_predecessors(3)
        self.assertEqual(ga1, [2], 'Resultado diferente do suposto')
        
        


    def test_in_degree(self):
        
        GE1=MyGraph.MyGraph({1: [2], 2: [3], 3: [2, 4], 4: [2]})
        ge1 = GE1.in_degree(4)
        self.assertEqual(ge1, 1, 'Resultado diferente do suposto')
        
        

    def test_out_degree(self):
        
        GS1=MyGraph.MyGraph({1: [2], 2: [3], 3: [2, 4], 4: [2]})
        gs1 = GS1.out_degree(3)
        self.assertEqual(gs1, 2, 'Resultado diferente do suposto')


    def test_degree(self):
        
        G1=MyGraph.MyGraph({1: [2], 2: [3], 3: [2, 4], 4: [2]})
        g1 = G1.degree(3)
        self.assertEqual(g1, 2, 'Resultado diferente do suposto')
        
   
    def test_reachable_bfs(self):
        
        AB1=MyGraph.MyGraph({1: [2], 2: [3], 3: [2, 4], 4: [2]})
        ab1 = AB1.reachable_bfs(3)
        self.assertEqual(ab1, [2, 4], 'Resultado diferente do suposto')
        
        
    def test_reachable_dfs(self):
        
        AD1=MyGraph.MyGraph({1: [2], 2: [3], 3: [2, 4], 4: [2]})
        ad1 = AD1.reachable_dfs(4)
        self.assertEqual(ad1, [2, 3], 'Resultado diferente do suposto')
   
    def test_reachable_with_dist(self):
        
        AD1=MyGraph.MyGraph({1: [2], 2: [3], 3: [2, 4], 4: [2]})
        ad1 = AD1.reachable_with_dist(1)
        self.assertEqual(ad1, [(2, 1), (3, 2), (4, 3)] , 'Resultado diferente do suposto')


    def test_all_degrees(self):
        
        A1=MyGraph.MyGraph({1:[2], 2:[3], 3:[2,4], 4:[2]})
        a1 = A1.all_degrees()
        self.assertEqual(a1, {1: 1, 2: 3, 3: 2, 4: 2}, 'Resultado diferente do suposto')
        
    def test_highest_degrees(self):
        
        A1=MyGraph.MyGraph({1:[2], 2:[3], 3:[2,4], 4:[2]})
        a1 = A1.highest_degrees()
        self.assertEqual(a1, [2, 3, 4, 1], 'Resultado diferente do suposto')
    
    def test_mean_degree(self):
        
        A1=MyGraph.MyGraph({1:[2], 2:[3], 3:[2,4], 4:[2]})
        a1 = A1.mean_degree()
        self.assertEqual(a1, 2.0, 'Resultado diferente do suposto')
        
    def test_prob_degree(self):
        
        A1=MyGraph.MyGraph({1:[2], 2:[3], 3:[2,4], 4:[2]})
        a1 = A1.prob_degree()
        self.assertEqual(a1, {1: 0.25, 3: 0.25, 2: 0.5}, 'Resultado diferente do suposto')
        
    def test_mean_distances(self):
        
        A1=MyGraph.MyGraph({1:[2], 2:[3], 3:[2,4], 4:[2]})
        a1 = A1.mean_distances()
        self.assertEqual(a1, (1.5555555555555556, 0.75), 'Resultado diferente do suposto')
     
    def test_clustering_coef(self):
        
        A1=MyGraph.MyGraph({1:[2], 2:[3], 3:[2,4], 4:[2]})
        a1 = A1.clustering_coef(2)
        self.assertEqual(a1, 0.3333333333333333 , 'Resultado diferente do suposto')
        
    def test_all_clustering_coefs(self):
        
        A1=MyGraph.MyGraph({1:[2], 2:[3], 3:[2,4], 4:[2]})
        a1 = A1.all_clustering_coefs()
        self.assertEqual(a1, {1: 0.0, 2: 0.3333333333333333, 3: 1.0, 4: 1.0} , 'Resultado diferente do suposto')
    
    def test_mean_clustering_coef(self):
        
        A1=MyGraph.MyGraph({1:[2], 2:[3], 3:[2,4], 4:[2]})
        a1 = A1.mean_clustering_coef()
        self.assertEqual(a1, 0.5833333333333333 , 'Resultado diferente do suposto')
        
    def test_mean_clustering_perdegree(self):
        
        A1=MyGraph.MyGraph({1:[2], 2:[3], 3:[2,4], 4:[2]})
        a1 = A1.mean_clustering_perdegree()
        self.assertEqual(a1,{1: 0.0, 3: 0.3333333333333333, 2: 1.0} , 'Resultado diferente do suposto')
        


    

    
if __name__ == "__main__":
    unittest.main()
