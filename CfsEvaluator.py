#!/user/bin/python3
import math
#Turn data into 2d matrix with matrix[total#150][total#4], 150x4
def prepareData(toyData):
    iris_discrete=[]
    merge=[]
    for i in toyData:
        x=i.rstrip('\n').split(',')
        for feature in x:
            merge.append(feature)
    for k in range(0,len(merge),4):
        iris_discrete.append(merge[k:k+4])
    return iris_discrete

def prepareLabel(iris_labels):
    labels=[]
    for i in iris_labels:
        j=i.rstrip('\n').split(',')
        for x in j:
            labels.append(x)
    return labels
#----------------------------------------------------------------
class CfsEvaluator:
    tdata=None
    nvalues=[]
    labels=None
    lvalues=-1
    correlation=[]
    classCorrelation=[]

    def __init__(self,data,labels):
        self.tdata=self.transpose(data)
        self.nvalues=self.setNvalues(data)
        self.labels=labels
        self.lvalues=self.setLvalues(labels)
        
    def setNvalues(self,data):
         nvals=[]
         for f in range(0,len(self.tdata)):
             nvals.append(int(self.maxValueIndex(self.tdata[f]))+1)
         return nvals

    def setLvalues(self,labels):
        lvalues=int(labels[self.maxValueIndex(labels)])+1
        return lvalues
#------------------------------------
#Initialize of
#------------------------------------
#Transpose matrix[#150][#4] into matrix[#4][#150]
#                  |    |                |    |
#Dimension:      high  low             high  low
    def transpose(self,array):
       #m=150, n=4
        m=len(array)
        n=len(array[0])
        C=[[0 for lowD_col in range(m)] for highD_row in range(n)]
        for i in range(0,m):
            for j in range(0,n):
                C[j][i]=array[i][j]
        return C

    def maxValueIndex(self,array):
        maximum=0
        maxIndex=0
        for i in range(0,len(array)):
            if i == 0 or array[i] > maximum:
                maxIndex=i
                maximum=array[i]
        return int(maxIndex)

    def buildEvaluator(self):
        nfeatures=len(self.tdata)
        for i in range(0,nfeatures):
            self.classCorrelation.append(float('nan'))
        #initialize correlation matrix
        #[1]
        #[nan,1]
        #[nan,nan,1]
        for i in range(nfeatures):
            l=list(range(i+1))
            for j in range(len(l)):
                l[j]=float('nan')
                l[-1]=1
            self.correlation.append(l)    
    

if __name__=='__main__':
    toyData=open('iris_discrete.txt','r').readlines()
    iris_labels=open('iris_label.txt','r').readlines()
    data=prepareData(toyData)
    labels=prepareLabel(iris_labels)
    cfsEvaluator=CfsEvaluator(data,labels)
    cfsEvaluator.buildEvaluator()
#cfsEvaluator object has been created

