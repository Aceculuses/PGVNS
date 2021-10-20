calculateCutPointsLeft <- function(sfeatures,slabels,numClass,first,last){
  
  stop <- last
  bestIndex <- -1
  
  pcounts <- matrix(0,nrow = 1, ncol = numClass)
  for(p in seq(first,last)){
    pcounts[1,slabels[p]+1] <- pcounts[1,slabels[p]+1]+1
  }
  
  pentropy <- entropy(pcounts)
  bentropy <- pentropy
  
  ccounts <- bcounts <- matrix(0,nrow = 2, ncol = numClass)
  colnames(ccounts) <- colnames(bcounts) <- c(paste0('cluster_',seq_len(numClass)-1))
  rownames(ccounts) <- rownames(bcounts) <- c('c','p')
  ccounts[2,] <- pcounts
  
  numCutPoints <- 0
  numInstances <-  last - first + 1
  
  cpoints <- c()
  
  
  if(last - first >= 2){
    
    for(w in seq(first,last-1)){
      ccounts[1,slabels[w]+1] <- ccounts[1,slabels[w]+1] + 1
      ccounts[2,slabels[w]+1] <- ccounts[2,slabels[w]+1] - 1
      
      if(sfeatures[w] < sfeatures[w+1]){
        cpoint <- (sfeatures[w] + sfeatures[w+1]) / 2
        centropy <- entropyConditionedOnRows(ccounts)
        
        if(centropy < bentropy){
          bcpoint <- cpoint
          bentropy <- centropy
          bestIndex <- w
          bcounts <- ccounts
        }
        
        numCutPoints <- numCutPoints + 1
      }
    }
    right <- c()
    left <- c()
    gain <- pentropy - bentropy
    
    
    # print(paste0('besIndex: ',bestIndex))
    stop <- stop - 1
    # print(stop>bestIndex)
    
    if(gain > 0 & splitTest(pcounts,bcounts,numInstances,numCutPoints) & bestIndex < stop){
      left <-  calculateCutPointsLeft(sfeatures,slabels,numClass,first,bestIndex+1)
      
      if(length(left) == 0 & length(right) == 0){
        cpoints <- c()
        cpoints[1] <- bcpoint
      }
      else if(length(right) == 0){
        cpoints <- left
        cpoints <- append(cpoints,bcpoint)
      }
      else if(length(left) == 0){
        cpoints <- right
        cpoints <- append(bcpoint,cpoints)
      }
      else{
        cpoints <- left
        cpoints <- append(cpoints,bcpoint,right)
      }
    }
  }
  return(cpoints)
}

