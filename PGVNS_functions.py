#from NumericConstant import NumericConstant
import math
from decimal import Decimal
import copy
import random

class PGVNS:
    
    def __init__(self):
        print('Initializing PGVNS objects')

#----------iris test data------------------------------
    iris_discrete = [[0,2,0,0],[0,1,0,0],[0,1,0,0],[0,1,0,0],[0,2,0,0],[0,2,0,0],[0,1,0,0],[0,1,0,0],[0,0,0,0],[0,1,0,0],
                     [0,2,0,0],[0,1,0,0],[0,1,0,0],[0,1,0,0],[1,2,0,0],[1,2,0,0],[0,2,0,0],[0,2,0,0],[1,2,0,0],[0,2,0,0],
                     [0,1,0,0],[0,2,0,0],[0,2,0,0],[0,1,0,0],[0,1,0,0],[0,1,0,0],[0,1,0,0],[0,2,0,0],[0,1,0,0],[0,1,0,0],
                     [0,1,0,0],[0,1,0,0],[0,2,0,0],[1,2,0,0],[0,1,0,0],[0,1,0,0],[1,2,0,0],[0,1,0,0],[0,1,0,0],[0,1,0,0],
                     [0,2,0,0],[0,0,0,0],[0,1,0,0],[0,2,0,0],[0,2,0,0],[0,1,0,0],[0,2,0,0],[0,1,0,0],[0,2,0,0],[0,1,0,0],
		     [1,1,1,1],[1,1,1,1],[1,1,2,1],[1,0,1,1],[1,0,1,1],[1,0,1,1],[1,1,1,1],[0,0,1,1],[1,0,1,1],[0,0,1,1],
		     [0,0,1,1],[1,1,1,1],[1,0,1,1],[1,0,1,1],[1,0,1,1],[1,1,1,1],[1,1,1,1],[1,0,1,1],[1,0,1,1],[1,0,1,1],
		     [1,1,2,2],[1,0,1,1],[1,0,2,1],[1,0,1,1],[1,0,1,1],[1,1,1,1],[1,0,2,1],[1,1,2,1],[1,0,1,1],[1,0,1,1],
		     [1,0,1,1],[1,0,1,1],[1,0,1,1],[1,0,2,1],[0,1,1,1],[1,1,1,1],[1,1,1,1],[1,0,1,1],[1,1,1,1],[1,0,1,1],
		     [1,0,1,1],[1,1,1,1],[1,0,1,1],[0,0,1,1],[1,0,1,1],[1,1,1,1],[1,0,1,1],[1,0,1,1],[0,0,1,1],[1,0,1,1],
		     [1,1,3,2],[1,0,2,2],[2,1,3,2],[1,0,3,2],[1,1,3,2],[2,1,3,2],[0,0,1,1],[2,0,3,2],[1,0,3,2],[2,2,3,2],
		     [1,1,2,2],[1,0,3,2],[1,1,3,2],[1,0,2,2],[1,0,2,2],[1,1,3,2],[1,1,3,2],[2,2,3,2],[2,0,3,2],[1,0,2,1],
		     [1,1,3,2],[1,0,2,2],[2,0,3,2],[1,0,2,2],[1,1,3,2],[2,1,3,2],[1,0,2,2],[1,1,2,2],[1,0,3,2],[2,1,3,1],
		     [2,0,3,2],[2,2,3,2],[1,0,3,2],[1,0,2,1],[1,0,3,1],[2,1,3,2],[1,1,3,2],[1,1,3,2],[1,1,2,2],[1,1,3,2],
		     [1,1,3,2],[1,1,2,2],[1,0,2,2],[1,1,3,2],[1,1,3,2],[1,1,3,2],[1,0,2,2],[1,1,3,2],[1,1,3,2],[1,1,2,2]] 
    
    iris_labels = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
		   1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,
		   2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2]

#----------Load Datasets---------------------------------
    def loadWineDataset(self):
        datasets = []
        file = open('/Users/guoping/Documents/PhD/Research/Algorithm/PGVNS/wine_continuous.txt','r').readlines()
        for i in file:
            j = i.rstrip('\n').split(',')
            for n in range(len(j)):
                j[n] = float(j[n])
            datasets.append(j)
        return datasets

    def loadWineLabels(self):
        labels = []
        file = open('/Users/guoping/Documents/PhD/Research/Algorithm/PGVNS/wine_labels.txt','r').readlines()
        for i in file:
            j = i.rstrip('\n').split(',')
            for m in range(len(j)):
                j[m] = int(j[m])
                labels.append(j[m])
        return labels

    def loadIrisDataset(self):
        file = open('/Users/guoping/Documents/PhD/Research/Algorithm/PGVNS/iris_continuous_features.txt','r').readlines()
        datasets = []
        for i in file:
            j = i.rstrip('\n').split(',')
            for n in range(len(j)):
                j[n] = float(j[n])
            datasets.append(j)
        return datasets

    def loadIrisLabels(self):
        labels = []
        k = []
        d ={}
        count = 0
        file = open('/Users/guoping/Documents/PhD/Research/Algorithm/PGVNS/iris_continuous_labels.txt','r').readlines()
        for i in file:
            x = i.rstrip('\n')
            if x not in k:
                k.append(x)
                d[x] = count
                count += 1
                labels.append(d[x])
            else:
                labels.append(d[x])
        return labels

#----------FCBFOverlappingBagSearch Parameters-----------
    tdata= ''
    dvalues = ''
    labels = ''
    lvalues = ''
    threshold = float(0)
    featureIdx = []
    MarkovBlanket = []
    featureCluster = {}
    kMax = ''
    numFeatures = ''
    numClass = ''
    cutPoints = ''
    predominantIndex = []
#----------MaxtrixUtil-----------------------------------  
    def transpose(self,A):
        m = len(A)
        n = len(A[0])
        C = [[0 for row in range(m)] for col in range(n)]
        for i in range(0,m):
            for j in range(0,n):
                C[j][i] = A[i][j]
        return C

    def maxValueIndex(self,L):
        maximum = 0
        maxIndex = 0
        for i in range(len(L)):
            if i == 0 or L[i] > maximum:
                maxIndex = i
                maximum = L[i]
        return maxIndex

    def getCategory(self, valueSpace, labelSpace):
        dict = {}
        k = []
        for i in range(len(labelSpace)):
            if labelSpace[i] not in k:
                dict[labelSpace[i]] = [valueSpace[i]]
                k.append(labelSpace[i])
            else:
                dict[labelSpace[i]].append(valueSpace[i])
        return dict

    def contingencyTable(self, valueSpace, dvalues, labelSpace, lvalues):
        ctable = [ [ 0 for n in range(len(lvalues))]  for m in range(len(dvalues)) ]
        C = self.getCategory(valueSpace, labelSpace)
        for i in lvalues:
            for j in dvalues:
#                print(dvalues.index(j))
#                print(lvalues.index(i))
                ctable[dvalues.index(j)][lvalues.index(i)] = C[i].count(j)
        return ctable
    
    def eq(self,a,b):
        if a-b < 1e-06 and b-a < 1e-06:
            return True 
        return False

#----------Discretization Methods-----------------------------
    def buildDiscretizationModel(self,data,labels):
        self.numClass = labels[self.maxValueIndex(labels)] + 1 
        tdata = self.transpose(data)
        cutPoints = [ '' for f in range(len(tdata)) ]
        # print(cutPoints)
        for findex in range(len(tdata)):
            sindices = self.sort(tdata[findex])
            sfeatures = [ '' for f in range(len(sindices)) ]
            slabels = [ '' for f in range(len(sindices)) ]
            #
            for i in range(len(data)):
                sfeatures[i] = tdata[findex][sindices[i]]
                slabels[i] = labels[sindices[i]]
            #
            cutPoints[findex] = self.calculateCutPoints(sfeatures,slabels,0,len(data))
            if cutPoints[findex] == []:
                cutPoints[findex] = [float('Inf')]
        self.model = cutPoints
        self.cutPoints = cutPoints
        #return self.model

    def calculateCutPoints(self,svalues,labels,first,last):
        #print('Self-calling')
        numCutPoints = 0
        pcounts = [ 0 for f in range(self.numClass)]
        for p in range(first,last):
            # 默认labels 是从0开始的
            pcounts[labels[p]] = pcounts[labels[p]] + 1
        ccounts = [ ['' for i in range(self.numClass)] for j in range(2) ]
        bcounts = [ ['' for i in range(self.numClass)] for j in range(2) ]
        ccounts[0] = [ 0 for i in range(self.numClass) ]
        ccounts[1] = copy.deepcopy(pcounts)
        #
        pentropy = self.entropy(pcounts)
        bentropy = pentropy
        #
        cpoints = []
        centropy = ''
        cpoint = ''
        bcpoint = ''
        numInstances = last - first
        bestIndex = -1
        #
        if last - first >= 2:
            for i in range(first,last-1):

                ccounts[0][labels[i]] = ccounts[0][labels[i]] + 1
                ccounts[1][labels[i]] = ccounts[1][labels[i]] - 1

                #print('Round',i,'pcounts:',pcounts)
                #print('Round',i,'ccounts:',ccounts)

                if svalues[i] < svalues[i+1]:
                    cpoint = (svalues[i] + svalues[i+1]) / 2

                    #print('Round',i, 'cpoint:',cpoint)

                    centropy = self.entropyConditionedOnRows(ccounts)

                    #print('Round',i, 'centropy:',centropy)
                    #print('Round',i,'betropy:',bentropy)
                    #print('Round',i,'centropy < bentropy:',centropy < bentropy)

                    if centropy < bentropy:
                        bcpoint = cpoint
                        bentropy = centropy
                        bestIndex = i
                        bcounts[0][0:self.numClass] = ccounts[0][0:self.numClass]
                        bcounts[1][0:self.numClass] = ccounts[1][0:self.numClass] 

                        #print('Round',i,'bcpoint:',bcpoint)
                        #print('Round',i,'bentropy:',bentropy)
                        #print('Round',i,'besIndex:',i)
                        #print('Round',i,'bcounts:',bcounts)
                        #print('Round',i,'bestIndex:',bestIndex,'\n')

                    #else:
                        #print('Round',i,'centropy < bentropy:',centropy < bentropy,'\n')

                    numCutPoints += 1
                    #print('Round',i,'numCutPoints:',numCutPoints,'\n')
            right = []
            gain = pentropy - bentropy

            #print('IG:',gain)
            #C = gain > 0 and self.splitTest(pcounts,bcounts,numInstances,numCutPoints)
            #print('Controller:',C)
            #print('*********************Original Input Above**************************\n')

            if gain > 0 and self.splitTest(pcounts,bcounts,numInstances,numCutPoints):
                left = self.calculateCutPoints(svalues,labels,first,bestIndex+1)
                ritgh = self.calculateCutPoints(svalues,labels,bestIndex+1,last)
                if left == [] and ritgh == []:
                    cpoints = ['']
                    cpoints[0] = bcpoint
                elif right == []:
                    cpoints = [ '' for f in range(len(left)+1)]
                    cpoints[0:len(left)] = left[0:len(left)]
                    cpoints[len(left)] = bcpoint
                elif left == []:
                    cpoints = [ '' for i in range(len(right)+1)]
                    cpoints[0] = bcpoint
                    cpoints[1:len(right)] = right[0:len(right)]
                else:
                    cpoints = [ '' for i in range(len(left)+len(right)+1)]
                    cpoints[0:len(left)] = left[0:len(left)]
                    cpoints[len(left)] = bcpoint
                    cpoints[len(left)+1:len(right)] = right[0:len(right)]
        return cpoints

    def splitTest(self,priorCounts,bestCounts,numInstances,numCutPoints):
        priorEntropy = self.entropy(priorCounts)
        entropy = self.entropyConditionedOnRows(bestCounts)
        gain = priorEntropy - entropy
        numClassTotal = 0
        for i in range(len(priorCounts)):
            if priorCounts[i] > 0:
                numClassTotal += 1
        #
        numClassLeft = 0
        for i in range(len(bestCounts[0])):
            if bestCounts[0][i] > 0:
                numClassLeft += 1
        #
        numClassRight = 0
        for i in range(len(bestCounts[1])):
            if bestCounts[1][i] > 0:
                numClassRight += 1
        #
        entropyLeft = self.entropy(bestCounts[0])
        entropyRight = self.entropy(bestCounts[1])
        delta = math.log(math.pow(3,numClassTotal) - 2,2) - numClassTotal * priorEntropy - numClassRight * entropyRight - numClassLeft * entropyLeft
        #print('Delt:',(math.log(numCutPoints,2) + delta) / numInstances)
        #print('Gain:',gain)
        return gain > (math.log(numCutPoints,2) + delta) / numInstances

    def discretize(self,iarray):
        oarray = [ '' for i in range(len(iarray))]
        for i in range(len(iarray)):
            index = 0
            currentValue = iarray[i]
            while index < len(self.cutPoints[i]) and currentValue >= self.cutPoints[i][index]:
                index += 1
            oarray[i] = index
        return oarray

    def discretizeViaFayyad(self,dataset,labels):
        self.buildDiscretizationModel(dataset,labels)
        points = dataset
        ddata =[ '' for f in range(len(points))]
        for r in range(len(points)):
            ddata[r] = self.discretize(points[r])
        return ddata

#----------StatUtils--------------------------------------
    def symmetricalUncertainty(self, ctable):
        ctotal = 0
        rtotal = 0
        columnEntropy = 0
        rowEntropy = 0
        entropyConditionedOnRows = 0
        infoGain = 0
        
        # Math 
        # Hx = (-1 / colSum) * [ i.SUM(Xi * log2(Xi)) - colSum * log2(colSum) ]
        # Hy = (-1 / rowSum) * [ i.SUM(Yi * log2(Yi)) - rowSum * log2(rowSum) ]
        # H(X|Y) = (-1 / rowSum) * { j.SUM [ i.SUM(Xij * log2(Xij)) - rowSum * log2(rowSum) ] }  

        # H(x)
        for i in range(len(ctable[0])):
            sumForColumn = 0
            for j in range(len(ctable)):
                sumForColumn += ctable[j][i]
            columnEntropy += self.xlogx(sumForColumn)
            ctotal += sumForColumn
        # Hx = (-1/ctotal) * (columnEntropy - self.xlogx(ctotal)) 
        Hx = columnEntropy - self.xlogx(ctotal)

        # H(Y) and H(X|Y)
        for i in range(len(ctable)):
            sumForRow = 0
            for j in range(len(ctable[0])):
                sumForRow += ctable[i][j]
                entropyConditionedOnRows += self.xlogx(ctable[i][j])
            rowEntropy += self.xlogx(sumForRow)
            rtotal += sumForRow
        # Hx_y = ( -1/rtotal) * (entropyConditionedOnRows - rowEntropy)
        # Hy = ( -1/rtotal) * (rowEntropy - self.xlogx(rtotal))
        Hx_y = entropyConditionedOnRows - rowEntropy
        Hy = rowEntropy - self.xlogx(rtotal)

        # IG(X|Y) = H(X) - H(X|Y)
        infoGain = Hx - Hx_y
 
        # SU(X,Y) = 2 * ( IG(X|Y) / ( H(X) + H(Y) ) )
        if self.eq(columnEntropy,float(0)) or self.eq(rowEntropy, float(0)):
            return float(0)

        # -1/ctotal = -1/rtotal
        SU = 2 * infoGain / (Hx + Hy)
        return SU
            
    def differentValues(self,A):
        aux = A.copy()
        aux.sort()
        vset = set()
        vset.add(aux[0])
        ref = aux[0]
        for i in range(1,len(aux)):
            if aux[i] != ref:
                ref =aux[i]
                vset.add(aux[i])
        values = list(vset)
        return values
    
    def xlogx(self,x):
        value=0
        #if x >= NumericConstant().DOUBLE_TYPE_PRECISION:
        if x > 0:
            value = x*math.log(x,2)
        return value

#    def log2(self,x):
#        y = float(1.4426950408889634) * math.log(x,2)
#        return y

    def eq(self,a,b):
        if a-b < 1e-06 and b-a < 1e-06:
            return True
        return False

    def entropy(self,histogram):
        sum = 0
        entropy = 0
        for i in range(len(histogram)):
            sum += histogram[i]
            entropy += self.xlogx(histogram[i])
        # Hx = (-1 / Sum) * [ i.SUM(Xi * log2(Xi)) - Sum * log2(Sum) ]
        if self.eq(sum,0):
            Hx = 0
        else:
            Hx = (-1 / sum) * (entropy - self.xlogx(sum)) 
        return Hx

    #def entropy2(self,histgram):
    #    entropy = 0
    #    sum = 0
    #    for i in range(len(histgram)):
    #        entropy -= self.xlogx(histgram[i])
    #        sum += histgram[i]
    #    if self.eq(sum,0):
    #        entropy = 0
    #    else:
    #        entropy = ( entropy + self.xlogx(sum)) / sum * float(0.6931471805599453)
    #    return entropy

    def entropyConditionedOnRows(self,ctable):
        entropyConditionedOnRows = 0
        total = 0
        rowEntropy = 0
        for i in range(len(ctable)):
            sumForRow = 0
            for j in range(len(ctable[0])):
                sumForRow += ctable[i][j]
                entropyConditionedOnRows += self.xlogx(ctable[i][j])
            rowEntropy += self.xlogx(sumForRow)
            total += sumForRow
        # Hx_y = ( -1/total) * (entropyConditionedOnRows - rowEntropy)
        Hx_y = (-1 / total) * (entropyConditionedOnRows - rowEntropy)
        return Hx_y

    #def entropyConditionedOnRows2(self,ctable):
    #    returnValue = 0
    #    total = 0
    #    for i in range(len(ctable)):
    #        sumForRow = 0
    #        for j in range(len(ctable[0])):
    #            returnValue = self.xlogx(ctable[i][j])
    #            total += sumForRow
    #        returnValue += -self.xlogx(sumForRow)
    #        total = sumForRow
    #    if self.eq(total,0):
    #        return 0
    #    return -returnValue / total * float(0.6931471805599453)

#----------FCBFOverlappingBagSearch Constructor-----------
    def setData(self,A):
        self.tdata = self.transpose(A)
        self.dvalues = [ '' for f in range(len(self.tdata)) ] 
        for i in range(len(self.tdata)):
            self.dvalues[i] = self.differentValues(self.tdata[i])
            self.featureIdx.append(i)

    def setLabels(self,labels):
        self.labels = labels
        self.lvalues = self.differentValues(self.labels)
 
    def setThreshold(self,threshold):
        self.threshold = threshold

    def setkMax(self,kMax):
        self.kMax = kMax

    def new(self,data,labels,threshold,kMax):
        self.setData(data)
        self.setLabels(labels)
        self.setThreshold(threshold)
        self.setkMax(kMax)

#----------ArrayUtil--------------------------------------
    #@para: double[] array
    def sort(self,array):
        #@para: int[] index
        #@para: int[] newIndex
        index=[0 for i in range(len(array))]
        newIndex=[0 for i in range(len(array))]
        Array=copy.deepcopy(array)
        for i in range(0,len(Array)):
            index[i]=i
            if math.isnan(Array[i])==True:
                Array[i]=0
        #return a index represents a sorted array
        #The index has not been sorted yet, and need to be sorted according to numEqual
        self.quickSort(Array,index,0,len(Array)-1)
        i=0
        #return a index represents a sorted index which represent a sorted array
        while i < len(index):
            numEqual=1
            for j in range(i+1,len(index)):
                if self.eq(Array[index[i]],Array[index[j]])== True:
                    numEqual+=1
            if numEqual > 1:
                helpIndex=[float('nan') for i in range(numEqual)]
                for j in range(0,numEqual):
                    helpIndex[j]=i+j
                self.quickSort(index,helpIndex,0,numEqual-1)
                for j in range(0,numEqual):
                    newIndex[i+j]=index[helpIndex[j]]
                i+=numEqual
                continue
            newIndex[i]=index[i]
            i+=1
        return newIndex
            
    #@para: double[][]array, int[] index, int left, int right
    def quickSort(self,array,index,left,right):
        if left < right:
            #@para: int middle
            key=self.partition(array,index,left,right)
            self.quickSort(array,index,left,key)
            self.quickSort(array,index,key+1,right)

    #@para: double[][] array, int[] index, int l, int r
    #Sort index element of array, not directly sort array
    def partition(self,array,index,l,r):
        pivot=array[index[l]]
        while l < r:
            while array[index[l]] < pivot and l < r:
                l+=1
            while array[index[r]] > pivot and l < r:
                r-=1
            if l < r:
                help=index[l]
                index[l]=index[r]
                index[r]=help
                l+=1
                r-=1
        if l == r and array[index[r]] > pivot:
            r-=1
        return r

#----------Greedy Predominant Groups Generator (GreedyPGG)-----------------------
#----------valuesSpace is Predominant Feature------------------------------------
#----------labelSpcae is Markov Blanket------------------------------------------
    def search(self):
        nfeatures = len(self.tdata)
        predominant = [  0 for f in range(nfeatures) ]
        suc = [ '' for f in range(nfeatures) ]
        for i in range(nfeatures):
            # SU(X,Y)
            # X is value Space, Y is label Space for all   
            ctable = self.contingencyTable(self.tdata[i], self.dvalues[i], self.labels, self.lvalues)
            suc[i] = self.symmetricalUncertainty(ctable)
        isuc = self.sort(suc)
        
        # wvalue = float(0)
        sux = ''

        # Start from the largest SU(Xi,Y) value
        index1 = nfeatures - 1
        att1 = isuc[index1]
        
        # bestSolution Contains All Predominant Features
        bestSolution = []

        # set featureCluster 
        for i in isuc:
            self.featureCluster[i] = set()
        
        nPreds = 0
        # Outer While Loop is for Detecting Each Predominant Feature
        # Threshold = 0 
        while index1 >= 0 and suc[att1] > self.threshold:
            # Only Features under evaluation have values 0
            if predominant[att1] == 0:
                # Mark Predominant Feature
                predominant[att1] = 1
                nPreds += 1
                blanket = set()
                bestSolution.append(att1)
                # wvalue += suc[att1]
                index2 = nfeatures -2
                att2 = isuc[index2]
                
                # Inner While Loop is for Finding Markov Blanket Values 
                # If SU(Xr1,Xr2) >= SU(Xr2,Y), Then Xr2 is a Markov Blanket value of Xr1
                while index2 >= 0 and suc[att2] > self.threshold:
                    if predominant[att2] != 1:
                        ctable = self.contingencyTable(self.tdata[att1], self.dvalues[att1], self.tdata[att2], self.dvalues[att2])
                        sux = self.symmetricalUncertainty(ctable)
                        if sux >= suc[isuc[index2]]:
                            predominant[att2] = 2
                            blanket.add(att2)
                            self.featureCluster[att1].add(att2)
                    index2 -= 1
                    att2 = isuc[index2]
                ##### PredFeatures: Markov Blanket #
                # {    Xr1:          [Xr2,Xr3],    #
                #      Xr4:          [Xr3] }       #
                ####################################
                self.MarkovBlanket.append(blanket)
            index1 -= 1
            att1 = isuc[index1]   
        self.MarkovBlanket = self.MarkovBlanket[0:nPreds]
        self.predominantIndex = predominant
        return bestSolution

#----------Greedy Forward Selection (Sequential Forward Search)-------
    def SFSearch(self,shakedSolution):
        X = shakedSolution
        bestScore = 0
        currentScore = 0
        C = []
        J = []
        S = []
        Sx = []

        for i in range(0,len(X)):
            C.append(X[i])
            Js = self.CfsEvaluator(C)
            J.append(Js)
            Jmax = max(J)
            #
            Xj = X[J.index(Jmax)]
            #
            if Xj not in Sx: 
                Sx.append(Xj)
                if len(Sx) > 1:
                    currentScore = self.CfsEvaluator(Sx)
                    if currentScore > bestScore:
                        S = copy.deepcopy(Sx)
                        bestScore = currentScore
        return S

#----------Correlation Based Feature Selection Evaluation Function------
    def correlation(self,idx):
        ctable = self.contingencyTable(self.tdata[idx], self.dvalues[idx], self.labels, self.lvalues)
        su = self.symmetricalUncertainty(ctable)
        return su

    def subCorrelation(self,f1,f2):
        ctable = self.contingencyTable(self.tdata[f1], self.dvalues[f1], self.tdata[f2], self.dvalues[f2])
        su = self.symmetricalUncertainty(ctable)
        return su

    def CfsEvaluator(self,featureIdx):
        num = 0
        denom = 0
        classCorrelation = {}
        
        # ∑SU(Xi,Y)
        for i in range(len(featureIdx)):
            idx = featureIdx[i]
            corr = self.correlation(idx)
            #classCorrelation[idx] = corr
            num += corr

        # 2 * ∑∑SU(Xi,Xj)
        larger = -1
        samller = -1
        if len(featureIdx) > 1:
            for j in range(len(featureIdx)):
                ifeature = featureIdx[j]
                denom += 1
                for k in range(j+1, len(featureIdx)):
                    jfeature = featureIdx[k]
                    if ifeature > jfeature:
                        larger = ifeature
                        samller = jfeature
                    else:
                        larger = jfeature
                        samller = ifeature
                    corr = self.subCorrelation(larger,samller)
                    denom += 2 * corr
        #
        if denom < 0:
            denom = denom * -1
        if denom == 0:
            return 0

        # J(S)
        merit = num / math.sqrt(denom)
        if merit < 0:
            merit = merit * -1
        return merit

#----------Variable Neighbourhood Search (VNS)---------------------
    def generateInitialSolution(self):
        solution = self.search()
        self.numFeatures = len(self.tdata)
        return solution

    def shakeSolution(self,currentSolution,shakeNumber):
        # featureIdx = [0,1,2,3] 
        # The index of features is equal to the  position of index
        # featureIdx = [0,1,2,3]
        #        idx :  0 1 2 3
        # for i in range(tnfeature):
        #      print(i)
        # i = 0,1,2,3
        S = copy.deepcopy(currentSolution)
        Sx= copy.deepcopy(currentSolution)
        G = []
        F = []
        
        s = len(currentSolution)
        # d can be whatever a integer.
        # d = len(tdata)
        d = len(self.tdata)

        # Loop times = shake number
        for k in range(shakeNumber):
            j = random.randint(0,d)
            if j < len(Sx):

                # Once Xj is popped out of S, then S becomes S'
                # Xj is added to a new list G 
                Xj = Sx.pop(j)
                G.append(Xj)

                # F contains all features in G except Xj
                F = G
                F.pop(F.index(Xj))

                #
                if len(F) > 0:
                    k = random.randint(0,len(F)-1)
                    Xk = F[k]
                    if Sx.count(Xk) == 0:
                        Sx.appen(Xk)
            else:
                stop = False
                while stop == False and len(Sx) < s:
                    r = random.randint(0,s - 1)
                    Xr = S[r]
                    if Sx.count(Xr) == 0:
                        Sx.append(Xr)
                        stop = True
        return Sx
 
#----------Main Function-------------------------------------------
    def VNS(self,shakeNumber):
        bestSolution = self.generateInitialSolution()
        k = 0
        bestScore = 0
        localScore = 0
        localSolution = []
        currentSolution = []
        while k <= self.kMax:
            #print('Iteration:',k)
            shakedSolution = self.shakeSolution(bestSolution,shakeNumber)
            bestScore = self.CfsEvaluator(bestSolution)
            #print('CheckPoint shakeSolution', k)

            #print('shakedSolution:',shakedSolution)
            
            if len(shakedSolution) < 1:
                k += 1
            else:
                #print('CheckPoint SFS:',k)
                #localSolution = self.SFSearch(shakedSolution,len(localSolution))
                
                localSolution = self.SFSearch(shakedSolution)
                #print('CheckPoint Compare:',k)
                if len(localSolution) < 1:
                    k += 1
                else:
                    localScore = self.CfsEvaluator(localSolution)
                    #print('bestScore',bestScore)
                    #print('localScore',localScore)
                    if localScore > bestScore:
                        bestSolution = localSolution
                        bestScore = localScore
                        k += 1
                    else:
                        k += 1
        return bestSolution






















