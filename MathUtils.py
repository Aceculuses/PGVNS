#!/user/bin/python3

class MathUtils:

    #@para
    #int[] array
    def maxValueIndex(array):
        maximum=0
        maxIndex=0
        for i in range(0,len(array)):
            if i == 0 or array[i] > maximum:
                maxIndex=i
                maximum=array[i]
        return int(maxIndex) 
