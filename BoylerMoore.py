# -*- coding: utf-8 -*-
class BoyerMoore:
    '''
        O objetivo desta class é encontrar onde o pattern se repete numa determinada sequência/texto.
        A função contrutora recebe o padrão e o alfabeto a que o mesmo pertence.
        Inputs:
            :pattern: Padrão a procurar
            :type pattern: string
            :alphabet: Alfabeto que o padrão pertence (por omissão "ATCG")
            :type alphabet: string
    '''
    def __init__(self, pattern: str, alphabet = "ATCG") -> str:
        self.pattern = pattern
        self.alphabet = alphabet
        if self.pattern not in alphabet:
            raise TypeError("Esse padrão não pertence ao alfabeto indicado.")
        self.preprocess()

    def preprocess(self):
        self.process_bad_character_rule()
        self.process_good_suffix_rule()

    def process_bad_character_rule(self):
        self.occurrences = {}
        for s in self.alphabet:
            self.occurrences[s] = -1
        for j in range(len(self.pattern)): # AATTTCCG occ['A'] = 1, occ['T'] = 4, occ['C'] = 6, occ['G'] = 7
            self.occurrences[self.pattern[j]] = j
            
     def process_good_suffix_rule(self):
        self.f = [0 for n in range(len(self.pattern) + 1)]
        self.s = [0 for n in range(len(self.pattern) + 1)]
        i = len(self.pattern)
        j = len(self.pattern) + 1
        self.f[i] = j
        while i > 0:
            while j <= len(self.pattern) and self.pattern[i - 1] != self.pattern[j - 1]:
                if self.s[j] == 0:
                    self.s[j] = j - i
                j = self.f[j]
            i = i - 1
            j = j - 1
            self.f[i] = j
        j = self.f[0]
        for i in range(len(self.pattern)):
            if self.s[i] == 0:
                self.s[i] = j
            if i == j:
                j = self.f[j]
                
     def search_pattern(self, text:str) -> str:
        '''
            Recebe a sequência ou o texto onde se pertende encontrar o padrão e devolve uma lista com os indices onde se repete o padrão
            Inputs:
                :text: Sequência ou o texto para procurar o padrão
                :type text: string
            Returns:
                :return list: Lista com os indices onde o padrão foi reconhecido
                :rtype list: list
            '''
        res = []
        i = 0
        while i <= len(text) - len(self.pattern):
            j = len(self.pattern) - 1
            while j >= 0 and self.pattern[j] == text[i + j]:
                j -= 1
            if j < 0:
                res.append(i)
                i += self.s[0]
            else:
                c = text[i + j]
                i += max(self.s[j + 1], j - self.occurrences[c])
        return res
