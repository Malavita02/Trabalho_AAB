# -*- coding: utf-8 -*-
class Bwt:
    """
        O objetivo desta class é converter repetições em sequências de símbolos repetidos
        Inputs:
            :seq: Sequência 
            :type seq: string
            
    """
    def __init__(self, seq):
        self.seq = seq
        self.check_seqs()
        self.btw = self.build_bwt(seq)
        self.bwt_seq, self.sa = self.sufix_array()

    def check_seqs(self):
         '''
            Verifica se a sequência é uma string
            
        '''
        if type(self.seq) != str:
            raise TypeError("Estas sequencias não são strings.")

    def get_bwt(self):
        '''
            Retorna a sequência BWT
            Returns:
                :return str: Devolve a sequência BWT
                :rtype str: string
        '''
        return self.bwt_seq

    def build_bwt(self, text:str)-> str:
         '''
            Retorna a última coluna da matriz
            Inputs:
                :text: Sequência ou o texto para procurar o padrão
                :type text: string
            Returns:
                :return str: última coluna da matriz
                :rtype str: string
        '''
        perm_ord = sorted([(text[i:] + text[:i], i) for i in range(len(text))])
        return perm_ord

    def sufix_array(self):
        '''
            Retorna a última coluna da matriz
         
        '''
        bwt, suffix_array = zip(*[(s[-1], p) for s, p in self.btw])
        bwt = "".join(bwt)
        return bwt, suffix_array

    def dict_bwt(self, bwt:str)-> dict:
        '''
            Contróis uma tabela com o bwt
            Inputs:
                :bwt: sequencia
                :type bwt: string
            Returns:
                :return tab: dicionário com elementos do bwt
                :rtype tab: dicionario
        '''
        def tabela():
            D = {}
            def _add(x):
                nonlocal D
                idx = D.get(x, 0)
                D[x] = idx + 1
                return x + str(idx)
            return _add
        fun = tabela()
        self.bwt_off = [fun(x) for x in bwt]
        fun = tabela()
        self.ord_off = [fun(x) for x in sorted(bwt)]
        tab = {k: v for k, v in zip(self.bwt_off, self.ord_off)}
        return tab

    def reverse_bwt(self, bwt:str)-> str:
        '''
            Inverte a coluna da matriz para obter a sequência
            Inputs:
                :bwt: Sequência para reverter
                :type bwt: string
            Returns:
                :return str: última coluna da matriz
                :rtype str: string
        '''
        tab = self.dict_bwt(bwt)
        rec = ""
        x = tab["$0"]
        while x != "$0":
            rec += x[0]
            x = tab[x]
        self.dict_bwt = tab
        return rec

    def find_pattern(self, patt:str)-> list:
        '''
            Procura padrão com a bwt
            Inputs:
                :patt: Padrão para procurar 
                :type patt: string
            Returns:
                :return res:lista dos índices do padrão que foi encontrado
                :rtype res: list
        '''
        for i in range(len(patt)-1):
            p = patt[-1-i]
            l = []
            for j in range(len(self.ord_off)):
                if p in self.ord_off[j]: l.append(j)
            t, b = l[0], l[-1]
            l = []
            for j in range(t,b+1):
                if patt[-2-i] in self.bwt_off[j]: l.append(j)
            t, b = int(l[0]), int(l[-1])
        aux = []
        for j in self.bwt_off[t:b+1]:
            aux.append(j)
        res = []
        for i in range(len(self.ord_off)):
            if self.ord_off[i] in aux: res.append(i)
        return res


bwt = Bwt("TAGACAGAGA$")
get_bwt = bwt.get_bwt()
reverse = bwt.reverse_bwt("ACG$GTAAAAC")
print(get_bwt)
print(reverse)
print(bwt.find_pattern("AGA"))
