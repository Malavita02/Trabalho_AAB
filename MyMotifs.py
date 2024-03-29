# -*- coding: utf-8 -*-

def createMatZeros (nl, nc): # cria matriz de zeros nlxnc
    '''
    Cria matriz de zeros
    Inputs:
        :nl: número de linhas
        :type nl: int
        :nc: número de colunas
        :type nc: int
    Returns:
        :return list: matriz de zeros
        :rtype list: list
    '''
    res = [ ] 
    for i in range(0, nl):
        res.append([0]*nc)
    return res

def printMat(mat):
    for i in range(0, len(mat)): print(mat[i])

class MyMotifs:
    """
    classe que recebe uma lista de sequÊncias
    """
    def __init__(self, seqs):
        self.size = len(seqs[0])
        self.seqs = seqs # objetos classe MySeq
        self.alphabet = seqs[0].alfabeto()
        self.doCounts()
        self.createPWM()
        
    def __len__ (self):
        '''
        Comprimento das seqs
        '''
        return self.size
        
    def doCounts(self):
        '''
        Cria a matriz de contagens
        '''
        self.counts = createMatZeros(len(self.alphabet), self.size)
        for s in self.seqs:
            for i in range(self.size):
                lin = self.alphabet.index(s[i])
                self.counts[lin][i] += 1
                
    def createPWM(self):
        '''
        Cria a matriz de probabilidades
        '''
        if self.counts == None: self.doCounts()
        self.pwm = createMatZeros(len(self.alphabet), self.size)
        for i in range(len(self.alphabet)):
            for j in range(self.size):
                self.pwm[i][j] = float(self.counts[i][j]) / len(self.seqs)
                
    def consensus(self):
        '''
        Procura o consensus na matriz dos counts por coluna
        '''
        res = ""
        for j in range(self.size):
            maxcol = self.counts[0][j]
            maxcoli = 0
            for i in range(1, len(self.alphabet) ):
                if self.counts[i][j] > maxcol: 
                    maxcol = self.counts[i][j]
                    maxcoli = i
            res += self.alphabet[maxcoli]        
        return res

    def maskedConsensus(self):
        '''
        Semelhantes ao consensus mas só interessa as letras com uma incidência superior a 50% em todas as seqs
        '''
        res = ""
        for j in range(self.size):
            maxcol = self.counts[0][j]
            maxcoli = 0
            for i in range(1, len(self.alphabet) ):
                if self.counts[i][j] > maxcol: 
                    maxcol = self.counts[i][j]
                    maxcoli = i
            if maxcol > len(self.seqs) / 2:
                res += self.alphabet[maxcoli]        
            else:
                res += "-"
        return res

    def probabSeq (self, seq):
        '''
        Probabilidade da seq fazer parte da PWM
        '''
        res = 1.0
        for i in range(self.size):
            lin = self.alphabet.index(seq[i])
            res *= self.pwm[lin][i]
        return res
    
    def probAllPositions(self, seq):
        '''
        Probablidade de devolver uma lista com as probabilidades de acontecer em cada letra da seq
        '''
        
        res = []
        for pos in range(len(seq)-self.size+1):
            res.append(self.probabSeq(seq[pos:pos+self.size]))
        return res

    def mostProbableSeq(self, seq):
        '''
        Verifica qual é a posição inicial da subseq de uma seq de comprimento indefinido que encaixa melhor no quadro de motifs das seqs
        '''
        
        maximo = -1.0
        maxind = -1
        for k in range(len(seq)-self.size):
            p = self.probabSeq(seq[k:k+ self.size])
            if(p > maximo):
                maximo = p
                maxind = k
        return maxind

def test():
    # test
    from MySeq import MySeq
    seq1 = MySeq("AAAGTT")
    seq2 = MySeq("CACGTG")
    seq3 = MySeq("TTGGGT")
    seq4 = MySeq("GACCGT")
    seq5 = MySeq("AACCAT")
    seq6 = MySeq("AACCCT")
    seq7 = MySeq("AAACCT")
    seq8 = MySeq("GAACCT")
    lseqs = [seq1, seq2, seq3, seq4, seq5, seq6, seq7, seq8]
    motifs = MyMotifs(lseqs)
    printMat (motifs.counts)
    printMat (motifs.pwm)
    print(motifs.alphabet)
    
    print(motifs.probabSeq("AAACCT"))
    print(motifs.probabSeq("ATACAG"))
    print(motifs.mostProbableSeq("CTATAAACCTTACATC"))
    
    print(motifs.consensus())
    print(motifs.maskedConsensus())

if __name__ == '__main__':
    test()
