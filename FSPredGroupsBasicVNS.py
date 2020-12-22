#!/user/bin/python3
import random

class FSPredGroupsBasicVNS:
    numFeatures=-1
    random=None
    data=None
    values=None
    labels=None
    overlap=True
    isKmaxPct=True
    featureSpaceSearch=None
    cfsEvaluator=None
#this.random.nextInt(tnfeatures); 
#python random.randint(0,tnfeatures-1)   
#No seed is available for random
#FeatureBags featureSpaceSearch
    def __init__(self,idata,ilabels,cfsEvaluator):
        self.numFeatures=len(idata[0])
        self.data=idata
        self.labels=ilabels
        self.overlap=True
        self.cfsEvaluator=cfsEvaluator
    
    def 
