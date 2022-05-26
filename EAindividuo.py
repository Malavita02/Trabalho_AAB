from random import randint, random, shuffle

''' O que caracteriza o indivíduo são os seus genes e o fitness (valor de aptidão) 
        lb e ub são o intervalo de valores que cada gene pode ter 
        '''

class Indiv:

    def __init__(self, size, genes=None, lb=0, ub=1):
        self.lb = lb #Lower bound -> limite inferior do gene 0-binário
        self.ub = ub #Upper bound -> limite superioe do gene 1-binário
        self.genes = genes #Genoma (informação de todo o inidivíduo)
        self.fitness = None #Guarda o valor de aptidão (fitness)
        if not self.genes: #Se não fro fornecida nenhuma lista de genes
            self.initRandom(size) #Gera-se um indivíduo de forma aleatória

    # comparadores.
    # Permitem usar sorted, max, min
        #(sobre a população em que a comparação é feita com base no fitnesse - qualidade das soluções)

    def __eq__(self, solution):
        if isinstance(solution, self.__class__):
            return self.genes.sort() == solution.genes.sort()
        return False

    def __gt__(self, solution):
        if isinstance(solution, self.__class__):
            return self.fitness > solution.fitness
        return False

    def __ge__(self, solution):
        if isinstance(solution, self.__class__):
            return self.fitness >= solution.fitness
        return False

    def __lt__(self, solution):
        if isinstance(solution, self.__class__):
            return self.fitness < solution.fitness
        return False

    def __le__(self, solution):
        if isinstance(solution, self.__class__):
            return self.fitness <= solution.fitness
        return False

    def __str__(self):
        return f"{str(self.genes)} {self.getFitness()}"

    def __repr__(self):
        return self.__str__()

    def setFitness(self, fit):
        self.fitness = fit

    def getFitness(self):
        return self.fitness

    def getGenes(self):
        return self.genes

    def initRandom(self, size): ''' Gera indivíduos de forma aleatória '''
        self.genes = []
        for _ in range(size): #Size é o número de indivíduos (população) -> a nossa solução
            self.genes.append(randint(self.lb, self.ub)) #Gera inidivíduos aleatórios entre 0 e 1 (caso seja binário)

    def mutation(self): #São dependentes das representações
         ''' Mutação sobre im vetor de valores binários '''
        s = len(self.genes) #Genes = [0, 1, 0, 1, 0, 1]
        pos = randint(0, s-1) #Gera uma posição -> s - 1 porque o len começa a contar no 1 e o randint este está incluído
        if self.genes[pos] == 0:
            self.genes[pos] = 1
        else:
            self.genes[pos] = 0

    def crossover(self, indiv2): ''' Cruzamente de um ponto '''
        return self.one_pt_crossover(indiv2)

    def one_pt_crossover(self, indiv2): ''' Construção de um novo indivíduo '''
        offsp1 = []  #Descendente 1
        offsp2 = [] #Descendente 2
        s = len(self.genes)
        pos = randint(0, s-1)
        for i in range(pos): #Corre o pos
            offsp1.append(self.genes[i]) #Mantém = até pos - 1 , por ex: pos = 4, vai manter até à posição 2
            offsp2.append(indiv2.genes[i])
        for i in range(pos, s):
            offsp2.append(self.genes[i]) #Troca de pos até ao fim (progenitor 2 troca com o 1)
            offsp1.append(indiv2.genes[i])
        res1 = self.__class__(s, offsp1, self.lb, self.ub) #Cria uma nova instância mas com base na representação do novo
        res2 = self.__class__(s, offsp2, self.lb, self.ub)
        return res1, res2


class IndivInt (Indiv):

    def __init__(self, size, genes=[], lb=0, ub=1): #ub = tamanho da seq - tamanho do motif
        self.lb = lb
        self.ub = ub
        self.genes = genes
        self.fitness = None
        if not self.genes:
            self.initRandom(size)

    def initRandom(self, size):
         ''' Gerar indivíduos aleatoriamente '''
        self.genes = []
        for _ in range(size):
            self.genes.append(randint(0, self.ub))

    def mutation(self):
        s = len(self.genes)
        pos = randint(0, s-1) #Escolher posição aleatória
        self.genes[pos] = randint(0, self.ub) #Substituir essa posição por um valor aleatório entre 0 e ub
        
        while (num == self.genes[pos]):
            num = randint(0, self.ub)
        
        self.genes[pos] = num


