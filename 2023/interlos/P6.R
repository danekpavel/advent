setwd('D:/python/advent/2023/interlos/')

inp <- unname(as.matrix(read.csv('bridge.txt', header=F)))


start <- c(1, 6)
around <- unname(as.matrix(expand.grid(-1:1, -1:1)[-5, ]))
path <- NULL
visited <- matrix(F, nrow(inp), ncol(inp))
solution <- NULL
visited[t(start)] <- T

go <- function(from, path) {
  
  n_now <- inp[t(from)]
  path <- c(path, n_now)
  
  if (from[1] == nrow(inp)) {
    
    # solution:
    print(path)
    solution <<- path
  }
  
  neigh <- t(from + t(around))
  # only existing fields
  neigh <- neigh[neigh[, 1] > 0 & neigh[, 1] <= nrow(inp) &
                   neigh[, 2] > 0 & neigh[, 2] <= ncol(inp), , drop=F]
  # number not on path yet
  neigh <- neigh[!(inp[neigh] %in% path), , drop=F]
  # not visited yet
  neigh <- neigh[!visited[neigh], , drop=F]
  
  visited[neigh] <<- TRUE
  for (i in seq_len(nrow(neigh))) {
    go(neigh[i, ], path)
  }
  visited[neigh] <<- FALSE
}

go(start, path)