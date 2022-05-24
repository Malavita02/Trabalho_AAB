# -*- coding: utf-8 -*-
class Bwt:
    """
        O objetivo desta class é converter repetições em sequências de símbolos repetidos
    """
    def __init__(self, seq):
        self.seq = seq
        self.check_seqs()
        self.btw = self.build_bwt(seq)
        self.bwt_seq, self.sa = self.sufix_array()

    def check_seqs(self):
        if type(self.seq) != str:
            raise TypeError("Estas sequencias não são strings.")

    def get_bwt(self):
        '''
            Retorna a última coluna da matriz
            :param seq: Sequência
            :return self.bwt_seq: Retorna a sequencia BWT
        '''
        return self.bwt_seq

    def build_bwt(self, text):
        perm_ord = sorted([(text[i:] + text[:i], i) for i in range(len(text))])
        return perm_ord

    def sufix_array(self):
        bwt, suffix_array = zip(*[(s[-1], p) for s, p in self.btw])
        bwt = "".join(bwt)
        return bwt, suffix_array

    def dict_bwt(self, bwt):
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

    def reverse_bwt(self, bwt):
        tab = self.dict_bwt(bwt)
        rec = ""
        x = tab["$0"]
        while x != "$0":
            rec += x[0]
            x = tab[x]
        self.dict_bwt = tab
        return rec

    def find_pattern(self, patt):
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
