# -*- coding: utf-8 -*-
class Trie:
    """

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
        t = self.trie
        for x in seq:
            if x not in t: return False
            t = t[x]
        return "#$#" in t