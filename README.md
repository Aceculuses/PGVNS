# Predominant Group Varaible Neighbourhood Selection Algorithm

Usage
```
from PGVNS_functions import PGVNS
p = PGVNS()
data=p.iris_discrete
labels = p.iris_labels
p.new(data,labels,threshold=0,kMax=100)

Result = p.VNS(shakeNumber=10)
```

**Reference**
-----------------------------------------
García-Torres, M., Gómez-Vela, F., Melián-Batista, B. and Moreno-Vega, J.M., 2016. High-dimensional feature selection via feature grouping: A Variable Neighborhood Search approach. Information Sciences, 326, pp.102-118.
