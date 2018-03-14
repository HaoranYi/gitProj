# decicion tree is unstable. Random forest method, create a set of decicion
# trees and then add up the result, will make the result more stable.

require(randomForest)
require(MASS)  # package which contains the boston housing dataset
attach(Boston)
set.seed(101)

dim(Boston)

# training with 300 obs
train = sample(1:nrow(Boston), 300)

# training
Boston.rf = randomForest(medv ~ ., data=Boston, subset=train)
plot(Boston.rf)

oob.err = double(13)
test.err = double(13)

for (mtry in 1:13) {
    rf = randomForest(medv ~ ., data=Boston, subset=train, mtry=mtry, ntree=400)
    oob.err[mtry] = rf$mse[400]
    pred <- predict(rf, Boston[-train,])
    #browser()
    test.err[mtry] = with(Boston[-train,], mean((medv-pred)^2))
    cat(mtry, "")
}

test.err
oob.err
matplot(1:mtry,
        cbind(oob.err,test.err),
        pch=19,
        col=c("red","blue"),
        type="b",
        ylab="Mean Squared Error",
        xlab="Number of Predictors Considered at each Split")

legend("topright",
       legend=c("Out of Bag Error","Test Error"),
       pch=19,
       col=c("red","blue"))
