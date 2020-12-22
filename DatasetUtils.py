#!/user/bin/python3


class DatasetUtils:

    def read_csv(csv):
        file=open(csv,'r').readlines()
        array=[]
        merge=[]
        for i in file:
            j=i.rstrip('\n').split(',')
            for v in j:
                merge.append(v)
        for k in range(0,len(merge),4):
                array.append(merge[k:k+4])
        return array
