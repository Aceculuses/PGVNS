# iris_continuous <- readRDS('~/Desktop/iris_continuous.rds')
# label <- c(t(iris_continuous[5]))
# data <- iris_continuous[1:4]
# ddata <- discretizeViaFayyadModel(data,label)
# shakeNumber <- 10
# kMax <- 50

VNS <- function(ddata,label,shakeNumber,kMax){
  tddata <- t(ddata)
  nfeature <- nrow(tddata)
  dl <- sort(unique(label))
  dv <- lapply(seq_len(nfeature), 
               function(w){
                 sort(unique(tddata[w,]))
               })
  
  bestSolution <- search(tddata,dv,label,dl,nfeature)
  
  k <- 0
  bestScore <- 0
  localScore <- 0
  
  Best <- pbapply::pblapply(kMax,function(K){
    while(k <= K){
      shakedSolution <- shakeSolution(bestSolution,nfeature,shakeNumber)
      bestScore <- CfsEvaluator(bestSolution,tddata,dv,label,dl)
      
      if(length(shakeSolution) < 1){
        k <- k +1
      }else{
        localSolution <- SFSearch(shakedSolution,tddata,dv,label,dl)
        
        if(length(localSolution) < 1){
          k <- k +1
        }else{
          localScore <- CfsEvaluator(localSolution,tddata,dv,label,dl)
          if(localScore > bestScore){
            bestSolution <- localSolution
            bestScore <- localScore
            k <- k + 1
          }else{
            k <- k + 1
          }
        }
      }
      
      return(bestSolution)
      }
  })
  
  BestSol <- Best[[length(Best)]]
  return(BestSol)
}