#from NumericConstant import NumericConstant
import math
from decimal import Decimal
import copy
import random

class SU:
    
    def __init__(self):
        print('Initializing SU objects')

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
        if set(lvalues) - set(C.keys()) != set():
            for i in set(lvalues):
                C[i] = []
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

#----------StatUtils--------------------------------------
    def symmetricalUncertainty(self, ctable):
        ctotal = 0
        rtotal = 0
        columnEntropy = 0
        rowEntropy = 0
        entropyConditionedOnRows = 0
        eachEntropyConditionedOnRows = 0
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

#----------Correlation Based Feature Selection Evaluation Function------
    def correlation(self,idx):
        ctable = self.contingencyTable(self.tdata[idx], self.dvalues[idx], self.labels, self.lvalues)
        su = self.symmetricalUncertainty(ctable)
        return su

    def subCorrelation(self,f1,f2):
        ctable = self.contingencyTable(self.tdata[f1], self.dvalues[f1], self.tdata[f2], self.dvalues[f2])
        su = self.symmetricalUncertainty(ctable)
        return su


















