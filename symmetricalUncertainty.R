
# ctable <- matrix(sample(seq_len(100),70), nrow = 10, ncol = 7)

symmetricalUncertainty <- function(ctable){

  # H(X) = (-1/Sum) * [ sum(Xi * log2(Xi)) - colSum * log2(colSum) ]
  # Marginal Entropy H(X)
  sumForColumn <- apply(ctable,2,sum)
  columnEntropy <-  sum(sapply(sumForColumn,xlogx))
  ctotal <-  sum(sumForColumn)
  Hx <-  columnEntropy - xlogx(ctotal)
  
  # H(Y) = (-1/Sum) * [ sum(Yi * log2(Yi)) - rowSum * log2(rowSum) ]
  # Marginal Entropy H(Y)
  sumForRow <- apply(ctable,1,sum)
  rowEntropy <-  sum(sapply(sumForRow,xlogx))
  rtotal <-  sum(sumForRow)
  Hy <- rowEntropy - xlogx(rtotal)
  
  # H(X|Y) = (-1/Sum) * sum.i[sum.j(Xij * log2(Xij)) - rowSum.i * log2(rowSum.i)]   
  # i: row
  # j: column
  # Conditional Entropy H(X|Y)
  eachEntropyConditionedOnRows <- apply(ctable,1,
                                    function(w){
                                      rowSum <- sum(w)
                                      sum(sapply(w, xlogx)) - rowSum * xlogx(rowSum) 
                                    })
  Hx_y <- sum(eachEntropyConditionedOnRows)
  
  # IG(X|Y) = H(X) - H(X|Y)
  infoGain <-  Hx - Hx_y
  
  if(eq(columnEntropy,0) | eq(rowEntropy, 0)){
   return(0) 
  }
  
  # SU(X,Y) = 2 * IG(X|Y) / (H(X) + H(Y)) 
  SU = 2 * infoGain / (Hx + Hy)
  return(SU)
}

xlogx <- function(x){
  value = 0
  if(x>0){
    value = x * log2(x)
  }
  return(value)
}

eq <- function(a,b){
  if(a - b < 1e-6 & b - a < 1e-6){
    return(TRUE)
  }
  return(FALSE)
}