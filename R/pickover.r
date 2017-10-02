# pickover test to random number generator with various probability dist.
library("rgl")

N = 99000
r <- rnorm(N)
#r <- rbinorm(N, 100, 0.3)
#r <- rpois(N, 10)
#r <- runif(N)
#r <- rt(N, 3)
#r <- rlogis(N)
#r <- rbeta(N, 1, 2)
#r <- rchisq(N, 15)

x <- r[seq(1, length(r), 3)]
y <- r[seq(2, length(r), 3)]
z <- r[seq(3, length(r), 3)]

lim <- function(x) { 1.1*c(-max(abs(x)),max(abs(x))) }
rgl.open()
rgl.bg(color="white")
rgl.spheres(x, y, z, r=0.5, color="lightblue")
rgl.lines(lim(x), c(0, 0), c(0, 0), color="black", lw=1.5)
rgl.lines(c(0, 0), lim(y), c(0, 0), color="red", lw=1.5)
rgl.lines(c(0, 0), c(0, 0), lim(z), color="blue", lw=1.5)
grid3d(c("x", "y", "z"))
