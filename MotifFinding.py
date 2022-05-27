# -*- coding: utf-8 -*-

from MySeq import MySeq
from MyMotifs import MyMotifs
import random

class MotifFinding:
    '''
       Esta classe implementa algoritmos de procura de motifs conservados, dados conjuntos de sequências
       Inputs:
           :size: Tamanho
           :type size: int
           :seqs: Sequências a utilizar
           :type seqs: string
   '''
    def __init__(self, size = 8, seqs: str = None):
        self.motifSize = size
        if (seqs != None):
            self.seqs = seqs
            self.alphabet = seqs[0].alfabeto()
        else:
            self.seqs = []
                    
    def __len__ (self)-> int:
        '''
            Retorna o tamanho das sequências
            
            '''
        return len(self.seqs)
    
    def __getitem__(self, n:str)-> str:
        '''
            Procura um item  na sequência
            Inputs:
                :n: Sequência ou o texto para procurar o padrão
                :type n: string
            Returns:
                :return list: índice onde ocorre
                :type list: string
            '''
        return self.seqs[n]
    
    def seqSize (self, i: str)-> str:
        '''
            Retorna o tamanho da sequência
            Inputs:
                :i: Sequência ou o texto para procurar o padrão
                :type i: string
            Returns:
                :return list: índice onde ocorre
                :type list: string
            '''
        return len(self.seqs[i])
    
    def readFile(self, fic:str, t:str):
        '''
            Procura um item  na sequência
            Inputs:
                :fic: ficheiro a analisar
                :type fic: string
                :t: tipo
                :type t: string
            '''
        for s in open(fic, "r"):
            self.seqs.append(MySeq(s.strip().upper(),t))
        self.alphabet = self.seqs[0].alfabeto()
        
        
    def createMotifFromIndexes(self, indexes)-> list:
        '''
            Criação de um motif a partir dos índices
            Inputs:
                :indexes: ficheiro a analisar
                :type indexes: string
            Returns:
                :return list: lista do motif
                :type list: list
            '''
        pseqs = []
        for i,ind in enumerate(indexes):
            pseqs.append( MySeq(self.seqs[i][ind:(ind+self.motifSize)], self.seqs[i].tipo) )
        return MyMotifs(pseqs)
        
        
    # SCORES

    def score(self, s:str)-> int:
        '''
            Devolve o score
            Inputs:
                :s: indices
                :type s: str
            Returns:
                :return score: score
                :type score: int
            '''
        score = 0
        motif = self.createMotifFromIndexes(s)
        motif.doCounts()
        mat = motif.counts
        for j in range(len(mat[0])):
            maxcol = mat[0][j]
            for  i in range(1, len(mat)):
                if mat[i][j] > maxcol: 
                    maxcol = mat[i][j]
            score += maxcol
        return score
   
    def scoreMult(self, s: str)-> int:
        '''
            Devolve o score
            Inputs:
                :s: indices
                :type s: str
            Returns:
                :return score: score
                :type score: int
            '''
        score = 1.0
        motif = self.createMotifFromIndexes(s)
        motif.createPWM()
        mat = motif.pwm
        for j in range(len(mat[0])):
            maxcol = mat[0][j]
            for  i in range(1, len(mat)):
                if mat[i][j] > maxcol: 
                    maxcol = mat[i][j]
            score *= maxcol
        return score



    # EXHAUSTIVE SEARCH
       
    def nextSol (self, s:str):
        '''
            Devolve a próxima solução
            Inputs:
                :s: nodo
                :type s: str
            Returns:
                :return score: score
                :type score: int
            '''
        nextS = [0]*len(s)
        pos = len(s) - 1     
        while pos >=0 and s[pos] == self.seqSize(pos) - self.motifSize:
            pos -= 1
        if (pos < 0): 
            nextS = None
        else:
            for i in range(pos): 
                nextS[i] = s[i]
            nextS[pos] = s[pos]+1
            for i in range(pos+1, len(s)):
                nextS[i] = 0
        return nextS
        
    def exhaustiveSearch(self):
        '''
            Algoritmo de procura exaustiva
            Returns:
                :return res: lista com os resultados da procura exaustiva
                :type res: list
            '''
        melhorScore = -1
        res = []
        s = [0]* len(self.seqs)
        while (s!= None):
            sc = self.score(s)
            if (sc > melhorScore):
                melhorScore = sc
                res = s
            s = self.nextSol(s)
        return res

     
    # BRANCH AND BOUND     
     
    def nextVertex (self, s:str)-> list:
        '''
            Procura o próximo vértice
            Inputs:
                :s: nodo
                :type s: str
            Returns:
                :return res: lista com os próximos índices
                :type res: list
            '''
        res =  []
        if len(s) < len(self.seqs): # internal node -> down one level
            for i in range(len(s)): 
                res.append(s[i])
            res.append(0)
        else: # bypass
            pos = len(s)-1 
            while pos >=0 and s[pos] == self.seqSize(pos) - self.motifSize:
                pos -= 1
            if pos < 0: res = None # last solution
            else:
                for i in range(pos): res.append(s[i])
                res.append(s[pos]+1)
        return res

    def bypass (self, s:str)-> list:
        '''
            Algoritmo bypass que navega na árvore de procura
            Inputs:
                :s: nodo
                :type s: str
            Returns:
                :return res: lista com os resultados
                :type res: list
            '''
        res =  []
        pos = len(s) -1
        while pos >=0 and s[pos] == self.seqSize(pos) - self.motifSize:
            pos -= 1
        if pos < 0: res = None 
        else:
            for i in range(pos): res.append(s[i])
            res.append(s[pos]+1)
        return res
        
    def branchAndBound(self)-> str:
        '''
            Algoritmo que é utilizado para encontrar soluções ótimas
            Returns:
                :return melhorMotif: o melhor motif
                :type melhorMotif: lstr
            '''
        melhorScore = -1
        melhorMotif = None
        size = len(self.seqs)
        s = [0]*size
        while s != None:
            if len(s) < size:
                optimScore = self.score(s) + (size-len(s)) * self.motifSize
                if optimScore < melhorScore: s = self.bypass(s)
                else: s = self.nextVertex(s)
            else:
                sc = self.score(s)
                if sc > melhorScore:
                    melhorScore = sc
                    melhorMotif  = s
                s = self.nextVertex(s)
        return melhorMotif


    # Consensus (heuristic)

    def heuristicConsensus(self)-> list:
        '''
            Algoritmo que mantém um grande nº de soluções parciais em cada iteração (na ordem dos milhares) selecionando o melhor resultado no final
            Returns:
                :return res: lista com os resultados
                :type res: list
            '''
        seqs, resto = [self.seqs[0],self.seqs[1]], self.seqs[2:]
        melhorScore = -1
        res = []
        s = [0] * len(seqs)
        while (s != None):
            sc = self.score(s)
            if (sc > melhorScore):
                melhorScore = sc
                res = s
            s = self.nextSol(s)
        for i in range(len(resto)):
            aux = res
            melhorScore = -1
            for j in range(len(resto[i])-self.motifSize):
                aux.append(j)
                sc = self.score(aux)
                if (sc > melhorScore):
                    melhorScore = sc
                    best_i = j
                aux.pop()
            res.append(best_i)
        return res


    # Consensus (Stochastic)

    def heuristicStochastic(self)-> list:
        '''
            Algoritmo fortemente dependente das posições iniciais em que os resultados 
            podem ser melhorados se se considerarem várias ordens de apresentação das 
            sequências distintas
            Returns:
                :return pos_iniciais: lista com as posições iniciais
                :type pos_iniciais: list
            '''
        best_Score_list = []
        for x in range(100):
            pos_iniciais = [random.randint(0, self.seqSize(n)-self.motifSize) for n in range(len(self.seqs))]
            motif = self.createMotifFromIndexes(pos_iniciais)
            motif.createPWM()
            score = self.scoreMult(pos_iniciais)
            prev_score = score
            new_score = score + 0.000001
            while prev_score < new_score:
                for k in range(len(pos_iniciais)):
                    pos_iniciais[k] = motif.mostProbableSeq(self.seqs[k])
                prev_score = new_score
                new_score = self.scoreMult(pos_iniciais)
                motif = self.createMotifFromIndexes(pos_iniciais)
                motif.createPWM()
            best_Score_list.append(new_score)

        return pos_iniciais


# Gibbs sampling

    def gibbs(self, iter=1000)->list:
        '''
            Algoritmo para gerar uma sequência de amostras da distribuição conjunta de probabilidades de duas ou mais variáveis aleatórias.
            Sendo que o processo iterativo que vai substituindo um segmento em cada iteração.
            Inputs:
                :iter: valor a ser utilizado na range
                :type iter: int
            Returns:
                :return pos_iniciais: lista com as posições iniciais
                :type pos_iniciais: list
            '''
        pos_atuais = [random.randint(0, self.seqSize(n) - self.motifSize) for n in range(len(self.seqs))]
        score = self.scoreMult(pos_atuais)
        new_score = score + 0.000001
        while score < new_score:
            score = new_score
            for x in range(iter):
                seqi = random.randint(0, len(self.seqs) - 1)
                pos_atuais.pop(seqi)
                seq_removed = self.seqs.pop(seqi)
                motif = self.createMotifFromIndexes(pos_atuais)
                motif.createPWM()
                self.seqs.insert(seqi, seq_removed)
                probs = motif.probAllPositions(self.seqs[seqi])
                irolette = self.roulette(probs)
                pos_atuais.insert(seqi, irolette)
                for_score = self.scoreMult(pos_atuais)
                if for_score > new_score:
                    new_score = for_score
        return pos_atuais

    def roulette(self, f:str):
        '''
            Escolha aleatória. A probabilidade de escolher uma determinada posição é proporcional ao seu score.
            
            '''
        from random import random
        tot = 0.0
        for x in f: 
            tot += (0.01+x)
        val = random()* tot
        acum = 0.0
        ind = 0
        while acum < val:
            acum += (f[ind] + 0.01)
            ind += 1
        return ind-1


# tests

def test1():  
    sm = MotifFinding()
    sm.readFile("exemploMotifs.txt","dna")
    sol = [25,20,2,55,59]
    sa = sm.score(sol)
    print(sa)
    scm = sm.scoreMult(sol)
    print(scm)

def test2():
    print ("Test exhaustive:")
    seq1 = MySeq("ATAGAGCTGA","dna")
    seq2 = MySeq("ACGTAGATGA","dna")
    seq3 = MySeq("AAGATAGGGG","dna")
    mf = MotifFinding(3, [seq1,seq2,seq3])
    sol = mf.exhaustiveSearch()
    print ("Solution", sol)
    print ("Score: ", mf.score(sol))
    print("Consensus:", mf.createMotifFromIndexes(sol).consensus())

    print ("Branch and Bound:")
    sol2 = mf.branchAndBound()
    print ("Solution: " , sol2)
    print ("Score:" , mf.score(sol2))
    print("Consensus:", mf.createMotifFromIndexes(sol2).consensus())
    
    print ("Heuristic consensus: ")
    sol1 = mf.heuristicConsensus()
    print ("Solution: " , sol1)
    print ("Score:" , mf.score(sol1))
    print("Consensus:", mf.createMotifFromIndexes(sol1).consensus())

def test3():
    mf = MotifFinding()
    mf.readFile("exemploMotifs.txt","dna")
    print ("Branch and Bound:")
    sol = mf.branchAndBound()
    print ("Solution: " , sol)
    print ("Score:" , mf.score(sol))
    print("Consensus:", mf.createMotifFromIndexes(sol).consensus())

def test4():
    mf = MotifFinding()
    mf.readFile("exemploMotifs.txt","dna")

    print("Heuristic consensus: ")
    sol1 = mf.heuristicConsensus()
    print("Solution: ", sol1)
    print("Score:", mf.score(sol1))
    print("Consensus:", mf.createMotifFromIndexes(sol1).consensus())

    print("Heuristic stochastic")
    sol = mf.heuristicStochastic()
    print ("Solution: " , sol)
    print ("Score:" , mf.score(sol))
    print ("Score mult:" , mf.scoreMult(sol))
    print("Consensus:", mf.createMotifFromIndexes(sol).consensus())
    
    print("Gibbs Sampling")
    sol2 = mf.gibbs(100000)
    print("Solution: ", sol2)
    print("Score:" , mf.score(sol2))
    print("Score mult:" , mf.scoreMult(sol2))
    print("Consensus:", mf.createMotifFromIndexes(sol2).consensus())

def meu_teste():
    mf = MotifFinding()
    mf.readFile("exemploMotifs2.txt","dna")
    #sol = mf.exhaustiveSearch()
    #print(sol)
    print(mf.heuristicConsensus())
    #print(mf.heuristicStochastic())
    #print(mf.gibbs())

test1()
test2()
test3()
test4()
meu_teste()
