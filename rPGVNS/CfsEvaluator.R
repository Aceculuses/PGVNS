# # Test
# iris_continuous <- readRDS('~/Desktop/iris_continuous.rds')
# label <- c(t(iris_continuous[5]))
# data <- iris_continuous[1:4]
# ddata <- discretizeViaFayyadModel(data,label)
# tddata <- t(ddata)
# nfeature <- nrow(tddata)
# dl <- sort(unique(label))
# dv <- lapply(seq_len(nfeature), function(w){sort(unique(tddata[w,]))})
# #
# bestSolution <- search(tddata,dv,label,dl,nfeature)
# shakeNumber <- 10
# shakeSolution <- shakeSolution(bestSolution,nfeature,shakeNumber)
# #
# bestScore <- CfsEvaluator(bestSolution,tddata,dv,label,dl)


CfsEvaluator <- function(bestSolution,tddata,dv,label,dl){
  num <- 0
  denome <- 0
  
  for(i in bestSolution){
    corr <- correlation(tddata[i,],dv[[i]],label,dl)
    num <- num + corr
  }
  
  corr.dim <- length(bestSolution)
  corr.matrix <- diag(ncol = corr.dim, nrow = corr.dim)
  corr.matrix[lower.tri(corr.matrix)] <- 1
  bestSolution <- sort(bestSolution,decreasing = TRUE)
  
  if(length(bestSolution) > 0){
    for(i in seq_len(corr.dim)){
      d <- corr.matrix[i,corr.dim]
      if( d == 0 ){
        large <- bestSolution[i]
        empty <- which(corr.matrix[i,] == 0)
        r <- sapply(empty,
                    function(w){
                      small <- bestSolution[w]
                      corr <- subCorrelation(tddata[large,],dv[[large]],tddata[small,],dv[[small]])
                      return(corr)
                      })
        z <- which(corr.matrix[i,] == 0)
        corr.matrix[i,z] <- r
      }
    }
  }
  
  denome <- nrow(corr.matrix)
  t <- upper.tri(corr.matrix)
  denome <- denome + sum(corr.matrix[t]) * 2
  
  if(denome < 0){
    denome <- denome * -1
  }else if(denome == 0){return(0)}
  
  merit <- num / sqrt(denome)
  if(merit < 0){merit <- merit * -1}
  
  return(merit)
}


correlation <- function(tddatax,dvx,label,dl){
  ctable <- contingencyTable(tddatax,dvx,label,dl)
  su <- symmetricalUncertainty(ctable)
  return(su)
}

subCorrelation <- function(tddata1,f1,tddata2,f2){
  ctable <- contingencyTable(tddata1,f1,tddata2,f2)
  su <- symmetricalUncertainty(ctable)
  return(su)
}
