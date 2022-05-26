from EvolAlgorithm import EvolAlgorithm
from Popul import PopulInt, PopulReal
from MotifFinding import MotifFinding, MotifFindingReal
from MyMotifs import MyMotifs


def createMatZeros(nl, nc):
    res = []
    for _ in range(0, nl):
        res.append([0]*nc)
    return res


def printMat(mat):
    for i in range(0, len(mat)):
        for j in range(len(mat[i])):
            print(f"{mat[i][j]:.3f}", end=' ')
        print()


class EAMotifsInt (EvolAlgorithm):
    def __init__(self, popsize, numits, noffspring, filename):
        self.motifs = MotifFinding()
        self.motifs.readFile(filename, "dna")
        indsize = len(self.motifs)
        EvolAlgorithm.__init__(self, popsize, numits, noffspring, indsize)

    def initPopul(self, indsize):
        maxvalue = self.motifs.seqSize(0) - self.motifs.motifSize
        self.popul = PopulInt(self.popsize, indsize,
                              maxvalue, [])

    def evaluate(self, indivs):
        for i in range(len(indivs)):
            ind = indivs[i]
            sol = ind.getGenes()
            fit = self.motifs.score(sol)
            ind.setFitness(fit)


class EAMotifsReal (EvolAlgorithm):
    def __init__(self, popsize, numits, noffspring, filename):
        self.motifs = MotifFindingReal()
        self.motifs.readFile(filename, "dna")
        indsize = self.motifs.motifSize * len(self.motifs.alphabet)
        EvolAlgorithm.__init__(self, popsize, numits, noffspring, indsize)

    def initPopul(self, indsize):
        maxvalue = self.motifs.seqSize(0) - self.motifs.motifSize
        
        
        self.popul = PopulReal(seqs=self.motifs.seqs, 
                                popsize=self.popsize, 
                                indsize=self.motifs.motifSize, 
                                lb=0,
                                ub=maxvalue, 
                                indivs=[])

    # def vector_to_PWM(self, v): #v -> vetor de números reais 
    #     pwm = createMatZeros(len(self.motifs.alphabet), self.motifs.motifSize)
    #     for i in range(0, len(v), self.motifs.alphabet):
    #         col_idx = i / len(self.motifs.alphabet)
    #         col = v[i:i + len(self.motifs.alphabet)]
    #         soma = sum(col)
    #         for j in range(len(self.motifs.alphabet)):
    #             self.pwm[j][col_idx] = col[j] / soma
    #     return pwm


    def evaluate(self, indivs): #Muda a função de avaliação -> usamos o socre
        for i in range(len(indivs)):
            ind = indivs[i] #Cada vetor de posições
            sol = ind.getGenes()
            score = 1.0
            
            for j in range(len(sol[0])):
                maxcol = sol[0][j]
                for  i in range(1, len(sol)):
                    if sol[i][j] > maxcol: 
                        maxcol = sol[i][j]
                score *= maxcol

            fit = self.motifs.score(sol) #Avalia o score que será a fit para cada vetor de posições iniciais
            ind.setFitness(fit)

def test1():
    ea = EAMotifsInt(popsize=100, numits=1000, noffspring=50, filename="exemploMotifs.txt")
    ea.run()
    ea.printBestSolution()


def test2():
    print("EAMotifsReal")
    # ea = EAMotifsReal(popsize=100, numits=2000, noffspring=50, filename="exemploMotifs.txt", 2)
    ea = EAMotifsReal(popsize=100, numits=2000, noffspring=50, filename="exemploMotifs.txt")
    print("run()")
    ea.run()
    print("printBestSolution()")
    ea.printBestSolution()


if __name__ == "__main__":

    # test1()
    test2()
