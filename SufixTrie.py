# -*- coding: utf-8 -*-
class Sufix_trie:
    """
    Esta classe permite fazer um pré-processamento da sequência na qual se quer procurar o padrão (ou padrões)
    """
    def __init__(self, seq):
        n = len(seq)
        self.trie = {}
        for i in range(n+1):
            self.insert(seq[i:n], i)

    def __str__(self):
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
        Esta função procura o nó correspondente ao padrão e se não existir retorna falso
        Inputs:
            :seq: Padrão da sequência
        Returns:
                :return t["$"]: Devolve a posição do nó
        '''
        t = self.trie
        for x in seq:
            if x not in t: return False
            t = t[x]
        return t["$"]
