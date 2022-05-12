# -*- coding: utf-8 -*-

import io
import pprint
import re
import numpy as np

"""
Para desenhar o grafo: Graphviz
com pesos
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


'''
Aula seguinte (7) de Reações!!
Aqui vamos adicionar ao grafo g as reações, metabolitos e respetivas ligações, sendo cada reação a conversão de reagentes a produtos
'''

def separar_metabolitos(exp):
    return [M.strip() for M in re.split(r'\s*\+\s*', exp)]


def create_met_react_graph(ficheiro):
    g = create_graph()
    for reacao in ficheiro:
        R, Eq = reacao.split(':')
        bidirec = '<=>' in Eq
        if bidirec:
            esq, dir = [separar_metabolitos(X) for X in Eq.split('<=>')]
        else:
            esq, dir = [separar_metabolitos(X) for X in Eq.split('=>')]
        # print(R, bidirec, esq, dir)

        for M in esq:
            add_edge(g, M, R)
            if bidirec: add_edge(g, R, M)

        for M in dir:
            add_edge(g, R, M)
            if bidirec: add_edge(g, M, R)
    return g


def is_met(M): return M[:2] == "M_"


def is_react(M): return M[:2] == "R_"


def converte_graph(criterio, g):
    '''
    Associa seja metabolitos ou reações, aos que é possível chegar a partir de cada
    '''
    novo = create_graph()
    for M1 in g:
        if criterio(M1):
            for R in g[M1]:
                for M2 in g[R]:
                    add_edge(novo, M1, M2)
    return novo


def outdeg(g, node):
    '''
    Conta os graus associados a cada nodo -> Ou seja, length do dicionário associado
    '''
    return len(g[node])


def inverse(g):
    '''
    Permite verificar quais reações dão origem aos metabolitos e, por outro lado, quais metabolitos dão origem às reações
    '''
    novo = create_graph()
    for U in g:
        for V in g[U]:
            add_edge(novo, V, U)
    return novo

def alcancaveis(g, M):
    lst = [(M,0)]
    alc = {}
    while lst:
        U, dist = lst[0]
        lst = lst[1:]
        alc[U] = dist
        for V in g[U]:
            if V not in alc:
                S = V, dist + 1
                lst.append(S)
    return alc

def distancias(g):
    return {U : alcancaveis(g, U) for U in g}

def dist_med(distancias):
    return np.mean([distancias[U][V] for U in distancias for V in distancias[U]])