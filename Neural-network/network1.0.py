import random as rd
import math
import matplotlib.pyplot as plt
class Cell(object):

    def __init__(self,front):
        self.front = front
        weight = []
        error = []
        if self.front:
            for i in range(self.front):
                weight.append(2*rd.random()-1)
                error.append(0)
        self.weight = weight
        self.error = error
        self.bias = 2*rd.random()-1

    def forward(self,others):
        value = 0.0
        for i in range(self.front):
            value += self.weight[i] * others[i].value
        value += self.bias
        self.value = self.relu(value)

    def back_forward_outputlayer(self,others,target,l):

        for i in range(len(self.error)):
            self.error[i] = (self.value**2)*(1-self.value)*(self.value-target)
            self.weight[i] -= self.error[i]*l

    def back_forward(self,others_back,others_front,sn,l):
        error = 0.0
        for cell in others_back:
            error += cell.error[sn]
        for i in range(len(self.error)):
            self.error[i] = error*self.value*(1-self.value)*others_front[i].value
            self.weight[i] -= self.error[i] * l
        bias = error*self.value*(1-self.value)
        self.bias -= bias*0.1

    @classmethod
    def sigmod(ctl,x):
        return 1/(1+math.exp(-1*x))

    @classmethod
    def relu(ctl,x):
        if -1 < x < 0.3:
            return x
        else:
            return ctl.sigmod(x)

class Neural_network(object):

    def __init__(self,*structure):
        neural_network = []
        input_layer = []
        for i in range(structure[0]):
            input_layer.append(Cell(0))
        neural_network.append(input_layer)
        for i in range(1,len(structure)-1):
            hidden_layer = []
            for j in range(structure[i]):
                hidden_layer.append(Cell(structure[i-1]))
            neural_network.append(hidden_layer)
        output_layer = []
        for i in range(structure[-1]):
            output_layer.append(Cell(structure[-2]))
        neural_network.append(output_layer)
        self.neural_network = neural_network

    def forward(self,x):

        for each in range(len(self.neural_network[0])):
            self.neural_network[0][each].value = Cell.relu(x[each])

        for layer in range(1,len(self.neural_network)):
            for cell in self.neural_network[layer]:
                cell.forward(self.neural_network[layer-1])

    def back_forward(self,y,l):

        for each in range(len(self.neural_network[-1])):
            target =  Cell.sigmod(y[each])
            #target = y[each]
            self.neural_network[-1][each].back_forward_outputlayer(self.neural_network[-2],target,l)

        for layer in range(len(self.neural_network)-2,1,-1):
            for cell in range(len(self.neural_network[layer])):
                self.neural_network[layer][cell].back_forward(self.neural_network[layer+1],self.neural_network[layer-1],cell,l)

if __name__ != '__main__':
    network = Neural_network(4,6,3,1)
    l = 0.05
    X = []
    Y = []
    for i in range(1000):
        X.append([rd.random(), rd.random(),rd.random(),rd.random()])
        Y.append([X[i][0]+X[i][1]+X[i][2]+X[i][3]])
    for j in range(1000):
        for i in range(len(X)):
            network.forward(X[i])
            network.back_forward(Y[i],l)
    m = 0
    x_label = []
    y_label = []
    for i in range(100):
        x = [rd.random(), rd.random(), rd.random(), rd.random()]
        y = x[0] + x[1] + x[2] + x[3]
        network.forward(x)
        x_label.append(network.neural_network[-1][0].value)
        y_label.append(Cell.sigmod(y))
        #'''
        print(network.neural_network[-1][0].value,Cell.sigmod(y),network.neural_network[-1][0].value-Cell.sigmod(y))
        if -0.1<network.neural_network[-1][0].value-Cell.sigmod(y)<0.1:
            m += 1
            ''' 
        print(network.neural_network[-1][0].value, y, network.neural_network[-1][0].value - y)
        if -0.1 < network.neural_network[-1][0].value - y/4 < 0.1:
            m += 1
            '''
    print(m)
    '''
    plt.scatter(x_label,y_label,c='blue', s=16)
    plt.scatter(y_label, y_label, c='red', s=16)
    plt.show()
    '''
if __name__ == '__main__':
    network = Neural_network(3,5,3,1)
    l = 0.005
    X = []
    Y = []
    Z = []
    for i in range(100,500,20):
        for j in range(380,600,20):
            for k in range(60,70,5):
                X.append([(i-100)/400,(j-380)/220,(k-60)/10])
                Z.append(-1.440 * i + 0.74 * j + 9.449 * k + 0.001426 * i * j - 0.087 * k * k + 1187.391)
    max_y = max(Z)
    min_Y = min(Z)
    for each in Z:
        Y.append([(each - min_Y)/(max_y - min_Y)])
    for j in range(1000):
        '''
        for i in range(int(len(X)/2),len(X)):
            network.forward(X[i])
            network.back_forward(Y[i],l)
        '''
        for i in range(len(X)):
            network.forward(X[i])
            network.back_forward(Y[i],l)
    m = 0
    x_label = []
    z_label = []
    k_label = []
    X = []
    Y = []
    Z = []
    for i in range(300, 400, 20):
        for j in range(420, 500, 20):
            for k in range(60, 70, 5):
                v = [(i-300)/100,(j-420)/80,(k-60)/10]
                X.append(v)
                Z.append(-1.440 * i + 0.74 * j + 9.449 * k + 0.001426 * i * j - 0.087 * k * k + 1187.391)
    max_y = max(Z)
    min_Y = min(Z)
    for each in Z:
        Y.append(Cell.relu((each - min_Y)/(max_y - min_Y)))
    for i in range(len(X)):
        network.forward(X[i])
        k_label.append(network.neural_network[-1][0].value)
        #'''
        print(network.neural_network[-1][0].value,Y[i],network.neural_network[-1][0].value-Y[i])
        if -0.1<network.neural_network[-1][0].value-Y[i]<0.1:
            m += 1
            '''
        print(network.neural_network[-1][0].value, y, network.neural_network[-1][0].value - y)
        if -0.1 < network.neural_network[-1][0].value - y/4 < 0.1:
            m += 1
            '''
    print(m)
    #'''
    plt.scatter(k_label,Y,c='blue', s=16)
    plt.scatter(Y, Y, c='red', s=16)
    plt.show()
    #'''
