#!/user/bin/python3
import copy
import math

class ArrayUtils:

    #@para: double[] array
    def sort(self,array):
        #@para: int[] index
        #@para: int[] newIndex
        index=[]
        newIndex=[]
        Array=copy.deepcopy(array)
        for i in range(0,len(Array)):
            index[i]=i
            if math.isnan(Array[i])==True:
                Array[i]=0
        self.quickSort(Array,index,0,len(Array)-1)
        i=0
        while i < len(index):
            numEqual=1
            pass

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
