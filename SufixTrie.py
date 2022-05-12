# -*- coding: utf-8 -*-
class Sufix_trie:
    """

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
        t = self.trie
        for x in seq:
            if x not in t: return False
            t = t[x]
        return t["$"]