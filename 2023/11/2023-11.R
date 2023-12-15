setwd('D:/python/advent/2023/11')

dat <- readLines('input.txt')
dat <- do.call(rbind, strsplit(dat, ''))

# numbers of expanding rows/columns prior to each row/column
row.exp <- cumsum(apply(dat == '.', 1, all))
col.exp <- cumsum(apply(dat == '.', 2, all))

for (exp.i in c(1, 10^6 - 1)) {
  ind <- which(dat == '#', arr.ind=T)
  ind[, 1] = ind[, 1] + row.exp[ind[, 1]] * exp.i
  ind[, 2] = ind[, 2] + col.exp[ind[, 2]] * exp.i
  cat(paste0('Part ', 2 - (exp.i==1), ': ', 
             sum(dist(ind, method='manh')), '\n'))
}