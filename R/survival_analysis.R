library(survival)
library(ranger)
library(ggplot2)
library(dplyr)
library(ggfortify)

data(veteran)
head(veteran)

# kaplan meier analysis
km <- with(veteran, Surv(time, status))
head(km, 80)
km_fit <- survfit(Surv(time, status) ~ 1, data=veteran)
#autoplot(km_fit)
plot(km_fit, xlab="Days", main="Kaplan Meyer Plot")

km_trt_fit <- survfit(Surv(time, status) ~ trt, data=veteran)
#autoplot(km_trt_fit)
plot(km_trt_fit, xlab="Days", main="Kaplan Meyer Plot")

vet <- mutate(veteran, AG=ifelse((age<60), "LT60", "OV60"),
              AG=factor(AG),
              trt=factor(trt, labels=c("standard", "test")),
              prior=factor(prior,labels=c("N0","Yes")))
km_AG_fit <- survfit(Surv(time, status) ~ AG, data=vet)
#autoplot(km_AG_fit)
plot(km_trt_fit, xlab="Days", main="Kaplan Meyer Plot")

cox <- coxph(Surv(time, status)~trt + celltype + karno + diagtime + age +
             prior, data=vet)
summary(cox)
cox_fit <- survfit(cox)
#autoplot(cox_fit)
plot(cox_fit)


aa_fit <- aareg(Surv(time, status) ~ trt + celltype + karno + diagtime + age +
                prior, data=vet)
autoplot(aa_fit)
plot(aa_fit)


r_fit <- ranger(Surv(time, status) ~ trt + celltype + karno + diagtime + age + prior,
                data=vet,
                mtry=4,
                importance="permutation",
                splitrule="extratrees",
                verbose=TRUE)
death_times <- r_fit$unique.death.times
surv_prob <- data.frame(r_fit$survival)
avg_prob <- sapply(surv_prob, mean)
plot(r_fit$unique.death.time, r_fit$survival[1,],
     type="l",
     ylim=c(0,1),
     col="red",
     xlab="days",
     ylab="survival",
     main="patient survial curves")

cols <- colors()
for (n in sample(c(2:dim(vet)[1]),20)) {
    lines(r_fit$unique.death.times, r_fit$survival[n,], type="l", col=cols[n])
}
lines(death_times, avg_prob, lwd=2)
legend(500, 0.7, legend=c('Average=black'))

vi <- data.frame(sort(round(r_fit$variable.importance, 4), decreasing=TRUE))
names(vi) <- "importance"
head(vi)

cat("Prediction Error = 1 - Harrel's c-index = ", r_fit$prediction.error)
kmi <- rep("KM", length(km_fit$time))
km_df <- data.frame(km_fit$time, km_fit$surv, kmi)
names(km_df) <- c("Time", "Surv", "Model")

coxi <- rep("Cox", lenght(cox_fit$time))
cox_df <- data.frame(cox_fit$time, cox_fit$surv, coxi)
names(cox_df) <- c("Time", "Surv", "Model")


rfi <- rep("RF", lenght(r_fit$unique.death.times))
rf_df <- data.frame(r_fit$unique.death.times, avg_prob, rfi)
names(rf_df) <- c("Time", "Surv", "Model")

plot_df <- rbind(km_df, cox_df, rf_df)
p <- ggplot(plot_df, aes(x=time, y= Surv, color=Model)) + geom_line()

