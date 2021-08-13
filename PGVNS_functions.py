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

#----------Discretion Methods-----------------------------
    def discretizeViaFayyad(self):
        

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

    def eq(self,a,b):
        if a-b < 1e-06 and b-a < 1e-06:
            return True
        return False

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
        return bestSolution

#----------Greedy Forward Selection (Sequential Forward Search)-------
    def SFSearch(self,shakedSolution,k):
        nfeatures = len(shakedSolution)
        bestSolution = []
        bestSolution.append(shakedSolution[0])
        solution = []
        solution.append(shakedSolution[0])
        Js = 0
        Jx = 0
        stop = False
        count = 1
        #
        #print('SFS Start:',k)
        #while stop == False and count < k:
        while count < k:
            #print('SFS count:',count)     
            for i in range(1, nfeatures):
                solution.append(shakedSolution[i])
                Js = self.CfsEvaluator(bestSolution)
                Jx = self.CfsEvaluator(solution)
                if Jx > Js:
                    Js = Jx 
                    bestSolution = solution
                    count += 1
                else:
                    count += 1
                    stop = True
        return bestSolution

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
        pfeatures = currentSolution
        #print(pfeatures)
        nfeatures = self.numFeatures
        stop = False
        for k in range(shakeNumber):
            pk = random.randint(0,nfeatures)
            if pk < len(pfeatures):
                rfeature = pfeatures.pop(pk)
                fblanket = self.featureCluster[rfeature]
                if len(fblanket) > 0:
                    pk = random.randint(0,len(fblanket)-1)
                    if list(fblanket)[pk] not in pfeatures:
                        pfeatures.append(list(fblanket)[pk])
            else:
                while stop == False and len(pfeatures) < nfeatures:
                    pk = random.randint(0,nfeatures-1)
                    if pk not in pfeatures:
                        pfeatures.append(pk)
                        stop = True
        shakedSolution = pfeatures
        return shakedSolution

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
            if len(shakedSolution) < 1:
                k += 1
            else:
                #print('CheckPoint SFS:',k)
                localSolution = self.SFSearch(shakedSolution,len(localSolution))

                #print('CheckPoint Compare:',k)
                if len(localSolution) < 1:
                    k += 1
                else:
                    localScore = self.CfsEvaluator(localSolution)
                    if localScore > bestScore:
                        bestSolution = localSolution
                        bestScore = localScore
                        k += 1
                    else:
                        k += 1
        return bestSolution






















