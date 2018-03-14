set.seed(123)
x <- seq(from=1, to=100, by=1) + 10 + rnorm(100, sd=7)
plot(x)

# convert vector to time series
# >> args(ts)

xt <- ts(x, start=c(2000,1), frequency=4)
print(xt)
plot(xt)

# difference, log, moving average, percent change, lag or cumulative sum
xt_lag1 <- stats::lag(xt, 1)  # shift the time base back (start with offset 1)
head(cbind(xt, xt_lag1))

xt_lag1 <- stats::lag(xt, -1)
head(cbind(xt, xt_lag1))

# adj diff
xs_diff <- diff(xs, lag=1)

# simulate data
trend <- ts(seq(from=10, to=110))
cycle <- ts(sin(tred))*0.2*trend
xt <- trend + cycle
plot.ts(xt)

# log
xt_log <- log(xt)
tm <- cbind(xt, xt_log)
plot.ts(tm)

# boxcox transform to remove constant: to normal varaible
library(forecast)
plot.ts(BoxCox(xt, lambda=0.5))

# percent change
xs_pch <- xt/lag(xt, -1)-1

# filtering
xt_filter <- filter(xt, filter=rep(1/5, 5), sides=1)
