# -*- coding: utf-8 -*-
import pprint

class Trie:
    """
        Árvores n-árias permitem organizar um padrão ou vários padrões a procurar numa sequência.
        Cada arco é associado a um dos símbolos do alfabeto, sendo que cada arco que sai de um nodo é associado a um símbolo distinto
        Árvore tem uma folha por cada padrão.
        Cada padrão pode ser construído juntando os símbolos da raiz até uma das folhas
        Inputs:
            :seqs: Sequências
            :type seqs: string
    """
    def __init__(self, seqs):
        self.trie = {}
        self.seqs = seqs
        self.check_seqs()
        seqs = seqs.split()
        for seq in seqs:
            self.insert(seq)

    def check_seqs(self):
        '''
        Verifica se a sequência é uma string
        '''
        if type(self.seqs) != str:
            raise TypeError("Estas sequencias não são strings.")


    def print_trie(self):
        '''
        "Imprime" a árvore
        Returns:
            :return str: Devolve a árvore
            :rtype str: str
                
        '''
        trie = pprint.pprint(self.trie, width=1)
        return str(trie)

    def insert(self, seq):
        '''
        Insere a sequência na árvore
        Inputs:
            :seq: Sequência a inserir
            :type seq: string          
        '''
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
                :return boolean: Retorna True se o padrão da sequência é encontrado  nas sequências "disponíveis"
                :rtype boolean: boolean
        '''
        t = self.trie
        for x in seq:
            if x not in t: return False
            t = t[x]
        return "#$#" in t

x = Trie("AAA AAG ACTT")
x.print_trie()
print(x.matches("AAA"))