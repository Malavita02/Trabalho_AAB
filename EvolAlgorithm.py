from Popul import Popul


class EvolAlgorithm:
    """
    Class que faz o EA receber o tamanho da populaçao, o n de iterações, o n de descedentes e o tamanho do individuo
    """
    def __init__(self, popsize, numits, noffspring, indsize):
        self.popsize = popsize
        self.numits = numits
        self.noffspring = noffspring
        self.indsize = indsize
        self.initPopul(self.indsize)
        self.run()

    def initPopul(self, indsize):
        self.popul = Popul(self.popsize, indsize)

    
    def evaluate(self, indivs):
        '''
        Avalia o fitness de cada indivíduo da população
        Inputs:
            :indivs:
        '''
        for i in range(len(indivs)):
            ind = indivs[i]
            fit = 0.0
            for x in ind.getGenes():
                if x == 1:
                    fit += 1.0
            ind.setFitness(fit)
        return None

    def iteration(self):
        parents = self.popul.selection(self.noffspring)
        offspring = self.popul.recombination(parents, self.noffspring)
        self.evaluate(offspring)
        self.popul.reinsertion(offspring)

    def run(self):
        self.initPopul(self.indsize)
        self.evaluate(self.popul.indivs)
        self.bestsol = self.popul.bestSolution()
        for i in range(self.numits+1):
            self.iteration()
            bs = self.popul.bestSolution()
            if bs > self.bestsol:
                self.bestsol = bs
            print("Iteration:", i, " ", "Best: ", self.bestsol)

    def get_best_sol(self):
        return self.bestsol

    def get_best_fit(self):
        return self.bestsol.getFitness()

    def printBestSolution(self):
        print("Best solution: ", self.bestsol.getGenes())
        print()
        print("Best fitness:", self.bestsol.getFitness())
        print()


def test():
    ea = EvolAlgorithm(popsize=1000, numits=1000, noffspring=800, indsize=50)
    ea.run()
    ea.printBestSolution()


if __name__ == "__main__":
    test()
