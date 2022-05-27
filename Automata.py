# -*- coding: utf-8 -*-
class Automata:
    """
        Os Autómatos processam uma sequência de símbolos da esquerda para a direita.
        Este pode ser usado para procurar ocorrências do padrão usado para o construir.
        Inputs:
            :pattern: Padrão a procurar
            :type pattern: string
            :alphabet: Alfabeto que o padrão pertence (por omissão "ATCG")
            :type alphabet: string
    """

    def __init__(self, alphabet, pattern):
        self.numstates = len(pattern) + 1
        self.current = 0  # [0, 1, 2, 3, 4, 5]
        self.pattern = pattern
        self.detected = False
        self.alphabet = alphabet
        self.check_pattern_alphabet()

    def check_pattern_alphabet(self):
        if type(self.pattern) != str:
            raise TypeError("Esse padrão não é uma string.")
        if type(self.alphabet) != str:
            raise TypeError("Esse alphabet não é uma string.")
        for p in self.pattern:
            if p not in self.alphabet:
                raise TypeError("Esse padrão não pertence ao alfabeto indicado.")

    def printAutomata(self):
        '''
            Mostra os estados, alfabeto utilizado, o padrão de procura e contrói uma tabela de transição a partir do padrão
        '''
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

    def nextState(self, symbol: str)-> str:
        """
            Verifica o símbolo seguinte. Se o mesmo se encontra no padrão
            Inputs:
                :symbol: Símbolo a procurar o padrão
                :type text: string
      
        """
        if(symbol == self.pattern[self.current]): # Se simbolo é o próximo no padrão
            self.current += 1 # Avançar para o próximo estado
            if(self.current == self.numstates):
                self.detected = True
                # P: AABAA
                # S: AABAABAA
                # D: FFFFTFFT
                self.current = self.patternSubSequence(symbol)
            else:
                self.detected = False
        else: # Caso contrário
            # Verificar se existe uma subsequência no (padrão detectato até agora+simbolo) que faça parte do padrão
            self.current = self.patternSubSequence(symbol)
            self.detected = False

    def patternSubSequence(self, symbol: str)-> int:
        '''
            Função que faz a procura do padrão na sequência 
            Inputs:
                :symbol: Sequência ou o texto para procurar o padrão
                :type symbol: string
            Returns:
                :return int: índice do próximo
                :rtype int: int
            '''
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

    def occurencesPattern(self, text: str)-> list:
        """
        Função que conta as ocorrências do padrão
         Inputs:
             :text: Sequência ou o texto para procurar o padrão
             :type text: string
         Returns:
             :return list: lista com as ocorrências do padrão
             :rtype list: list
        """

        self.current = 0
        res = []
        for symbolIndex in range(len(text)):
         self.nextState(self, text[symbolIndex])
         if(self.detected == True):
             res.append(symbolIndex)
        return res

    def overlap(s1: str, s2: str) -> int:
        """
        Função que dá o comprimento do overlap máximo entre s1 e s2, ou seja, o maior sufixo de s1 que é prefixo de s2
         Inputs:
             :s1: Sequência ou o texto para procurar o padrão
             :type text: string
             :s2: Sequência ou o texto para procurar o padrão
             :type text: string
         Returns:
             :return int: comprimento do overlap máximo
             :rtype int: int
        """
        maxov = min(len(s1), len(s2))
        for i in range(maxov, 0, -1):
            if s1[-i:] == s2[:i]:
                return i
        return 0

automata = Automata("ABC", "AABB")
automata.printAutomata()
