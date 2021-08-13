# Predominant Group Variable Neighbourhood Search Algorithm

Usage
```
from PGVNS_functions import PGVNS
p = PGVNS()

# Discrete dataset
data=p.iris_discrete
labels = p.iris_labels
p.new(data,labels,threshold=0,kMax=100)
Result = p.VNS(shakeNumber=10)

# Continuous dataset
data = p.loadWineDataset()
labels = p.loadWineLabels()
```

**Reference**
-----------------------------------------
García-Torres, M., Gómez-Vela, F., Melián-Batista, B. and Moreno-Vega, J.M., 2016. High-dimensional feature selection via feature grouping: A Variable Neighborhood Search approach. Information Sciences, 326, pp.102-118.
