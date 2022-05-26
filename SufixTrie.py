# -*- coding: utf-8 -*-
class Sufix_trie:
    """
    Esta classe permite fazer um pré-processamento da sequência na qual se quer procurar o padrão (ou padrões)
    Inputs:
            :seq: Sequência
            :type seqs: string
    """
    def __init__(self, seq):
        n = len(seq)
        self.trie = {}
        self.seq = seq
        self.check_seqs()
        for i in range(n+1):
            self.insert(seq[i:n], i)

    def check_seqs(self):
        '''
        Verifica se a sequência é uma string
        '''
        if type(self.seq) != str:
            raise TypeError("Estas sequencias não são strings.")

    def __str__(self):
        '''
        "Imprime" a árvore
        Returns:
                :return str: Devolve a árvore
                :rtype str: str
        '''
        import pprint
        trie = pprint.pprint(self.trie, width=1)
        return str(trie)

    def insert(self, seq, i):
        t = self.trie
        for x in seq:
            if x not in t:
                t[x] = {}
            t = t[x]
        t["$"] = i

    def matches(self, seq):
        '''
        Esta função procura o nó correspondente ao padrão e se não existir retorna falso, se existir retorna uma lista com is índices
        Inputs:
            :seq: Padrão da sequência
        Returns:
            :return: Devolve a posição do nó
            :rtype list: list
        '''
        t = self.trie
        list = []
        for x in seq:
            if x not in t: return False
            t = t[x]
            list.append(t)
        string = str(list)
        res = ""
        for s in string:
            if s in ["0","1","2","3","4","5","6","7","8","9","$"]:
                res += s
        res = res.strip().split("$")
        sol = []
        for i in res:
            if i != "" and i not in sol:
                sol.append(i)
        sol = [int(i) for i in sol]
        return sol
