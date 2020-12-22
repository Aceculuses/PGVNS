#!/user/bin/python3
from StatUtils import StatUtils

class FCBFOverlappingBagSearch:

    tdata=None
    dvalues=None
    labels=None
    lvalues=None
        
    def __init__(self,tdata):
        self.tdata=tdata

    def setdvalues(self):
        #this.dvalues = new int[this.tdata.length][]
        self.dvalues=[[] for row in range(len(self.tdata))]
        for i in range(len(self.tdata)):
            dvalues[i]= StatUtils().differentValues(self.tdata[i])
        return dvalues

    def search(self):
        nfeatures=len(tdata)
        predominant=[]
        suc=[]
        for i in range(nfeatures):
            predominant[i]=0
            suc[i]=StatUtils().symmetricalUncertainty(self.tdata[i],len(self.dvalues[i]),self.labels,len(self.lvalues))
