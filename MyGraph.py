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
    
# aula redes biológicas    
    def all_degrees(self, deg_type="inout") -> dict:
        ''' 
            Calcula o grau (de um determinado tipo) para todos os nós.
            Parameters
            ----------
            deg_type: pode ser "in", "out" ou "inout"
        '''
        degs = {}
        for v in self.graph.keys():
            if deg_type == "out" or deg_type == "inout":
                degs[v] = len(self.graph[v])
            else:
                degs[v] = 0
        if deg_type == "in" or deg_type == "inout":
            for v in self.graph.keys():
                for d in self.graph[v]:
                    if deg_type == "in" or v not in self.graph[d]:
                        degs[d] = degs[d] + 1
        return degs

    def highest_degrees(self, all_deg=None, deg_type="inout", top: str =10)-> list:
        ''' 
            Calcula o grau mais elevado.
            Parameters
            ----------
            deg_type: pode ser "in", "out" ou "inout"
            all_deg: todos os graus
            top: str do top 10 dos maiores
        '''
        if all_deg is None:
            all_deg = self.all_degrees(deg_type)
        ord_deg = sorted(list(all_deg.items()), key=lambda x: x[1], reverse=True)
        return list(map(lambda x: x[0], ord_deg[:top]))

 

    def mean_degree(self, deg_type="inout")-> str:
        ''' 
            Calcula o grau médio
            Parameters
            ----------
            deg_type: pode ser "in", "out" ou "inout"
        '''
        degs = self.all_degrees(deg_type)
        return sum(degs.values()) / float(len(degs))


    def prob_degree(self, deg_type="inout"):
        ''' 
            Calcula a probabilidade do grau
            Parameters
            ----------
            deg_type: pode ser "in", "out" ou "inout"
        '''
        degs = self.all_degrees(deg_type)
        res = {}
        for k in degs.keys():
            if degs[k] in res.keys():
                res[degs[k]] += 1
            else:
                res[degs[k]] = 1
        for k in res.keys():
            res[k] /= float(len(degs))
        return res
    
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
    
 #aula redes biológicas   
    def mean_distances(self):
        ''' 
            Calcula a distância média
            Parameters
            ----------
        '''
        tot = 0
        num_reachable = 0
        for k in self.graph.keys():
            distsk = self.reachable_with_dist(k)
            for _, dist in distsk:
                tot += dist
            num_reachable += len(distsk)
        meandist = float(tot) / num_reachable
        n = len(self.get_nodes())
        return meandist, float(num_reachable) / ((n - 1) * n)

    
    
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

    def has_cycle(self)-> str:
        '''
            Verifica se é ciclo
        '''
        res = False
        for v in self.graph.keys():
            if self.node_has_cycle(v): 
                return True
        return res
    
# aula redes biológicas

    def clustering_coef(self, v:str)-> str:
        '''
           Coeficientes do Clustering
            
            Parameters
            ----------
            v: nodo 
        '''
        adjs = self.get_adjacents(v)
        if len(adjs) <= 1: return 0.0
        ligs = 0
        for i in adjs:
            for j in adjs:
                if i != j:
                    if j in self.graph[i] or i in self.graph[j]:
                        ligs = ligs + 1
        return float(ligs) / (len(adjs) * (len(adjs) - 1))

    def all_clustering_coefs(self)-> dict:
        '''
            Calcula todos os coeficientes
            
            Parameters
            ----------
        
        '''
        ccs = {}
        for k in self.graph.keys():
            ccs[k] = self.clustering_coef(k)
        return ccs

    def mean_clustering_coef(self) -> str:
        '''
            Média global dos coeficientes na rede
            
            Parameters
            ----------
          
        '''
        ccs = self.all_clustering_coefs()
        return sum(ccs.values()) / float(len(ccs))

    def mean_clustering_perdegree(self, deg_type="inout"):
        '''
            Calcula valores para C(k) para todos os nós
            Parameters
            ----------
            deg_type: pode ser "in", "out" ou "inout"
        '''
        degs = self.all_degrees(deg_type)
        ccs = self.all_clustering_coefs()
        degs_k = {}
        for k in degs.keys():
            if degs[k] in degs_k.keys():
                degs_k[degs[k]].append(k)
            else:
                degs_k[degs[k]] = [k]
        ck = {}
        for k in degs_k.keys():
            tot = 0
            for v in degs_k[k]: tot += ccs[v]
            ck[k] = float(tot) / len(degs_k[k])
        return ck

# aula garfos e sequenciação de genomas

    def check_if_valid_path(self, p:list)-> str:
        '''
            Verifica se o caminho é válido
            
            Parameters
            ----------
            p: caminho
        '''
        if p[0] not in self.graph.keys(): return False
        for i in range(1, len(p)):
            if p[i] not in self.graph.keys() or p[i] not in self.graph[p[i - 1]]:
                return False
        return True

    def check_if_hamiltonian_path(self, p: list)-> str:
        '''
            Verifica se o caminho é Hamiltoniano
            
            Parameters
            ----------
            p: caminho
        '''
        if not self.check_if_valid_path(p): return False
        to_visit = list(self.get_nodes())
        if len(p) != len(to_visit): return False
        for i in range(len(p)):
            if p[i] in to_visit:
                to_visit.remove(p[i])
            else:
                return False
        if not to_visit:
            return True
        else:
            return False

    def search_hamiltonian_path(self):
        '''
            Procura caminhos Hamiltonianos
            
            Parameters
            ----------
            p: caminho
        '''
        for ke in self.graph.keys():
            p = self.search_hamiltonian_path_from_node(ke)
            if p != None:
                return p
        return None

    def search_hamiltonian_path_from_node(self, start: str)-> list:
        '''
            Procura exaustiva pelo caminho Hamiltoniano
            
            Parameters
            ----------
            start: nodo origem
        '''
        current = start
        visited = {start: 0}
        path = [start]
        while len(path) < len(self.get_nodes()):
            nxt_index = visited[current]
            if len(self.graph[current]) > nxt_index:
                nxtnode = self.graph[current][nxt_index]
                visited[current] += 1
                if nxtnode not in path:
                    path.append(nxtnode)
                    visited[nxtnode] = 0
                    current = nxtnode
            else:
                if len(path) > 1:
                    rmvnode = path.pop()
                    del visited[rmvnode]
                    current = path[-1]
                else:
                    return None
        return path
    
# ultima aula

    def eulerian_cycle(self)->list:
        '''
            Implementa o Ciclo Euleriano
            
            Parameters
            ----------
        '''
        if not self.is_connected() or not self.check_balanced_graph(): return None
        edges_visit = list(self.get_edges())
        res = []
        while edges_visit:
            pair = edges_visit[0]
            i = 1
            if res != []:
                while pair[0] not in res:
                    pair = edges_visit[i]
                    i = i + 1
            edges_visit.remove(pair)
            start, nxt = pair
            cycle = [start, nxt]
            while nxt != start:
                for suc in self.graph[nxt]:
                    if (nxt, suc) in edges_visit:
                        pair = (nxt, suc)
                        nxt = suc
                        cycle.append(nxt)
                        edges_visit.remove(pair)
            if not res:
                res = cycle
            else:
                pos = res.index(cycle[0])
                for i in range(len(cycle) - 1):
                    res.insert(pos + i + 1, cycle[i + 1])
        return res

    def check_balanced_node(self, node: str)-> str:
        '''
            Verifica se o nodo é balanceado
            
            Parameters
            ----------
            start: nodo origem
        '''
        return self.in_degree(node) == self.out_degree(node)

    def check_balanced_graph(self)-> str:
        '''
            Verifica se o grafo é balanceado
            
            Parameters
            ----------
        '''
        for n in self.graph.keys():
            if not self.check_balanced_node(n): return False
        return True
    
    def check_nearly_balanced_graph(self)-> str:
        '''
            Verifica se o grafo é semibalanceado
            
            Parameters
            ----------
           
        '''
        res = None, None
        for n in self.graph.keys():
            indeg = self.in_degree(n)
            outdeg = self.out_degree(n)
            if indeg - outdeg == 1 and res[1] is None:
                res = res[0], n
            elif indeg - outdeg == -1 and res[0] is None:
                res = n, res[1]
            elif indeg == outdeg:
                pass
            else:
                return None, None
        return res
    
    def is_connected(self)-> str:
        '''
            Verifica se o é atingível em largura
            
            Parameters
            ----------
           
        '''
        total = len(self.graph.keys()) - 1
        for v in self.graph.keys():
            reachable_v = self.reachable_bfs(v)
            if (len(reachable_v) < total): return False
        return True

    def eulerian_path(self):
        '''
            Retorna caminho Euleriano (se existir)
            
            Parameters
            ----------
           
        '''
        unb = self.check_nearly_balanced_graph()
        if unb[0] is None or unb[1] is None: return None
        self.graph[unb[1]].append(unb[0])
        cycle = self.eulerian_cycle()
        for i in range(len(cycle) - 1):
            if cycle[i] == unb[1] and cycle[i + 1] == unb[0]:
                break
        path = cycle[i + 1:] + cycle[1:i + 1]
        return path
    
    
    
    

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
  









