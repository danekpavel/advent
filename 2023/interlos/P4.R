setwd('D:/python/advent/2023/interlos/')

los = '#.#....#.#
###....###
..######..
...####...'
los <- do.call(rbind, strsplit(strsplit(los, '\n')[[1]], split=''))
los[] <- los == '#'
mode(los) <- 'logical'
lw <- nrow(los)
lh <- ncol(los)

inp <- readLines('photo.txt')
inp <- do.call(rbind, strsplit(inp, split=''))
inp[] <- inp == '#'
mode(inp) <- 'logical'

matches <- 0
for (i in seq_len(nrow(inp) - lw + 1)) {
  for (j in seq_len(ncol(inp) - lh + 1)) {
    diff <- sum(abs(inp[i + seq_len(lw) - 1, j + seq_len(lh) -1] - los))
    if (diff <= 10) {
      matches <- matches + 1
    }
  }
}
# solution:
print(matches)