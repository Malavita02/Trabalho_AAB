# -*- coding: utf-8 -*-

from Individuo import Indiv, IndivInt
from random import random


class Popul:
    # objeto da class Indiv
    def __init__(self, popsize, indsize, indivs=[]):
        self.popsize = popsize #Número de indivíduos da população (10 listas)
        self.indsize = indsize #Tamanho dos indivíduos (cada indivíduo (lista) com 5 elementos)

        # se já forem dados os indivíduos
        if indivs != []:
            self.indivs = indivs
        else:
            # gera aleatoriamente toda a população
            self.initRandomPop()

    def getIndiv(self, index): #Vai bsucar o indivíduo x
        return self.indivs[index]

    def initRandomPop(self):
        '''
        Gera indivíduos de forma aleatória
        '''
        self.indivs = []
        for _ in range(self.popsize): #Quantidade de listas a gerar
            indiv_i = Indiv(self.indsize)
            self.indivs.append(indiv_i)

    def getFitnesses(self, indivs=None): 
        '''
        Vai buscar todos os fitness (valores de aptidão) dos indivíduos
        '''
        fitnesses = [] #Lista de fitness
        if not indivs: #Se não forem inseridos os indivíduos
            indivs = self.indivs
        for ind in indivs:  #Se forem inseridos os indivíduos
            fitnesses.append(ind.getFitness()) #Adicionar fitness à lista
        return fitnesses

    def bestSolution(self):
        '''
        Melhor solução dos indivíduos
        '''
        return max(self.indivs)

    def bestFitness(self):
        '''
        Indivíduos com melhor fitness (avaliação máxima)
        '''
        indv = self.bestSolution() #Melhor solução
        return indv.getFitness() #Fitness da solução


    def selection(self, n, indivs=None): 
        '''
        Mecanismo de seleção para reprodução
        '''
        res = []
        fitnesses = list(self.linscaling(self.getFitnesses(indivs)))
         #Vai obter os fitnesses dos indivíduos e fazer a normalização
        for _ in range(n): #n = número de novos descendentes
            sel = self.roulette(fitnesses) #Seleção através da roulette (sel = posição do fitness)
            fitnesses[sel] = 0.0
            res.append(sel)
        return res

    def roulette(self, f):
        tot = sum(f)
        val = random()
        acum = 0.0
        ind = 0
        while acum < val:
            acum += (f[ind] / tot)
            ind += 1
        return ind-1

    def linscaling(self, fitnesses): #Normalização do valor de aptidão para [0, 1]
        mx = max(fitnesses)
        mn = min(fitnesses)
        res = []
        
        for f in fitnesses:
            # se o minimo == maximo, todos os elementos são iguais
            # nesse caso, colocamos a probabilidade igual para todos (1/num elementos)
            if mx == mn:
                res.append(1/len(fitnesses))
            else:
                val = (f-mn)/(mx-mn)
                res.append(val)
        return res

    def recombination(self, parents, noffspring):
        #noffspring -> quantas novas soluções queremos gerar a partir da população existente
        offspring = []
        new_inds = 0 #Inicialização de novos indivíduos
        while new_inds < noffspring:
            parent1 = self.indivs[parents[new_inds]] #Vai buscar o progenitor 1 aos indivíduos
            parent2 = self.indivs[parents[new_inds+1]]
            offsp1, offsp2 = parent1.crossover(parent2) #Cruzamento entre os progenitores
            offsp1.mutation() #Aplica uma mutação à nova geraçã
            offsp2.mutation()
            offspring.append(offsp1) #Adiciona à lista de novos descendentes
            offspring.append(offsp2)
            new_inds += 2
        return offspring

    def reinsertion(self, offspring):
        '''
        Mecanismo de reinserção: seleção dos indivíduos que vão constituir a população ou a iteração seguinte
        '''
        tokeep = self.selection(self.popsize-len(offspring))
        ind_offsp = 0
        for i in range(self.popsize):
            if i not in tokeep:
                self.indivs[i] = offspring[ind_offsp]#Preencher o resta da populção com novos indivíduos
                ind_offsp += 1


class PopulInt(Popul):

    def __init__(self, popsize, indsize, ub, indivs=[]):
        self.ub = ub
        Popul.__init__(self, popsize, indsize, indivs)

    def initRandomPop(self):
        self.indivs = []
        for _ in range(self.popsize):
            indiv_i = IndivInt(self.indsize, [], 0, self.ub) #Gera os indivíduos aleatoriamente (número de elementos, lista); NOTA: diferente IndivInt
            self.indivs.append(indiv_i)

