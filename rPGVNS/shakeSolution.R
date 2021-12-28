# nfeature <- nrow(tddata)
# shakeNumber <- 10
# s1 <- search(tddata,dv,label,dl,nfeature)
# shakeSolution(s1,nfeature,shakeNumber)

shakeSolution <- function(currentSolution,nfeature,shakeNumber){
  S <- Sx <- currentSolution
  G <- F <- c()
  s <- length(currentSolution)
  d <- nfeature
  
  for ( k in seq_len(shakeNumber)){
    j <- sample(seq_len(d),1)
    #______________________
    if(j < length(Sx)){
      Xj <- Sx[j]
      Sx <- Sx[-j]
      
      G <- append(G,Xj)
      
      F <- G
      idx <- which(F == Xj)
      F <- F[-idx]
      
      #*****************
      if(length(F) > 0){
        w <- sample(seq_len(length(F)),1)
        Xw<- F[w]
        
        #!!!!!!
        if(!(Xw %in% Sx)){
          Sx <- append(Sx,Xw)
        }
        #!!!!!
        
      }
      #****************
      
    }#______________________
    else{
      stop <- FALSE
      while(stop == FALSE & length(Sx) < s){
        r <- sample(seq_len(s),1)
        Xr <- S[r]
        if(!(Xr %in% Sx)){
          Sx <- append(Sx,Xr)
          stop == TRUE
        }
      }
    }
  }
  return(Sx)
}
