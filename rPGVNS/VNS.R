# iris_continuous <- readRDS('~/Desktop/iris_continuous.rds')
# label <- c(t(iris_continuous[5]))
# data <- iris_continuous[1:4]
# ddata <- discretizeViaFayyadModel(data,label)
# shakeNumber <- 10
# kMax <- 50

# V <- VNS(ddata,label,shakeNumber,100)

VNS <- function(ddata,label,shakeNumber,kMax){
  shakeNumber <- shakeNumber
  kMax <- kMax
  tddata <- t(ddata)
  nfeature <- nrow(tddata)
  dl <- sort(unique(label))
  dv <- lapply(seq_len(nfeature), 
               function(w){
                 sort(unique(tddata[w,]))
               })
  
  message('Generate initial solution')
  O <- search2(tddata,dv,label,dl,nfeature)
  bestSolution <- rownames(O$predominant_group)
  
  k <- 0
  bestScore <- 0
  localScore <- 0
  
  
  message('Combinatorial optimization and global optimization with variable neighborhood search')
    while(k <= kMax){
      message('    Iteration ',k)
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
    }
  
  message('---SUCCESS---\n')
  
  Out <- list('initial_solution' = O, 'best_solution' = bestSolution)
  return(Out)
}
