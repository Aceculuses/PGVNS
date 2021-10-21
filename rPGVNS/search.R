# iris_continuous <- readRDS('~/Desktop/iris_continuous.rds')
# label <- c(t(iris_continuous[5]))
# data <- iris_continuous[1:4]
# ddata <- discretizeViaFayyadModel(data,label)
# tddata <- t(ddata)
# 
# features <- tddata[1,]
# dv <- sort(unique(tddata[1,]))
# dl <- sort(unique(label))

# ddata <- discretizeViaFayyadModel(data,label)

contingencyTable <- function(features,dv,label,dl){
  ctable <- matrix(0,nrow = length(dv), ncol = length(dl))
  rownames(ctable) <- dv
  colnames(ctable) <- dl
  
  for (w in seq_len(length(label))){
    # As label start from 0, need to increase to 1
    w <- w + 1
    ctable[features[w],label[w]] <- ctable[features[w],label[w]] + 1
  }
  return(ctable)
}

search <- function(ddata,label){
  tddata <- t(ddata)
  nfeature <- nrow(tddata)
  dl <- sort(unique(label))
  
  #
  dv <- lapply(seq_len(nfeature), 
               function(w){
                 sort(unique(tddata[w,]))
               }
              )
  
  # SU(X1,Y), Su(X2,Y), SU(X3,Y)......Su(Xn,Y)
  suc <- sapply(seq_len(nfeature), 
                function(w){
                  ctable <- contingencyTable(tddata[w,],dv[[w]],label,dl)
                  sucx <- symmetricalUncertainty(ctable)
                  return(sucx)
                }
              )
  # 
  isuc <- order(suc)
  index1 <- nfeature
  
  # att1 is with the larget SU.
  att1 <- isuc[nfeature]
  
  # predominant is the marker matrix which keep features record
  # 0 is for feature to be measured.
  # 1 is for predominant feature
  # 2 is for markove blanket feature
  predominant <- matrix(0,nrow = 1, ncol = nfeature)
  
  # Threshold can be adjusted
  threshold <- 0
  
  # Counting the number of predominant features
  nPreds <- 0
  bestSolution <- c()
  while(index1 >= 1 & suc[att1] > threshold){
    
    #****************************************
    if(predominant[att1] == 0){
      predominant[att1] <- 1
      nPreds <- nPreds + 1
      bestSolution <- append(bestSolution,att1)
      
      # The Second Largest SU
      index2 <- nfeature - 1
      att2 <-  isuc[index2]
      
      #----------------- Compare SU(X,Y) and SU(Xi,Xj) -------------------------------- 
      while (index2 >=1 & suc[att2] > threshold){
        # print(paste0('index2: ',index2))
        if(predominant[att2] != 1){
          ctable <- contingencyTable(tddata[att1,],dv[[att1]],tddata[att2,],dv[[att2]])
          sux <- symmetricalUncertainty(ctable)
          
          # Whether att2 is in Markov Blanket of att1.
          # sux = SU(att1,att2), SU(att2,class)
          # if SU(att1,att2) > SU(att2,class)
          # att2 is in Markov Blanket of att1 which given by 2 as notation.
          if(sux >= suc[isuc[att2]]){
            predominant[att2] <- 2
          }
        }
        index2 <- index2 - 1
        if(index2 == 0) break
        att2 <- isuc[index2]
      }
      #--------------------------------------------------------------------------------
    }
    #**********************************************************************************
    index1 <- index1 - 1
    if(index1 == 0) break
    att1 <- isuc[index1]
  }
  return(bestSolution)
}

