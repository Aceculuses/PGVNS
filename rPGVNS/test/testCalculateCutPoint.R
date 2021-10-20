# Data
iris_continuous <- readRDS('~/Desktop/iris_continuous.rds')
label <- c(t(iris_continuous[5]))
data <- iris_continuous[1:4]
tdata <- t(data)

sindices <- lapply(seq_len(nrow(tdata)), 
                   function(w){
                     order(tdata[w,])
                   }
)

sfeatures <- lapply(seq_len(nrow(tdata)), 
                    function(w){
                      sort(tdata[w,])
                    }
)

slabels <- lapply(seq_len(nrow(tdata)),
                  function(z){
                    idx <- sindices[[z]]
                    label[idx]
                  }
)

sf <- sfeatures[[1]]
sl <- slabels[[1]]
numClass <-max(unique(label)) + 1
first <- 1
last <- sampleSize <- nrow(data)


# Calculate Cut Points
calculateCutPoints <- function(sfeatures,slabels,numClass,first,last){
  print('Open this function')
  
  pcounts <- matrix(0,nrow = 1, ncol = numClass)
  for(p in seq(first,last)){
    pcounts[1,slabels[p]+1] <- pcounts[1,slabels[p]+1]+1
  }
  # print(paste0('pcounts: ',pcounts))
  
  pentropy <- entropy(pcounts)
  bentropy <- pentropy
  
  ccounts <- bcounts <- matrix(0,nrow = 2, ncol = numClass)
  colnames(ccounts) <- colnames(bcounts) <- c(paste0('cluster_',seq_len(numClass)-1))
  rownames(ccounts) <- rownames(bcounts) <- c('c','p')
  ccounts[2,] <- pcounts
  
  numCutPoints <- 0
  numInstances <-  last - first + 1
  
  cpoints <- c()
  
  bestIndex <- -1
  
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
    print(paste0('gain:',gain))
    
    # tf <- gain > 0 & splitTest(pcounts,bcounts,numInstances,numCutPoints)
    # print(paste0('tf: ',tf))
    print(paste0('bestIndex: ',bestIndex))
    if(gain > 0 & splitTest(pcounts,bcounts,numInstances,numCutPoints)){
      # left <-  calculateCutPoints(sfeatures,slabels,numClass,first,bestIndex+1)
      
      # print(paste0('bestIndex: ',bestIndex))
      # print(paste0('left: ',left))

      right <-  calculateCutPoints(sfeatures,slabels,numClass,bestIndex+1,last)
      
      if(length(left) == 0 & length(right) == 0){
        cpoints <- c()
        cpoints[1] <- bcpoint
        print(cpoints)
      }
      else if(length(right) == 0){
        cpoints <- left
        cpoints <- append(cpoints,bcpoint)
        print(cpoints)
      }
      else if(length(left) == 0){
        cpoints <- right
        cpoints <- append(bcpoint,cpoints)
        print(cpoints)
      }
      else{
        cpoints <- left
        cpoints <- append(cpoints,bcpoint,right)
        print(cpoints)
      }
    }
  }
  return(cpoints)
}

# Debug
stdout2 <- vector('character')
con2    <- textConnection('stdout2', 'wr', local = TRUE)
sink(con2)
calculateCutPoints(sf,sl,numClass,first,last)
sink()
View(stdout2)


calculateCutPoints(sf,sl,numClass,first,last)

calculateCutPoints(sf,sl,numClass,first,last)
