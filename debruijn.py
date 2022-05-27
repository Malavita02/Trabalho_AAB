# -*- coding: utf-8 -*-

from MyGraph import MyGraph

class DeBruijnGraph (MyGraph):
    '''
    Esta classe representa os fragmentos (k-mers) não como nós do grafo mas antes como arcos, sendo os nós sequências 
    de tamanho k-1 correspondendo a prefixos/ sufixos destes fragmentos.
    '''
    
    def __init__(self, frags):
        MyGraph.__init__(self, {})
        self.create_deBruijn_graph(frags)

    def add_edge(self, o, d):
        '''
        Método add_edge redefinido para admitir arcos repetidos
        Inputs:
            :o:
            :d:
        '''
        if o not in self.graph.keys():
            self.add_vertex(o)
        if d not in self.graph.keys():
            self.add_vertex(d)
        self.graph[o].append(d)

    def in_degree(self, v):
        res = 0
        for k in self.graph.keys(): 
            if v in self.graph[k]: 
                res += self.graph[k].count(v)
        return res

    def create_deBruijn_graph(self, frags):
        for seq in frags:
            suf = suffix(seq)
            self.add_vertex(suf)
            pref = prefix(seq)
            self.add_vertex(pref)
            self.add_edge(pref, suf)

    def seq_from_path(self, path):
        seq = path[0]
        for i in range(1,len(path)):
            nxt = path[i]
            seq += nxt[-1]
        return seq 
    
def suffix (seq):
    '''
    Dá o sufixo da sequência
    Inputs:
        :seq: Sequência
        :type seq: str
    Returns:
        :return int: sufixo da sequência
        :rtype int: int
    '''
    return seq[1:]
    
def prefix(seq):
    '''
    Dá o prefixo da sequência
    Inputs:
        :seq: Sequência
        :type seq: str
    Returns:
        :return int: prefixo da sequência
        :rtype int: int
    '''
    return seq[:-1]

def composition(k, seq):
    res = []
    for i in range(len(seq)-k+1):
        res.append(seq[i:i+k])
    res.sort()
    return res



def test1():
    frags = [ "ATA", "ACC", "ATG", "ATT", "CAT", "CAT", "CAT", "CCA", "GCA", "GGC", "TAA", "TCA", "TGG", "TTC", "TTT"]
    dbgr = DeBruijnGraph(frags)
    dbgr.print_graph()
    
    
def test2():
    frags = [ "ATA", "ACC", "ATG", "ATT", "CAT", "CAT", "CAT", "CCA", "GCA", "GGC", "TAA", "TCA", "TGG", "TTC", "TTT"]
    dbgr = DeBruijnGraph(frags)
    dbgr.print_graph()
    print (dbgr.check_nearly_balanced_graph())
    print (dbgr.eulerian_path())


def test3():
    orig_sequence = "ATGCAATGGTCTG"
    frags = composition(3, orig_sequence)
    dbgr = DeBruijnGraph(frags)
    dbgr.print_graph()
    print(dbgr.check_nearly_balanced_graph())
    print(dbgr.eulerian_path())


test1()
print()
test2()
print()
test3()
    
