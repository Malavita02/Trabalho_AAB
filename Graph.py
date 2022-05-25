# -*- coding: utf-8 -*-

'''
Definição de grafo

Um grafo G=(V,E) é uma estrutura matemática composta por um conjunto V de vértices ou nós e um conjunto E de pares de nós, designados por ramos, conexões, ligações ou arcos, cada um ligando dois nós.
Estes arcos podem ter uma orientação (pares ordenados) ou não.
Os grafos ordenados têm, portanto, ligações com sentido definido, enquanto que os grafos não orientados têm arcos sem qualquer sentido definido.
Os grafos pesados têm valores associados aos seus arcos.
Podem ser representados computacionalmente por matrizes ou listas de adjacência.

Matrizes de adjacência

As linhas correspondem aos nós origem das ligações.
As colunas correspondem aos nós destino.
Se existe ligação entre nó i e j, então o valor na matriz (M[i][j]) será 1; caso contrário será 0.
Em grafos não orientados, a matriz é simátrica podendo apenas representar-se uma matriz triangular.
No caso de grafos pesados, os pesos nas ligações podem ser representados como valores na matriz.

Listas de adjacência

Apenas se representam as ligações existentes; para cada nó i temos uma lista com arcos originados em i.
Se o grafo é não orientado, poderá haver informação redundante representando-se ambos os sentidos da ligação.
Esta representação pode ser adaptada representando-se cada nó como um objeto e as ligações como listas de referência a objestos desta classe.




'''



from collections import defaultdict
import heapq as heap


class Graph:
    ''' 
        Classe que constrói grafos com custo e implementa as suas funções
    '''
    def __init__(self, g : dict ={}):
       
        '''
            Construtor que cria a variável
            
            Parameters
            ----------
            :param g: os valores do grafo vão para o dicionário
        
        '''
        self.graph = g
        
    def create_graph(self, g):
        
         self.graph = g
     
    def print_graph(self):
         ''' 
             Mostra o grafo numa lista de adjacencia e imprime o nó e os seus vizinhos
         '''
         
         for v in self.graph.keys():
             print(v, " -> ", self.graph[v])

    def length(self):
        ''' 
            Retorna o tamanho do grafo através do tamanho dos nodos e das arestas
        '''
        return len(self.get_nodes()), len(self.get_edges())
        
    def get_nodes(self):
        ''' 
            Retorna, numa lista, os nodos que estão no grafo 
        '''
        
        return list(self.graph.keys())

    def get_edges(self):
        '''
            Retorna as arestas (linhas) do grafo como uma lista de tuplos 
            A  lista de tuplos tem 2 argumentos: origem , destino
        '''
        
        edges = []
        for v in self.graph.keys():
            for d in self.graph[v]:
                edges.append((v, d))
        return edges

    
    def add_vertex(self, v: str):
        ''' 
            Adiciona nodo v ao grafo
            
            Parameters
            ----------
            v: nodo adicionado
        '''
        
        if v in self.graph:
            pass
        else:
            self.graph[v] = {}

    def add_edge(self, v1: str, v2: str, w : int = None):
        ''' 
            Adiciona o arco (v1,v2) ao grafo e peso w
            
            Parameters
            ----------
            v1: arco adicionado
            v2: arco adicionado
        '''
        if v1 not in self.graph:
            print("O nodo", v1, " não existe")
            return
        
        if v2 not in self.graph:
            print("O nodo ", v2, " não existe")
            return

        self.graph[v1][v2] = w  #custo

    
 # aula grafos  
 
    def distance(self, s: str, d: str)-> int:
        ''' 
            Distância entre dois nós dada pelo comprimento 
            do caminho mais curto entre os mesmos
            
            Parameters
            ----------
            s: nodo origem
            d: nodo destino
        '''
        if s == d: 
            return 0
        l = [(s, 0)]
        visited = [s]
        while len(l) > 0:
            node, dist = l.pop(0)
            for elem in self.graph[node]:
                if elem == d:
                    return dist + 1
                elif elem not in visited:
                    l.append((elem, dist + 1))
                    visited.append(elem)
        return None

    def shortest_path(self, s: str, d: str) -> list:
        '''
            Caminho mais curto entre dois nós caminho onde o comprimento (nº de nós) é o menor 
            entre todos os caminhos possíveis entre eles
            
            Parameters
            ----------
            s: nodo origem
            d: nodo destino
        '''
        
        if s == d: 
            return 0 # se o nó for o mesmo não há distância entre eles
        l = [(s, [])]
        visited = [s]
        while len(l) > 0:
            node, preds = l.pop(0)
            for elem in self.graph[node]:
                if elem == d:
                    return preds + [node, elem]
                elif elem not in visited:
                    l.append((elem, preds + [node]))
                    visited.append(elem)
        return None
    
    def dijkstra(self, orig: str) -> list:
        '''
            Caminho mais curto entre dois nós caminho onde o comprimento (nº de nós) é o menor 
            entre todos os caminhos possíveis entre eles pelo algoritmo Dijkstra
            
            Parameters
            ----------
            origem: nodo origem
            
        '''
        visited = set()
        dic_parents = {}
        result = []
        cost= defaultdict(lambda: float('inf'))
        cost[orig] = 0
        heap.heappush(result, (0, orig))
        
        while result:

            i , node = heap.heappop(result)
            visited.add(node)
            
            for adjacent_node, w in self.graph[node].items():
                if adjacent_node in visited:	continue
                
                new_cost = cost[node] + w
                if cost[adjacent_node] > new_cost:
                    dic_parents[adjacent_node] = node
                    cost[adjacent_node] = new_cost
                    heap.heappush(result, (new_cost, adjacent_node))

        return dic_parents, cost
    

    

#### FUNÇÕES AUXILIARES

def is_in_tuple_list(tl: str, val: str):
    '''
        Verificar se é tuplo
        
        Parameters
        ----------
        tl: string
        val: string
    '''
    res = False
    for (x, y) in tl:
        if val == x: return True
    return res

def find_path(parents: str, dest : str)-> list:
    '''
        Função auxiliar para encontrar caminho entre nodos
        
        Parameters
        ----------
        parentes: nodos próximos
        destino: nodo de destino
    '''
    lista = []
    lista.append(dest)
    if parents[dest] in parents.keys():
        lista = find(parents,parents[dest],lista)
    else:
        lista.append(parents[dest])
    return lista

def find(parents: str, dest : str, lista: list)-> list:
    '''
        Função auxiliar para encontrar caminho entre nodos
        
        Parameters
        ----------
        parentes: nodos próximos
        destino: nodo de destino
        lista: lista de nodos de destino ao longo do trajeto
    '''
    lista.append(dest)
    if parents[dest] in parents.keys():
        lista = find(parents,parents[dest],lista)
    else:
        lista.append(parents[dest])
    return lista




##### TESTES

def test():
    print('------------------TESTE 0---------------------')
    print('Mostrar o grafo:')
    gr = Graph()
    gr.create_graph({'1': {'2': 1}, '2': {'3': 1}, '3': {'2': 1, '4': 1}, '4': {'2':1}})
    gr.print_graph()
    print('CAMINHO:' , gr.shortest_path('1', '4'))
    print()
   
    x = dic_parentes,custo = gr.dijkstra('1')
    print('dijkstra:', x)
    algoritmo = find_path(dic_parentes,'3')
    algoritmo.reverse()
    print('Caminho Dijkstra:', algoritmo)
    print("O custo total deste caminho é: " + str(custo.get('3')))
    print()

    print('Tamanho (nodos, arcos):',gr.length())
    
    
    print()
    
test()

def test1():
    print('------------------TESTE 1---------------------')
    print('Dar nodos e arestas do grafo')
    gr = Graph()
    gr.create_graph({'1': {'2': 1, '3': 1}, '2': {'4': 1}, '3': {'5': 1}, '4': {}, '5': {}})
    gr.print_graph()
    print('Nodos', gr.get_nodes())
    print('Arestas', gr.get_edges())
    print()
test1()

def test2():
    print('------------------TESTE 2---------------------')
    print('Novo grafo depois de adicionar nodos e arcos com tamanho:')
    gr = Graph()
    gr.add_vertex('A')  
    gr.add_vertex('B')
    gr.add_vertex('C')
    gr.add_vertex('D')
    gr.add_edge('A','B', 7)
    gr.add_edge('B','C', 2)
    gr.add_edge('C','B', 8)
    gr.add_edge('C','D', 12)
    gr.add_edge('D','B', 6)
    gr.add_edge('D', 'A', 4)
    gr.add_edge('B','D', 15)
    gr.print_graph()
    print()
    print('Nodos', gr.get_nodes())
    print('Arestas', gr.get_edges())
    print()
    print('Caminho mais curto:', gr.shortest_path('A','C'))
    print('Distância:',gr.distance('A','D'))

    print()
    
    dic_parentes,custo = gr.dijkstra('A')

    algoritmo = find_path(dic_parentes,"D")
    algoritmo.reverse()
    print('Caminho Dijkstra:', algoritmo)
    print("O custo total deste caminho é: " + str(custo.get("D")))
    print()


    print('Distância:', gr.distance('A','D'))
    print('Distância:', gr.distance('D','C'))
    print()


 
test2()  





