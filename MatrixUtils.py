#!/user/bin/python3

class MatrixUtils:

    def transpose(self,array):
        row=len(array)
        col=len(array[0])
        C=[[0 for lowD_col in range(row)] for highD_row in range(col)]
        for i in range(0,row):
            for j in range(0,col):
                C[j][i]=array[i][j]
        return C 

