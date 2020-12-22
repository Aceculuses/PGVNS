#!/user/bin/python3
from MathUtils import MathUtils
from MatrixUtils import MatrixUtils 

class MDLBasedDiscretization:

    #@para
    #double[][] data
    #int[] labels
    def buildDiscretizationModel(data,labels):
        #@para: int numClass
        numClass=labels[MathUtils().maxValueIndex(labels)]+1
        #@para: double[][] tdata
        tdata=MatrixUtils().transpose(data)
        #@para: double[][] cutPoint
        cutPoint=[[] for row in range(len(self.tdata))]
        for findex in range(0,len(tdata)):
            #@para: int[] sindices
            #Need to use ArrayUtils to convert double type array into int type array
            sindices=ArrayUtils().sort(tdata[findex])
            
