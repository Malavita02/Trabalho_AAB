# -*- coding: utf-8 -*-


import unittest
import Grafo

class TestGrafo(unittest.TestCase):
    
    def test_caminho_mais_curto(self):
        
        A1=Grafo.MyGraph()
        A1.create_graph({'1': {'2': 1}, '2': {'3': 1}, '3': {'2': 1, '4': 1}, '4': {'2':1}})
        a1 = A1.caminho_mais_curto('1', '4')
        self.assertEqual(a1, ['1', '2', '3', '4'], 'Resultado diferente do suposto')
        
    
    def test_distancia(self):
        
        D1=Grafo.MyGraph()
        D1.create_graph({'1': {'2': 1}, '2': {'3': 1}, '3': {'2': 1, '4': 1}, '4': {'2':1}})
        d1 = D1.distancia('1','3')
        self.assertEqual(d1, 2 , 'Resultado diferente do suposto')
        
        
    def test_tamanho(self):
        
        T1=Grafo.MyGraph()
        T1.create_graph({'1': {'2': 1}, '2': {'3': 1}, '3': {'2': 1, '4': 1}, '4': {'2':1}})
        t1 = T1.tamanho()
        self.assertEqual(t1, (4, 5) , 'Resultado diferente do suposto')
   
    
    def test_get_nodos(self):
        
        GN1=Grafo.MyGraph()
        GN1.create_graph({'1': {'2': 1}, '2': {'3': 1}, '3': {'2': 1, '4': 1}, '4': {'2':1}})
        gn1 = GN1.get_nodos()
        self.assertEqual(gn1, ['1', '2', '3', '4'], 'Resultado diferente do suposto')
        
    
    def test_get_arcos(self):
        
        GA1=Grafo.MyGraph()
        GA1.create_graph({'1': {'2': 1}, '2': {'3': 1}, '3': {'2': 1, '4': 1}, '4': {'2':1}})
        a1 = GA1.get_arcos()
        self.assertEqual(a1, [('1', '2'), ('2', '3'), ('3', '2'), ('3', '4'), ('4', '2')], 'Resultado diferente do suposto') 
        

    def test_ciclo(self):
        
        C1=Grafo.MyGraph()
        C1.create_graph({'1': {'2': 1}, '2': {'3': 1}, '3': {'2': 1, '4': 1}, '4': {'2':1}})
        c1 = C1.ciclo()
        self.assertEqual(c1, True, 'Resultado diferente do suposto')

    def test_grau_sucessor(self):
        
        GS1=Grafo.MyGraph()
        GS1.create_graph({'1': {'2': 1}, '2': {'3': 1}, '3': {'2': 1, '4': 1}, '4': {'2':1}})
        gs1 = GS1.get_sucessor('2')
        self.assertEqual(gs1, ['3'], 'Resultado diferente do suposto')
        
    def test_grau_antecessor(self):
        
        GA1=Grafo.MyGraph()
        GA1.create_graph({'1': {'2': 1}, '2': {'3': 1}, '3': {'2': 1, '4': 1}, '4': {'2':1}})
        ga1 = GA1.get_antecessor('3')
        self.assertEqual(ga1, ['2'], 'Resultado diferente do suposto')
        
        
    def test_grau_adjacente(self):
        
        GAD1=Grafo.MyGraph()
        GAD1.create_graph({'1': {'2': 1}, '2': {'3': 1}, '3': {'2': 1, '4': 1}, '4': {'2':1}})
        gad1 = GAD1.get_adjacente('3')
        self.assertEqual(gad1, ['2', '4'], 'Resultado diferente do suposto')


    def test_grau_entrada(self):
        
        GE1=Grafo.MyGraph()
        GE1.create_graph({'1': {'2': 1}, '2': {'3': 1}, '3': {'2': 1, '4': 1}, '4': {'2':1}})
        ge1 = GE1.grau_entrada('4')
        self.assertEqual(ge1, 1, 'Resultado diferente do suposto')
        
        

    def test_grau_saida(self):
        
        GS1=Grafo.MyGraph()
        GS1.create_graph({'1': {'2': 1}, '2': {'3': 1}, '3': {'2': 1, '4': 1}, '4': {'2':1}})
        gs1 = GS1.grau_saida('3')
        self.assertEqual(gs1, 2, 'Resultado diferente do suposto')


    def test_grau(self):
        
        G1=Grafo.MyGraph()
        G1.create_graph({'1': {'2': 1}, '2': {'3': 1}, '3': {'2': 1, '4': 1}, '4': {'2':1}})
        g1 = G1.grau('3')
        self.assertEqual(g1, 2, 'Resultado diferente do suposto')
        
   
    def test_atingiveis_bfs(self):
        
        AB1=Grafo.MyGraph()
        AB1.create_graph({'1': {'2': 1}, '2': {'3': 1}, '3': {'2': 1, '4': 1}, '4': {'2':1}})
        ab1 = AB1.atingiveis_bfs('3')
        self.assertEqual(ab1, ['2', '4'], 'Resultado diferente do suposto')
        
        
    def test_atingiveis_dfs(self):
        
        AD1=Grafo.MyGraph()
        AD1.create_graph({'1': {'2': 1}, '2': {'3': 1}, '3': {'2': 1, '4': 1}, '4': {'2':1}})
        ad1 = AD1.atingiveis_dfs('4')
        self.assertEqual(ad1, ['2', '3'], 'Resultado diferente do suposto')
   
    def test_atingiveis_distancia(self):
        
        AD1=Grafo.MyGraph()
        AD1.create_graph({'1': {'2': 1}, '2': {'3': 1}, '3': {'2': 1, '4': 1}, '4': {'2':1}})
        ad1 = AD1.atingiveis_distancia('1')
        self.assertEqual(ad1, [('2', 1), ('3', 2), ('4', 3)] , 'Resultado diferente do suposto')

    
if __name__ == "__main__":
    unittest.main()
    
