# -*- coding: utf-8 -*-
class Trie:
    """
    Árvores n-árias permitem organizar um padrão ou vários padrões a procurar numa sequência. 
    Cada arco é associado a um dos símbolos do alfabeto, sendo que cada arco que sai de um nodo é associado a um símbolo distinto
    Árvore tem uma folha por cada padrão.
    Cada padrão pode ser construído juntando os símbolos da raiz até uma das folhas
    """
    def __init__(self, seqs):
        self.trie = {}
        seqs = seqs.split()
        for seq in seqs:
            self.insert(seq)

    def __str__(self):
        import pprint
        trie = pprint.pprint(self.trie, width=1)
        return str(trie)

    def insert(self, seq):
        t = self.trie
        for x in seq:
            if x not in t:
                t[x] = {}
            t = t[x]
        t["#$#"] = 0

    def matches(self, seq):
        '''
        Esta função procura a ocorrência de um padrão como prefixo de uma sequência
        Inputs:
            :seq: Padrão da sequência
         # -*- coding: utf-8 -*-
class Trie:
    """
    Árvores n-árias permitem organizar um padrão ou vários padrões a procurar numa sequência. 
    Cada arco é associado a um dos símbolos do alfabeto, sendo que cada arco que sai de um nodo é associado a um símbolo distinto
    Árvore tem uma folha por cada padrão.
    Cada padrão pode ser construído juntando os símbolos da raiz até uma das folhas
    """
    def __init__(self, seqs):
        self.trie = {}
        seqs = seqs.split()
        for seq in seqs:
            self.insert(seq)

    def __str__(self):
        import pprint
        trie = pprint.pprint(self.trie, width=1)
        return str(trie)

    def insert(self, seq):
        t = self.trie
        for x in seq:
            if x not in t:
                t[x] = {}
            t = t[x]
        t["#$#"] = 0

    def matches(self, seq):
        '''
        Esta função procura a ocorrência de um padrão como prefixo de uma sequência
        Inputs:
            :seq: Padrão da sequência
        Returns:
            :return "#$#" in t: Retorna True se o padrão da sequência é encontrado  nas sequências "disponíveis"
        '''
        t = self.trie
        for x in seq:
            if x not in t: return False
            t = t[x]
        return "#$#" in t
        '''
        t = self.trie
        for x in seq:
            if x not in t: return False
            t = t[x]
        return "#$#" in t
