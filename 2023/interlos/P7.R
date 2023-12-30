setwd('D:/python/advent/2023/interlos/')

inp <- read.csv('park.txt', sep=' ', header=F)

chod0 <- SpatialLines(list(Lines(Line(inp), 1)))
chod <- gBuffer(chod0, width=5, quadsegs=50)

flowers <- SpatialPoints(expand.grid(0:256, 0:256))
plot(flowers)

x <- gDistance(chod, flowers, byid=T)
x[x < .005] <- 0
## solution:
table(x == 0)['FALSE']

idk <- x > 0 & x < .01
dont.know <- flowers[idk]
plot(dont.know)
plot(chod, add=T)
plot(chod0, add=T)

cdk <- coordinates(dont.know)
text(cdk, apply(cdk, 1, paste, collapse=','), col='red')
text(inp, apply(inp, 1, paste, collapse=','))
