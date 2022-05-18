# -*- coding: utf-8 -*-
class Automata:
    
    def __init__(self, alphabet, pattern):
        self.numstates = len(pattern) + 1
        self.current = 0 # [0, 1, 2, 3, 4, 5]
        self.pattern = pattern
        self.detected = False
        self.alphabet = alphabet

    def printAutomata(self):
        print("States: ", self.numstates)
        print("Alphabet: ", self.alphabet)
        print("Pattern: ", self.pattern)
        print("Transition table:")
        # State + Symbol -> State*
        for state in range(self.numstates):
            for symbolIndex in range(len(self.alphabet)):
                nextState = 0
                if(state < len(self.pattern) and self.alphabet[symbolIndex] == self.pattern[state]):
                    nextState = state+1
                detected = state == self.numstates - 1
                print(state, " + ", self.alphabet[symbolIndex], " = ", nextState, " detected: ", detected)

    def nextState(self, symbol):
        if(symbol == self.pattern[self.current]): # Se simbolo é o próximo no padrão
            self.current += 1 # Avançar para o próximo estado
            if(self.current == self.numstates):
                self.detected = True
                # P: AABAA
                # S: AABAABAA
                # D: FFFFTFFT
                self.current = patternSubSequence(symbol)
            else:
                self.detected = False
        else: # Caso contrário
            # Verificar se existe uma subsequência no (padrão detectato até agora+simbolo) que faça parte do padrão
            self.current = patternSubSequence(symbol)
            self.detected = False

    def patternSubSequence(self, symbol):
        # Caso contrário, se o estado atual (string detetada até agora) for substring do padrão,
        # queremos ir para o estado correspondente ao tamanho dessa substring
        sequence = self.pattern[0:self.current] + symbol
        # nextState = overlap(sequence, self.pattern)
        # Sequence: AABBCAABBCC
        # Pattern:       AABBA
        # Percorrer sequence, simbolo a simbolo
        nextState = 0
        sequenceStartIndex = 0
        index = 0
        while(index < (len(sequence) - sequenceStartIndex)):
            if(sequence[sequenceStartIndex + index] != self.pattern[index]):
                sequenceStartIndex += 1
                index = 0
            else:
                index += 1
        if(sequenceStartIndex < len(sequence)):
            nextState = sequenceStartIndex
        return nextState

    def occurencesPattern(self, text):
        self.current = 0
        res = []
        for symbolIndex in range(len(text)):
            self.nextState(self, text[symbolIndex])
            if(self.detected == True):
                res.append(symbolIndex)
        return res

    def overlap(s1, s2):
        maxov = min(len(s1), len(s2))
        for i in range(maxov, 0, -1):
            if s1[-i:] == s2[:i]: return i
        return 0
    
automata = Automata("ABC", "AABB")
automata.printAutomata()
