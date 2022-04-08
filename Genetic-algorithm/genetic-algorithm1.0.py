import sys
import random as rd
sys.path.append('../Neural_Network')
from neural_network1_0 import *
class Creature(object):

    def __init__(self,long,wide,structure):
        gentic = ''
        for i in range(long):
            gene = str(rd.randint(0,2))
            gentic += gene
        self.gentic = gentic
        self.long = long
        self.wide = wide
        self.structure = structure

    def intersect(self,wife):
        m = int(rd.random()*self.long)
        n = int(rd.random()*self.long)
        m,n = max(m,n),min(m,n)
        for i in range(m,n):
            self.gentic[i],wife.gentic[i] = wife.gentic[i],self.gentic[i]

    def varition(self):
        m = int(rd.random() * self.long)
        n = int(rd.random() * self.long)
        m, n = max(m, n), min(m, n)
        for i in range(m, n):
            self.gentic[i] = rd.randint(0,1)

class Population(object):

    def __init__(self,number,long):
        self.number = number
        creature = []
        for i in range(number):
            creature.append(Creature(long))
        self.creature = creature

    def iteration(self):
        reproduce_index = self.number*0.5
        intersect_index = self.number*0.8
        new_creature = []
        self.creature.sort(key=lambda d:d.fitness)
        for i in range(reproduce_index):
            new_creature.append(self.creature[i])
        for i in range(reproduce_index,intersect_index,2):
            self.creature[i].intersect(self.creature[i+1])
        for i in range(reproduce_index, intersect_index):
            new_creature.append(self.creature[i])
        for i in range(intersect_index,self.number):
            new_creature.append(self.creature[i].varition())
        self.creature = new_creature

class Network_by_genetic(Neural_network):

    def __init__(self):
        super().__init__()
        self.structure = structure
        num = 0
        for each in self.neural_network:
            for cell in each:
                for i in cell.weight:
                    num += 1
        self.weight_number = num

    def bulid_population(self,precise,creature_num):

        def num_claculate(x):
            num = 0
            while x:
                num += 2**x
                x -= 1
            return num
        pre_num = 2/precise
        wide = 1
        while True:
            if pre_num//(num_claculate(wide)) == 0:
                break
            wide += 1
        self.wide = wide
        self.population = Population(creature_num,wide*self.weight_number)

    def uncode(self):

        def gene_uncode(str):
            n = len(str)
            under = 2**n
            num = 0
            for i in str:
                num += 2**n
                n -= 1
            return (num/under)*2-1

        for animal in self.population.creature:
            for each in self.neural_network:
                for cell in each:
                    for i in range(len(cell.weight)):
                        gene = animal.gentic
                        weig_str = gene[0:self.wide]
                        gene = gene[self.wide:]
                        cell.weight[i] = gene_uncode(weig_str)
