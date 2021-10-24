SFSearch <- function(shakedSolution,tddata,dv,label,dl){
  X <- shakedSolution
  bestScoe <- 0
  currentScore <- 0
  C <- J <- S <- Sx <- c()
  
  for(i in X){
    C <- append(C,i)
    Js <- CfsEvaluator(C,tddata,dv,label,dl)
    J <- append(J,Js)
    Jmax <- max(J)
    
    idx <- which(X == max(X))
    Xj <- X[idx]
    
    if(!(Xj %in% Sx)){
      Sx <- append(Sx,Xj)
      if(length(Sx) > 1){
        currentScore <- CfsEvaluator(Sx,tddata,dv,label,dl)
        if(currentScore > bestScoe){
          S <- Sx
          bestScoe <- currentScore
        }
      }
    }
  }
  return(S)
}
