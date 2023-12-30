setwd('D:/python/advent/2023/interlos/')

inp <- readLines('semafory_test.txt')
tmp <- as.numeric(strsplit(inp[1], ' ')[[1]])
I <- tmp[1]
J <- tmp[2]

green <- matrix(T, J, I)
tmp <- as.numeric(unlist(strsplit(inp[2:(2+J-1)], ',| ')))
times <- matrix(tmp[(seq_along(tmp) %% 2) == 1], J, byrow=T)
phis <- matrix(tmp[(seq_along(tmp) %% 2) == 0], J, byrow=T)

# not finished...