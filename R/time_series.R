set.seed(123)
x <- seq(from=1, to=100, by=1) + 10 + rnorm(100, sd=7)
plot(x)

# convert vector to time series
# >> args(ts)

xt <- ts(x, start=c(2000,1), frequency=4)
print(xt)
plot(xt)
