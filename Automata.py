# -*- coding: utf-8 -*-
class Automata:
    """
    Falta terminar esta igual ao que o prof deu
    """
    def __init__(self, alphabet, pattern):
        self.numstates = len(pattern) + 1
        self.alphabet = alphabet
        self.transitionTable = {}
        self.buildTransitionTable(pattern)

    def buildTransitionTable(self, pattern):
        for q in range(self.numstates):
            for a in self.alphabet:
                pass
        # ...

    def printAutomata(self):
        print("States: ", self.numstates)
        print("Alphabet: ", self.alphabet)
        print("Transition table:")
        for k in self.transitionTable.keys():
            print(k[0], ",", k[1], " -> ", self.transitionTable[k])

    def nextState(self, current, symbol):
        pass
    # return ...

    def applySeq(self, seq):
        q = 0
        res = [q]
        # ...
        return res

    def occurencesPattern(self, text):
        q = 0
        res = []
        # ....
        return res


def overlap(s1, s2):
    maxov = min(len(s1), len(s2))
    for i in range(maxov, 0, -1):
        if s1[-i:] == s2[:i]: return i
    return 0