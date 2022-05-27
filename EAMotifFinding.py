# -*- coding: utf-8 -*-

from MySeq import MySeq
from MyMotifs import MyMotifs, printMat
import random


class MotifFinding:
    """
    Classe que encontra a posição em que o motif começa
    """
    
    def __init__(self, size = 8, seqs = None):
        self.motifSize = size #Indica qual é o tamanho dos motifs que vamos procurar; por definição, se não houver info acerca do tamanho usamos motifs de tamanho 8
        if (seqs != None):
            self.seqs = seqs
            self.alphabet = seqs[0].alfabeto()
        else:
            self.seqs = [] #Se for None, self.seqs é uma lista vazia
                    
    def __len__ (self):
        '''
        Retorna o número de elementos da lista self.seqs
        '''
        return len(self.seqs)
    
    def __getitem__(self, n):
        '''
        Retorna a primeira sequência da lista
            
        '''
        return self.seqs[n]
    
    def seqSize (self, i):
        '''
        Retorna o comprimento da sequência i da lista

        '''
        return len(self.seqs[i])
    
    def readFile(self, fic, t): 
        '''
        Lê um ficheiro que vai ser adicionado à lista self.seqs

        '''
        for s in open(fic, "r"):
            self.seqs.append(MySeq(s.strip().upper(),t))
        self.alphabet = self.seqs[0].alfabeto()
        
        
    def createMotifFromIndexes(self, indexes):
        '''
        Recebe uma lista de números composta pelos números das posições inciais dos motifs
   
        '''
        pseqs = []
        for i,ind in enumerate(indexes): #Faz uma contagem de elementos
            pseqs.append( MySeq(self.seqs[i][ind:(ind+self.motifSize)], self.seqs[i].tipo) )
            #Vai adicionar à lista pseqs uma sequência i (onde começa e acaba o motif) e o tipo de sequência com que estamos a trabalhar
        return MyMotifs(pseqs)
        
        
    # SCORES
        
    def score(self, s):
        score = 0
        motif = self.createMotifFromIndexes(s)
        motif.doCounts() #Cria a matriz de contagem
        mat = motif.counts #Matriz de contagens passa a ser mat
        for j in range(len(mat[0])): # ciclo vai correr as colunas da matriz
            maxcol = mat[0][j] #Máximo corresponde ao primeiro elemento da coluna
            for  i in range(1, len(mat)): #Passa para o segundo elemento e assim 
            #sucessivamente até chegar ao fim e comparar todos os elementos da coluna e descobrir qual tem o maior score    
                if mat[i][j] > maxcol: 
                    maxcol = mat[i][j]
            score += maxcol #o score passa a ser o valor máximo da coluna
        return score #Dá return ao score máximo
   
    def scoreMult(self, s):
        '''
        Semelhante à de cima mas em vez de contagem, usa probabilidades e usa a multiplicação
 
        '''
        score = 1.0
        motif = self.createMotifFromIndexes(s)
        motif.createPWM() #Matriz de probabilidades
        # print("PWM:")
        # printMat(motif.pwm)
        # print("\n\n")
        mat = motif.pwm #Matriz de probabilidades passa a ser mat
        for j in range(len(mat[0])):
            maxcol = mat[0][j]
            for  i in range(1, len(mat)):
                if mat[i][j] > maxcol: 
                    maxcol = mat[i][j]
            score *= maxcol #O score é multiplicado pelo valor máximo de cada coluna
        return score    #Dá return do score máximo   
       
    # EXHAUSTIVE SEARCH - vai comparar com tudo
       
    def nextSol (self, s):
        nextS = [0]*len(s) #Lista que contém as posições das sequências onde começa a formação dos motifs
        pos = len(s) - 1  #Posição é o comprimento da lista - 1 (lista com o número de sequências que existem)   
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
        return nextS #Vai finalizar e temos como resultado as posições dos motifs nas sequências
        
    def exhaustiveSearch(self):
        melhorScore = -1
        res = []
        s = [0]* len(self.seqs) #Posição inicial das sequências onde começam os motifs
        while (s!= None):
            sc = self.score(s) #Vai calcular o score dos motifs na posição inicial com o size escolhido
            if (sc > melhorScore):
                melhorScore = sc
                res = s #Lista com as posições iniciais onde vai começar o motif
            s = self.nextSol(s) ##O próximo s vai ser o nextSol
        return res #O resultado são as posições inicais que vão maximizar o score
     
    # BRANCH AND BOUND     
     
    def nextVertex (self, s):
        '''
        Procura entre os vértices
        Inputs:
            :s:
        Returns:
            :return
            :rtype
        '''
        res =  []
        if len(s) < len(self.seqs): # internal node -> down one level
            for i in range(len(s)):  #Procurar na sequência s um i
                res.append(s[i])
            res.append(0) #Como s é menor que seqs, a sequência não está a ser abranjida nas sequências, logo dá-se append de 0 para alcançar o tamanho das sequências
        else: # bypass
            pos = len(s)-1 #Número de sequências existentes
            while pos >=0 and s[pos] == self.seqSize(pos) - self.motifSize: #Enquanto a posição da sequência por menor ou igual a 0 e positção na lsta s por igual ao tamanho da sequência menos o tamanho do motif
                pos -= 1 #Diminui 1 na posição para ir para outra sequência
            if pos < 0: res = None # last solution
            else:
                for i in range(pos): res.append(s[i])
                res.append(s[pos]+1) #Adiciona ao último valor + 1
        return res #Dá return nas posições do melhor score
    
    
    def bypass (self, s):
        '''
        Verifica se já chegou ou não ao final de uma sequência
 
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
        
    def branchAndBound (self):
        '''
        Só verifica quando chegamos ao final de uma das sequências

        '''
        melhorScore = -1
        melhorMotif = None
        size = len(self.seqs)
        s = [0]*size #Cria s - lista com as posições iniciais onde começam os motifs
        while s != None: #Enquanto s não for vazio
            if len(s) < size:
                optimScore = self.score(s) + (size-len(s)) * self.motifSize
                if optimScore < melhorScore: #Se o score ótimo for menor que o melhor score anteriormente descoberto s = self.bypass(s)
                    #Passa-se a análise à frente -> vai para o bypass
                else: s = self.nextVertex(s)
            else:
                sc = self.score(s)
                if sc > melhorScore:
                    melhorScore = sc
                    melhorMotif  = s
                s = self.nextVertex(s)
        return melhorMotif

    # Consensus (heuristic)
  
    def heuristicConsensus(self):
        #É mais rápido mas não é o ideal porque as duas primeiras sequências não garantem a conservação das sequências
        '''
        Procura as posições para o motif nas duas primeiras sequências
 
        '''
        
        seqs_atuais = [self.seqs[0], self.seqs[1]]
        melhorScore = -1
        res = []
        s = [0] * len(seqs_atuais)
        
        while (s != None):
            sc = self.score(s)
            if (sc > melhorScore):
                melhorScore = sc
                res = s
            s = self.nextSol(s)
        

        for _ in range(len(self.seqs)-2):
            posicao_atual = len(seqs_atuais)

            seqs_atuais.append(self.seqs[posicao_atual])
            resultado_anterior = res
            res.append(0)
            s = res

            resultados_fazem_sentido = True
            while (s != None and resultados_fazem_sentido):
                sc = self.score(s)
                if (sc > melhorScore):
                    melhorScore = sc
                    res = s
                
                s = self.nextSol(s)
                for i in range(len(resultado_anterior)):
                    if(resultado_anterior[i] != res[i]):
                        resultados_fazem_sentido = False
                        break    
        return res

    # Consensus (heuristic)

    def heuristicStochastic (self):
        best_Score_list = []
        best_S_list = []
        for x in range(100): #Passo 1: inicia todas as posições com valores aleatórios 
            pos_motif_atuais = [random.randint(0, self.seqSize(n) - self.motifSize) for n in range(len(self.seqs))]
            motif = self.createMotifFromIndexes(pos_motif_atuais) #Constrói o perfil com base nas posições iniciais s
            motif.createPWM()
            score = self.scoreMult(pos_motif_atuais)
            prev_score = score
            new_score = score + 0.000001
            while prev_score < new_score:
                for k in range(len(pos_motif_atuais)): #Avalia a melhor posição inicial para cada sequência com base no perfil
                    pos_motif_atuais[k] = motif.mostProbableSeq(self.seqs[k]) #Vai ver em cada sequência qual é a subsequência que é mais provável acontecer na PWM
                prev_score = new_score #Verifica se houve alguma melhoria
                new_score = self.scoreMult(pos_motif_atuais)
                motif = self.createMotifFromIndexes(pos_motif_atuais)
                motif.createPWM()

            best_Score_list.append(new_score)
            best_S_list.append(pos_motif_atuais)
        
        s_do_max = -1
        max_ate_agora = -1
        for i in range(len(best_Score_list)):
            score = best_Score_list[i]
            if score > max_ate_agora:
                max_ate_agora = score
                s_do_max = best_S_list[i]

        return s_do_max

    # Gibbs sampling 
    # pos_iniciais = [7, 11, 9, 7, 1]
    # # pos_iniciais.remove(7)
    # pos_iniciais = [11, 9, 7, 1]
    # pos_iniciais = [7, 11, 9, 1]


    def gibbs(self, iter = 1000):
        pos_atuais = [random.randint(0, self.seqSize(n)-self.motifSize) for n in range(len(self.seqs))]
        score = self.scoreMult(pos_atuais)
        new_score = score + 0.000001
        while score < new_score:
            score = new_score
            for x in range(iter): #selecionar uma das sequência aleatoriamente
                seqi = random.randint(0, len(self.seqs)-1) #Posição
                pos_atuais.pop(seqi)
                seq_removed = self.seqs.pop(seqi) #Indica qual é a sequência que vai ser removida
                motif = self.createMotifFromIndexes(pos_atuais)
                motif.createPWM()
                self.seqs.insert(seqi, seq_removed) #Vai adicionar a sequência que foi removida anteriormente
                probs = motif.probAllPositions(self.seqs[seqi]) #Calcular a probabilidade de todas as subsequências possíveis na sequência removida
                irolette = self.roulette(probs)
                pos_atuais.insert(seqi, irolette)
                for_score = self.scoreMult(pos_atuais)
                if for_score > new_score:
                    new_score = for_score

        return pos_atuais

    def roulette(self, f):
        from random import random
        tot = 0.0
        for x in f: tot += (0.01+x)
        val = random()* tot #Vai multiplicar o total por um valor random - dá um número entre 0 e 1 (não incluído)
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
    seq4 = MySeq("ACTTAGATGA","dna")
    seq5 = MySeq("AAGATGGGGG","dna")
    seq6 = MySeq("ACTTACCTGA","dna")
    mf = MotifFinding(3, [seq1,seq2,seq3,seq4,seq5,seq6])
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
    print("Heuristic stochastic")
    sol = mf.heuristicStochastic()
    print ("Solution: " , sol)
    print ("Score:" , mf.score(sol))
    print ("Score mult:" , mf.scoreMult(sol))
    print("Consensus:", mf.createMotifFromIndexes(sol).consensus())
    
    sol2 = mf.gibbs(1000)
    print ("Score:" , mf.score(sol2))
    print ("Score mult:" , mf.scoreMult(sol2))


test3()
test4()
