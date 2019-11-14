import numpy as np
import math
import copy as cp

class FeedForwardNN(object):

    def __init__(self,inputNum,hiddenLayers,outputN):
        
        self.network = []
        self.networkOut = []
        self.networkDelta = []
        prevSize = inputNum
        for layerSize in hiddenLayers:
            tempLayer = np.random.rand(layerSize,prevSize+1)
            self.network.append(tempLayer)
            self.networkOut.append([0.0 for x in range(layerSize)]) 
            self.networkDelta.append([0.0 for x in range(layerSize)]) 
            prevSize = layerSize
        self.network.append(np.random.rand(outputN,prevSize+1))
        self.networkOut.append([0.0 for x in range(outputN)])
        self.networkDelta.append([0.0 for x in range(outputN)])

        #print(self.network)
        #print(self.networkOut)
    
    def sigmoid(self,x):
        return 1 / (1 + math.exp(0-x))


    def propagate_Forward(self,inputs):

        for i  in range(len(self.network)):
            for j in range(len(self.network[i])):
                if i == 0:
                    #print(inputs,self.network[0][j][:-1])
                    
                    self.networkOut[i][j] = self.sigmoid(np.dot(inputs,self.network[0][j][:-1])+self.network[0][j][-1] )
                else:
                    #print(inputs,self.network[i][j][:-1])
                    self.networkOut[i][j] = self.sigmoid(np.dot(inputs,self.network[i][j][:-1])+self.network[i][j][-1] )
            inputs = self.networkOut[i]

    def derivative(self,x):
        return x*(1.0-x)   

    def back_Propagate(self,expected):
        for i in reversed(range(len(self.network))):
            errors = []
            for j in range(len(self.network[i])):
                if i == len(self.network)-1:
                    errors.append(expected[j] - self.networkOut[i][j])
                else:
                    #print("error",i,j,self.networkDelta[i+1],self.network[i+1][:,j])
                    errors.append( np.dot(self.networkDelta[i+1],self.network[i+1][:,j]))
            #print(i,"\n",errors)    
            for j in range(len(self.network[i])):
                self.networkDelta[i][j] = errors[j]*self.derivative(self.networkOut[i][j])
    
    def update_Weights(self,inputs,l_rate):
        
        for i in range(len(self.network)):

            temp = np.zeros(np.shape(self.network[i]))
            delta = cp.copy(self.networkDelta[i])
            delta = np.reshape(delta,(len(delta),1))
            tempi = []
            if i==0:
                tempi = cp.deepcopy(inputs)
                tempi.append(1)
            else:
                tempi = cp.deepcopy(self.networkOut[i-1])
                tempi.append(1)    
            tempi = np.reshape(tempi,(1,len(tempi)))     
            
            #print(np.matmul(delta,tempi))
            temp = l_rate*np.matmul(delta,tempi)
            #print("before weight adjustment ")
            #print(self.network)
            #print("-------")
            self.network[i] = self.network[i] + temp
            #print(temp)

    def learn(self,l_rate,epoch,data):
        l = len(self.networkOut) 
        for e in range(epoch):

            for row in data:

                self.propagate_Forward(row[:-1])
            
                error = (self.networkOut[l-1][0]-row[-1])**2
                #print("error ",e," ",error)
                self.back_Propagate(row[-1:])
                self.update_Weights(row[:-1],l_rate)
                #print("------")


            

ff = FeedForwardNN(3,[2],1)
a = np.array([0.7,0.2,-0.5,-0.9])
b = np.array([0.4,-0.4,-0.5,-0.6])
c = np.array([0.7,0.4,0.8])
layer1 = np.zeros([2,4],float)
layer1[0] = a
layer1[1] = b
layer2 = np.zeros([1,3],float)
layer2[0] = c 
ff.network[0] = layer1
ff.network[1] = layer2
#print(ff.network)
print(ff.network)

ff.learn(0.5,20000,[[1.7,0.8,1.3,0.45]])
print(ff.network)
'''
ff.propagate_Forward([1.7,0.8,1.3])
ff.back_Propagate([0.45])

print(ff.networkDelta)
print(ff.networkOut)
ff.update_Weights([1.7,0.8,1.3],0.5)
print(ff.network)
'''