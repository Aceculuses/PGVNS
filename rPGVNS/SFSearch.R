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
# shakedSolution <- shakeSolution(bestSolution,nfeature,shakeNumber)
# localSolution <- SFSearch(shakedSolution,tddata,dv,label,dl)

SFSearch <- function(shakedSolution,tddata,dv,label,dl){
  X <- shakedSolution
  bestScore <- 0
  currentScore <- 0
  C <- J <- S <- Sx <- c()
  
  for(i in X){
    C <- append(C,i)
    Js <- CfsEvaluator(C,tddata,dv,label,dl)
    J <- append(J,Js)
    Jmax <- max(J)
    
    idx <- which(J == max(J))
    Xj <- X[idx]
    
    if(!(Xj %in% Sx)){
      Sx <- append(Sx,Xj)
      if(length(Sx) > 0){
        currentScore <- CfsEvaluator(Sx,tddata,dv,label,dl)
        if(currentScore > bestScore){
          S <- Sx
          bestScore <- currentScore
        }
      }
    }
  }
  return(S)
}
