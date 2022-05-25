# -*- coding: utf-8 -*-"""

# APAGAR!!!!  IGUAL AOS FICHEIROS AE.... 
def createMatZeros(nl, nc):
    res = []
    for i in range(0, nl):
        res.append([0] * nc)
    return res


def printMat(mat):
    for i in range(0, len(mat)): print(mat[i])


class MyMotifs:

    def __init__(self, seqs):
        self.size = len(seqs[0])
        self.seqs = seqs  # objetos classe MySeq
        self.alphabet = seqs[0].alfabeto()
        self.doCounts()
        self.createPWM()

    def __len__(self):
        return self.size

    def doCounts(self):
        self.counts = createMatZeros(len(self.alphabet), self.size)
        for s in self.seqs:
            for i in range(self.size):
                lin = self.alphabet.index(s[i])
                self.counts[lin][i] += 1

    def createPWM(self):
        if self.counts == None: self.doCounts()
        self.pwm = createMatZeros(len(self.alphabet), self.size)
        for i in range(len(self.alphabet)):
            for j in range(self.size):
                self.pwm[i][j] = float(self.counts[i][j]) / len(self.seqs)

    def consensus(self):
        res = ""
        for j in range(self.size):
            maxcol = self.counts[0][j]
            maxcoli = 0
            for i in range(1, len(self.alphabet)):
                if self.counts[i][j] > maxcol:
                    maxcol = self.counts[i][j]
                    maxcoli = i
            res += self.alphabet[maxcoli]
        return res

    def maskedConsensus(self):
        res = ""
        for j in range(self.size):
            maxcol = self.counts[0][j]
            maxcoli = 0
            for i in range(1, len(self.alphabet)):
                if self.counts[i][j] > maxcol:
                    maxcol = self.counts[i][j]
                    maxcoli = i
            if maxcol > len(self.seqs) / 2:
                res += self.alphabet[maxcoli]
            else:
                res += "-"
        return res

    def probabSeq(self, seq):
        res = 1.0
        for i in range(self.size):
            lin = self.alphabet.index(seq[i])
            res *= self.pwm[lin][i]
        return res

    def probAllPositions(self, seq):
        res = []
        for k in range(len(seq) - self.size + 1):
            res.append(self.probabSeq(seq))
        return res

    def mostProbableSeq(self, seq):
        maximo = -1.0
        maxind = -1
        for k in range(len(seq) - self.size):
            p = self.probabSeq(seq[k:k + self.size])
            if (p > maximo):
                maximo = p
                maxind = k
        return maxind


class MySeq:
    """
    @author: miguelrocha
    """
    def __init__(self, seq, tipo="dna"):
        self.seq = seq.upper()
        self.tipo = tipo

    def __len__(self):
        return len(self.seq)

    def __getitem__(self, n):
        return self.seq[n]

    def __getslice__(self, i, j):
        return self.seq[i:j]

    def __str__(self):
        return self.tipo + ":" + self.seq

    def printseq(self):
        print(self.seq)

    def alfabeto(self):
        if (self.tipo == "dna"):
            return "ACGT"
        elif (self.tipo == "rna"):
            return "ACGU"
        elif (self.tipo == "protein"):
            return "ACDEFGHIKLMNPQRSTVWY"
        else:
            return None

    def valida(self):
        alf = self.alfabeto()
        res = True
        i = 0
        while i < len(self.seq) and res:
            if self.seq[i] not in alf:
                res = False
            else:
                i += 1
        return res

    def validaER(self):
        import re
        if (self.tipo == "dna"):
            if re.search("[^ACTGactg]", self.seq) != None:
                return False
            else:
                return True
        elif (self.tipo == "rna"):
            if re.search("[^ACUGacug]", self.seq) != None:
                return False
            else:
                return True
        elif (self.tipo == "protein"):
            if re.search("[^ACDEFGHIKLMNPQRSTVWY_acdefghiklmnpqrstvwy]", self.seq) != None:
                return False
            else:
                return True
        else:
            return False

    def transcricao(self):
        if (self.tipo == "dna"):
            return MySeq(self.seq.replace("T", "U"), "rna")
        else:
            return None

    def compInverso(self):
        if (self.tipo != "dna"): return None
        comp = ""
        for c in self.seq:
            if (c == 'A'):
                comp = "T" + comp
            elif (c == "T"):
                comp = "A" + comp
            elif (c == "G"):
                comp = "C" + comp
            elif (c == "C"):
                comp = "G" + comp
        return MySeq(comp)

    def traduzSeq(self, iniPos=0):
        if (self.tipo != "dna"): return None
        seqM = self.seq
        seqAA = ""
        for pos in range(iniPos, len(seqM) - 2, 3):
            cod = seqM[pos:pos + 3]
            seqAA += self.traduzCodao(cod)
        return MySeq(seqAA, "protein")

    def orfs(self):
        if (self.tipo != "dna"): return None
        res = []
        res.append(self.traduzSeq(0))
        res.append(self.traduzSeq(1))
        res.append(self.traduzSeq(2))
        compinv = self.compInverso()
        res.append(compinv.traduzSeq(0))
        res.append(compinv.traduzSeq(1))
        res.append(compinv.traduzSeq(2))
        return res

    def traduzCodao(self, cod):
        tc = {"GCT": "A", "GCC": "A", "GCA": "A", "GCC": "A", "TGT": "C", "TGC": "C",
              "GAT": "D", "GAC": "D", "GAA": "E", "GAG": "E", "TTT": "F", "TTC": "F",
              "GGT": "G", "GGC": "G", "GGA": "G", "GGG": "G", "CAT": "H", "CAC": "H",
              "ATA": "I", "ATT": "I", "ATC": "I",
              "AAA": "K", "AAG": "K",
              "TTA": "L", "TTG": "L", "CTT": "L", "CTC": "L", "CTA": "L", "CTG": "L",
              "ATG": "M", "AAT": "N", "AAC": "N",
              "CCT": "P", "CCC": "P", "CCA": "P", "CCG": "P",
              "CAA": "Q", "CAG": "Q",
              "CGT": "R", "CGC": "R", "CGA": "R", "CGG": "R", "AGA": "R", "AGG": "R",
              "TCT": "S", "TCC": "S", "TCA": "S", "TCG": "S", "AGT": "S", "AGC": "S",
              "ACT": "T", "ACC": "T", "ACA": "T", "ACG": "T",
              "GTT": "V", "GTC": "V", "GTA": "V", "GTG": "V",
              "TGG": "W",
              "TAT": "Y", "TAC": "Y",
              "TAA": "_", "TAG": "_", "TGA": "_"}
        if cod in tc:
            aa = tc[cod]
        else:
            aa = "X"  # errors marked with X
        return aa

    def traduzCodaoER(self, cod):
        import re
        if re.search("GC.", cod):
            aa = "A"
        elif re.search("TG[TC]", cod):
            aa = "C"
        elif re.search("GA[TC]", cod):
            aa = "D"
        elif re.search("GA[AG]", cod):
            aa = "E"
        elif re.search("TT[TC]", cod):
            aa = "F"
        elif re.search("GG.", cod):
            aa = "G"
        elif re.search("CA[TC]", cod):
            aa = "H"
        elif re.search("AT[TCA]", cod):
            aa = "I"
        elif re.search("AA[AG]", cod):
            aa = "K"
        elif re.search("TT[AG]|CT.", cod):
            aa = "L"
        elif re.search("ATG", cod):
            aa = "M"
        elif re.search("AA[TC]", cod):
            aa = "N"
        elif re.search("CC.", cod):
            aa = "P"
        elif re.search("CA[AG]", cod):
            aa = "Q"
        elif re.search("CG.|AG[AG]", cod):
            aa = "R"
        elif re.search("TC.|AG[TC]", cod):
            aa = "S"
        elif re.search("AC.", cod):
            aa = "T"
        elif re.search("GT.", cod):
            aa = "V"
        elif re.search("TGG", cod):
            aa = "W"
        elif re.search("TA[TC]", cod):
            aa = "Y"
        elif re.search("TA[AG]|TGA", cod):
            aa = "_";
        else:
            aa = None
        return aa

    def maiorProteina(self):
        if (self.tipo != "protein"):
            return None
        seqAA = self.seq
        protAtual = ""
        maiorprot = ""
        for aa in seqAA:
            if aa == "_":
                if len(protAtual) > len(maiorprot):
                    maiorprot = protAtual
                protAtual = ""
            else:
                if len(protAtual) > 0 or aa == "M":
                    protAtual += aa
        return MySeq(maiorprot, "protein")

    def maiorProteinaER(self):
        import re
        if (self.tipo != "protein"): return None
        mos = re.finditer("M[^_]*_", self.seq)
        sizem = 0
        lprot = ""
        for x in mos:
            ini = x.span()[0]
            fin = x.span()[1]
            s = fin - ini + 1
            if s > sizem:
                lprot = x.group()
                sizem = s
        return MySeq(lprot, "protein")

    def todasProteinas(self):
        if (self.tipo != "protein"):
            return None
        seqAA = self.seq
        protsAtuais = []
        proteinas = []
        for aa in seqAA:
            if aa == "_":
                if protsAtuais:
                    for p in protsAtuais:
                        proteinas.append(MySeq(p, "protein"))
                    protsAtuais = []
            else:
                if aa == "M":
                    protsAtuais.append("")
                for i in range(len(protsAtuais)):
                    protsAtuais[i] += aa

        return proteinas

    def maiorProteinaORFs(self):
        if (self.tipo != "dna"):
            return None
        larg = MySeq("", "protein")
        for orf in self.orfs():
            prot = orf.maiorProteinaER()
            if len(prot.seq) > len(larg.seq):
                larg = prot
        return larg


class MotifFinding:
    
    def __init__(self, size=8, seqs=None):
        self.motifSize = size
        if (seqs != None):
            self.seqs = seqs
            self.alphabet = seqs[0].alfabeto()
        else:
            self.seqs = []

    def __len__(self):
        return len(self.seqs)

    def __getitem__(self, n):
        return self.seqs[n]

    def seqSize(self, i):
        return len(self.seqs[i])

    def readFile(self, fic, t):
        for s in open(fic, "r"):
            self.seqs.append(MySeq(s.strip().upper(), t))
        self.alphabet = self.seqs[0].alfabeto()

    def createMotifFromIndexes(self, indexes):
        pseqs = []
        for i, ind in enumerate(indexes):
            pseqs.append(MySeq(self.seqs[i][ind:(ind + self.motifSize)], self.seqs[i].tipo))
        return MyMotifs(pseqs)

    # SCORES

    def score(self, s):
        score = 0
        motif = self.createMotifFromIndexes(s)
        motif.doCounts()
        mat = motif.counts
        for j in range(len(mat[0])):
            maxcol = mat[0][j]
            for i in range(1, len(mat)):
                if mat[i][j] > maxcol:
                    maxcol = mat[i][j]
            score += maxcol
        return score

    def scoreMult(self, s):
        score = 1.0
        motif = self.createMotifFromIndexes(s)
        motif.createPWM()
        mat = motif.pwm
        for j in range(len(mat[0])):
            maxcol = mat[0][j]
            for i in range(1, len(mat)):
                if mat[i][j] > maxcol:
                    maxcol = mat[i][j]
            score *= maxcol
        return score

    # EXHAUSTIVE SEARCH

    def nextSol(self, s):
        nextS = [0] * len(s)
        pos = len(s) - 1
        while pos >= 0 and s[pos] == self.seqSize(pos) - self.motifSize:
            pos -= 1
        if (pos < 0):
            nextS = None
        else:
            for i in range(pos):
                nextS[i] = s[i]
            nextS[pos] = s[pos] + 1;
            for i in range(pos + 1, len(s)):
                nextS[i] = 0
        return nextS

    def exhaustiveSearch(self):
        melhorScore = -1
        res = []
        s = [0] * len(self.seqs)
        while (s != None):
            sc = self.score(s)
            if (sc > melhorScore):
                melhorScore = sc
                res = s
            s = self.nextSol(s)
        return res

    # BRANCH AND BOUND

    def nextVertex(self, s):
        res = []
        if len(s) < len(self.seqs):  # internal node -> down one level
            for i in range(len(s)):
                res.append(s[i])
            res.append(0)
        else:  # bypass
            pos = len(s) - 1
            while pos >= 0 and s[pos] == self.seqSize(pos) - self.motifSize:
                pos -= 1
            if pos < 0:
                res = None  # last solution
            else:
                for i in range(pos): res.append(s[i])
                res.append(s[pos] + 1)
        return res

    def bypass(self, s):
        res = []
        pos = len(s) - 1
        while pos >= 0 and s[pos] == self.seqSize(pos) - self.motifSize:
            pos -= 1
        if pos < 0:
            res = None
        else:
            for i in range(pos): res.append(s[i])
            res.append(s[pos] + 1)
        return res

    def branchAndBound(self):
        melhorScore = -1
        melhorMotif = None
        size = len(self.seqs)
        s = [0] * size
        while s != None:
            if len(s) < size:
                optimScore = self.score(s) + (size - len(s)) * self.motifSize
                if optimScore < melhorScore:
                    s = self.bypass(s)
                else:
                    s = self.nextVertex(s)
            else:
                sc = self.score(s)
                if sc > melhorScore:
                    melhorScore = sc
                    melhorMotif = s
                s = self.nextVertex(s)
        return melhorMotif

    # Consensus (heuristic)

     def heuristicConsensus(self):
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

     def heuristicStochastic(self):
        best_Score_list = []
        for x in range(100):
            pos_iniciais = [randint(0, self.seqSize(n)-self.motifSize) for n in range(len(self.seqs))]
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

   def gibbs(self, iter = 1000):
        pos_atuais = [random.randint(0, self.seqSize(n)-self.motifSize) for n in range(len(self.seqs))]
        score = self.scoreMult(pos_atuais)
        new_score = score + 0.000001
        while score < new_score:
            score = new_score
            for x in range(iter):
                seqi = random.randint(0, len(self.seqs)-1)
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


    def roulette(self, f):
        from random import random
        tot = 0.0
        for x in f: tot += (0.01 + x)
        val = random() * tot
        acum = 0.0
        ind = 0
        while acum < val:
            acum += (f[ind] + 0.01)
            ind += 1
        return ind - 1
