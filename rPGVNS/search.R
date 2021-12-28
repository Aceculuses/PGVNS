# iris_continuous <- readRDS('~/Desktop/iris_continuous.rds')
# label <- c(t(iris_continuous[5]))
# data <- iris_continuous[1:4]
# ddata <- discretizeViaFayyadModel(data,label)
# tddata <- t(ddata)

contingencyTable <- function(features,dv,label,dl){
  ctable <- matrix(0,nrow = length(dv), ncol = length(dl))
  rownames(ctable) <- dv
  colnames(ctable) <- dl
  
  for (w in seq_len(length(label))){
    r <- which(dv == features[w])
    c <- which(dl == label[w])
    
    ctable[r,c] <- ctable[r,c] + 1
  }
  return(ctable)
}

search <- function(tddata,dv,label,dl,nfeature){

  # SU(X1,Y), Su(X2,Y), SU(X3,Y)......Su(Xn,Y)
  message('Calculating global symmetrical uncertainty: SU(xi, Y)')
  suc <- sapply(seq_len(nfeature),
                function(w){
                  ctable <- contingencyTable(tddata[w,],dv[[w]],label,dl)
                  sucx <- symmetricalUncertainty(ctable)
                  return(sucx)
                }
              )
  message('Done!')

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

  message('Start searching...')
  while(index1 >= 1 & suc[att1] > threshold){
    message('    Searching feature ',index1)
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
        if(index2 == 0){
          break
        }else{
          att2 <- isuc[index2]
        }
      }
      #--------------------------------------------------------------------------------
    }
    #**********************************************************************************
    index1 <- index1 - 1
    if(index1 == 0){
      break
    }else{
      att1 <- isuc[index1]
    }
  }

  # Return the index of features
  return(bestSolution)
}


search2 <- function(tddata,dv,label,dl,nfeature){
  
  #---------------------------- Part 1 -----------------------------------------
  # SU(X1,Y), Su(X2,Y), SU(X3,Y)......Su(Xn,Y)
  message('Calculating global symmetrical uncertainty: SU(xi, Y)')
  suc <- sapply(seq_len(nfeature), 
                function(w){
                  ctable <- contingencyTable(tddata[w,],dv[[w]],label,dl)
                  sucx <- symmetricalUncertainty(ctable)
                  return(sucx)
                }
  )
  message('---SUCCESS---\n')
  
  #----------------------------- Part 2 ----------------------------------------
  message('Calculating similarity matrix between each feature using symmetrical uncertainty')
  
  EE <- pbapply::pblapply(seq_len(nfeature-1), function(w){
    v1 <- tddata[w,]
    k <- w+1
    
    E <- sapply(seq(from = k, to = nfeature),function(h){
      v1.uniqs <- sort(unique(v1))
      v2 <- tddata[h,]
      v2.uniqs <- sort(unique(v2))
      ee <- subCorrelation(v1,v1.uniqs,v2,v2.uniqs)
      return(ee)
    })
    return(E)
  }
  )
  
  A <- diag(nrow(tddata))
  A[upper.tri(A)] <- 1
  diag(A) <- 0
  
  for (K in seq_len(nrow(tddata)-1)) {
    A[K, A[K, ] == 1] = EE[[K]]
  }
  
  M <- A + t(A)
  diag(M) <- 1
  colnames(M) <- seq_len(nrow(tddata))
  message('---SUCCESS---\n')
  
  #----------------------------- Part 3 ----------------------------------------
  message('Searching the best solution with greedy predominant groups generator')
  sux <- order(suc, decreasing = TRUE)
  predominant <- as.vector(rep(0,nfeature))
  blanket <- matrix(0,ncol = nfeature,nrow = nfeature)
  
  for(d in seq_len(length(predominant))){
    feature <- sux[d]
    if(predominant[feature] == 0){
      # SU(Xi,Xj) >= SU(Xj,Y)
      markov <- which(as.numeric(M[feature,]) >= suc)
      predominant[markov] <- 2
      predominant[feature] <- 1
      
      # Markov blanket 
      blanket[feature,markov] <- 2
      blanket[feature,feature] <- 0
    }
  }
  
  colnames(blanket) <- rownames(blanket) <- rownames(tddata)
  Markovblanket <- blanket[which(predominant == 1),]
  diff <- setdiff(colnames(Markovblanket),rownames(Markovblanket))
  Markovblanket <- Markovblanket[,diff]
  
  message('---SUCCESS---\n')
  
  O <- list('global_symmetrical_uncertainty' = suc, 
            'similarity_matrix' = M, 
            'predominant_feature' = predominant,
            'predominant_group' = Markovblanket)
  
  return(O)
}

