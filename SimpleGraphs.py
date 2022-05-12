# -*- coding: utf-8 -*-
import Bio.SeqIO as io

# O codigo esta igual ao que se fez na aula
"""
Grafos sem peso
"""
def create_graph():
    return {}

def add_node(graph, node):
    if node not in graph:
        graph[node] = {}

def add_edge(graph, u, v, w=None):
    add_node(graph, u)
    add_node(graph, v)
    graph[u][v] = w

def to_graphviz(g):
    with io.StringIO() as F:
        print("""digraph{
            node[shape = "circle", style = "filled"];
            """, file=F)
        for u in g:
            print(f"{u} -> {v};", file=F)
            for v in g[u]:
                print(f"{u} -> {v};", file=F)
        print("}", file=F)
        return F.getvalue()


"""
Grafos com peso
"""



def create_graph():
    return {}

def add_node(graph, node):
    if node not in graph:
        graph[node] = {}

def add_edge(graph, u, v, w=None):
    add_node(graph, u)
    add_node(graph, v)
    graph[u][v] = w

def to_graphviz(g):
    with io.StringIO() as F:
        print("""digraph{
            node[shape = "circle", style = "filled"];
            """, file=F)
        for u in g:
            print(f"{u} -> {v};", file=F)
            for v in g[u]:
                if g[u][v] is not None:
                    print(f'{u} -> {v}[label = "{g[u][v]}"];', file=F)
                else:
                    print(f"{u} -> {v};", file=F)
        print("}", file=F)
        return F.getvalue()


