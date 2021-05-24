library(tydiverse)
library(boot)
library(tibble)
library(car)

df = readxl::read_excel("countries_data.xlsx")
df = apply(df,2,function(x)gsub('\\s+', '',x))
df = as_tibble(df)
df$gdp = as.numeric(df$gdp)
df$employment = as.numeric(df$employment)
df$HDI = as.numeric(df$HDI)
df$y = as.numeric(df$y)
df$life_exp = as.numeric(df$life_exp)
df

dfm = model.matrix(~ y + gdp+employment + HDI +life_exp, data=df, scale=TRUE)
dfm[, -2] = scale(dfm[, -2], center=F, scale=T)
dfm = as.data.frame(dfm)
colnames(dfm) = list("i", "y","gdp", "employment","HDI", "life_exp")

boot.huber <- function(data, indices, maxit=20) {
  data <- data[indices,] # select obs. in bootstrap sample
  mod <- glm(y ~ gdp + employment + HDI +life_exp, data = data, family = "binomial", maxit=maxit)
  coefficients(mod)}

system.time(migration.boot <- boot(dfm, boot.huber, R=200, maxit=100)) 
migration.boot$t0
warnings()
dataEllipse(migration.boot$t[,2], migration.boot$t[,3], xlab='gdp’', ylab='employment',
             cex=.3, levels=c(.5, .95, .99), robust=T)

boot.ci(migration.boot, index=2, type=c("norm", "perc", "bca"))

jack.after.boot(migration.boot, index=2, main='(a) income coefficient')

