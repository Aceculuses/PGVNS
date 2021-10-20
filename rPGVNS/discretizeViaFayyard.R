# iris_continuous <- readRDS('~/Desktop/iris_continuous.rds')
# label <- c(t(iris_continuous[5]))
# data <- iris_continuous[1:4]

buildDiscretizationModel <- function(data,label){
  sampleSize <- nrow(data)
  numClass <-max(unique(label)) + 1
  tdata <- t(data)
  first <- 1
  last <- sampleSize <- nrow(data)
  
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
  
  model <- pbapply::pblapply(seq_len(length(sfeatures)),
                             function(w){
                               left <- calculateCutPointsLeft(sfeatures[[w]],slabels[[w]],numClass,first,last)
                               right <- calculateCutPointsRight(sfeatures[[w]],slabels[[w]],numClass,first,last)
                               modelx <- unique(sort(append(left,right)))
                               if(length(modelx) == 0){
                                 modelx <- Inf
                               }
                               return(modelx)
                               }
                             )
  return(model)
}

discretizeViaFayyadModel <- function(data,label){
  
  print('Build Discretization Model')
  model <- buildDiscretizationModel(data,label)
  tdata <- t(data)
  
  print('Discretizing')
  discretizedModel <- pbapply::pbsapply(seq_len(nrow(tdata)),
                    function(w){
                      td <- tdata[w,]
                      m <- model[[w]]
                      
                      ds <- sapply(td, 
                             function(z){
                               length(which(z > m))
                             })
                      return(ds)
                      })
  rownames(discretizedModel) <- rownames(data)
  colnames(discretizedModel) <- colnames(data)
  return(discretizedModel)
}

splitTest <- function(pcounts,bcounts,numInstances,numCutPoints){
  priorEntropy <- entropy(pcounts)
  Entropy <- entropyConditionedOnRows(bcounts)
  Gain <- priorEntropy - Entropy
  # print(paste0('Gain: ',Gain) )
  numClassTotal <- length(which(pcounts > 0))
  numClassLeft <- length(which(bcounts[1,]>0))
  numClassRight <- length(which(bcounts[2,]>0))
  
  entropyLeft <- entropy(bcounts[1,])
  entropyRight <- entropy(bcounts[2,])
  
  delta <- log2(3^numClassTotal -2) - numClassTotal * priorEntropy - numClassRight * entropyRight - numClassLeft * entropyLeft
  delta <- (log2(numCutPoints) + delta) / numInstances
  # print(paste0('Delta: ',delta))
  return(Gain > delta)
}

         
 

