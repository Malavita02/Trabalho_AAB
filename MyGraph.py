# -*- coding: utf-8 -*-


from collections import defaultdict
import heapq as heap


class MyGraph:
    ''' 
        Classe que constrói grafos e implementa as suas funções
    '''
    def __init__(self, g : dict ={}):
       
        '''
            Construtor que cria a variável
            
            Parameters
            ----------
            :param g: os valores do grafo vão para o dicionário
        
        '''
        self.graph = {}
        
    def create_graph(self, g):
        
         self.graph = g
     
    def print_graph(self):
         ''' 
             Mostra o grafo numa lista de adjacencia e imprime o nó e os seus vizinhos
         '''
         
         for v in self.graph.keys():
             print(v, " -> ", self.graph[v])
        
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

    def length(self):
        ''' 
            Retorna o tamanho do grafo através do tamanho dos nodos e das arestas
        '''
        
        return len(self.get_nodes()), len(self.get_edges())
    

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

    def add_edge(self, v1: str, v2: str,  w : int = None):
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
        
   

    def get_successors(self, v: str) -> list:
        ''' 
            Retorna numa lista o nodo sucessor
            
            Parameters
            ----------
            v: nodo de partida para procura do sucessor
        '''
        return list(self.graph[v])

    def get_predecessors(self, v: str) -> list:
        ''' 
            Retorna numa lista o nodo antecessor
            
            Parameters
            ----------
            v: nodo de partida para procura do antecessor
        '''
        res = []
        for k in self.graph.keys():
            if v in self.graph[k]:
                res.append(k)
        return res

    def get_adjacents(self, v: str)-> list:
        ''' 
            Retorna na lista anterior os nodos adjacentes
            
            Parameters
            ----------
            v: nodo de partida para procura de adjacentes
        '''
        suc = self.get_successors(v)
        pred = self.get_predecessors(v)
        res = pred
        for p in suc:
            if p not in res: res.append(p)
        return res


    def in_degree(self, v: str)-> str:
        ''' 
            Retorna o grau de entrada de um nó: o número de 
            ligações que chegam a esse nó (nº depredecessores)
            
            Parameters
            ----------
            v: nodo para o qual é retornado o grau de entrada
    '''

        return len(self.get_predecessors(v))
    
    def out_degree(self, v: str)-> str:
        ''' 
            Retorna o grau de saída de um nó:
            o número de ligações que saem desse nó (nº de suvessores)
            
            Parameters
            ----------
            v: nodo para o qual é retornado o grau de saída
        '''
        
        return len(self.graph[v])


    def degree(self, v: str)-> str:
        ''' 
            Retorna o grau do nó v (todos os nós adjacentes)
            
            Parameters
            ----------
            v: nodo para o qual é retornado o grau
        '''
        return len(self.get_adjacents(v))
    

    
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
    
    def reachable_with_dist(self, v: str) -> list:
        '''
            Retorna uma lista de nodos atingíveis a partir de v
            com a respetiva distância
            
            Parameters
            ----------
            v: nodo de partida
        '''
        res = []
        l = [(v, 0)]
        while len(l) > 0:
            node, dist = l.pop(0)
            if node != v: res.append((node, dist))
            for elem in self.graph[node]:
                if not is_in_tuple_list(l, elem) and not is_in_tuple_list(res, elem):
                    l.append((elem, dist + 1))
        return res



    def reachable_bfs(self, v: str)-> list:
        '''
            Travessia do grafo em largura começando pelo nó origem, explorando todos sucessores e
            os sucessores destes, até todos os nós atingíveis terem sido explorados, para observar os nós atingíveis

            Parameters
            ----------
            v: nodo de partida
        '''
        l = [v]
        res = []
        while len(l) > 0:
            node = l.pop(0)
            if node != v: res.append(node)
            for elem in self.graph[node]:
                if elem not in res and elem not in l and elem != node:
                    l.append(elem)
        return res

    def reachable_dfs(self, v:str) -> list:
        '''
            Travessia do grafo em profundidade começando pelo nó origem, explorando o 1º sucessor, seguido pelo
            1º sucessor deste até não haver mais sucessores e fazer "backtracking",  para observar os nós atingíveis

            Parameters
            ----------
            v: nodo de partida
        '''
        l = [v]
        res = []
        while len(l) > 0:
            node = l.pop(0)
            if node != v: res.append(node)
            s = 0
            for elem in self.graph[node]:
                if elem not in res and elem not in l:
                    l.insert(s, elem)
                    s += 1
        return res


    def node_has_cycle(self, v: str) -> str:
        '''
            Ciclo (simples) se não tem vértices ou arcos repetidos
            
            Parameters
            ----------
            v: nodo de origem e destino
        '''
        
        l = [v]
        res = False
        visited = [v]
        while len(l) > 0:
            node = l.pop(0)
            for elem in self.graph[node]:
                if elem == v:
                    return True
                elif elem not in visited:
                    l.append(elem)
                    visited.append(elem)
        return res

    def has_cycle(self):
        '''
            Verifica se é ciclo
        '''
        res = False
        for v in self.graph.keys():
            if self.node_has_cycle(v): 
                return True
        return res
    

        
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
    gr = MyGraph()
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
    gr = MyGraph()
    gr.create_graph({'1': {'2': 1, '3': 1}, '2': {'4': 1}, '3': {'5': 1}, '4': {}, '5': {}})
    gr.print_graph()
    print('Nodos', gr.get_nodes())
    print('Arestas', gr.get_edges())
    print()
test1()

def test2():
    print('------------------TESTE 2---------------------')
    print('Novo grafo depois de adicionar nodos e arcos com tamanho:')
    gr = MyGraph()
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
    print('É ciclo:' , gr.has_cycle())
    
    print()
    
    dic_parentes,custo = gr.dijkstra('A')

    algoritmo = find_path(dic_parentes,"D")
    algoritmo.reverse()
    print('Caminho Dijkstra:', algoritmo)
    print("O custo total deste caminho é: " + str(custo.get("D")))
    print()
# teste 3    
    analise = 'B' #input do número do nodo a analisar
    print (f'Vértice sucessor de {analise}:', gr.get_successors(analise))
    print (f'Vértice antecessor: {analise}', gr.get_predecessors(analise))
    print (f'Vértice adjacente {analise}:', gr.get_adjacents(analise))
    print (f'Grau de entrada de {analise}:', gr.in_degree(analise))
    print (f'Grau de saída de {analise}:', gr.out_degree(analise))
    print (f'Grau do nó {analise}:', gr.degree(analise))
    print()
    print()
# teste 4    
    v = 'A' # input do nó em análise
    print(f'Nós atingíveis de {v} em largura (bfs):', gr.reachable_bfs(v))
    print(f'Nós atingíveis de {v} em profundidade (dsf):',gr.reachable_dfs(v))
    print()
# teste 5
    print('Distância:', gr.distance('A','D'))
    print('Distância:', gr.distance('D','C'))
    print()


# teste 7
    a = 'A'
    b = 'C'
    print(f'Nós atingíveis a partir de {a}:', gr.reachable_with_dist(a))
    print(f'Nós atingíveis a partir de {b}: ', gr.reachable_with_dist(b))
    print()

 
test2()  
  

