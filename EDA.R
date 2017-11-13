Data <- read.csv("/home/cancer/PycharmProjects/ORMAE/HR_Employee_Attrition_Data.csv")
summary(Data)
namelist <- c(names(Data))
for (var in namelist) {
  value <- Data[var]
  plot(table(value), ylab = "Frequency", xlab = var, type = 'h')
}
remove(value1)
value1 <-Data$WorkLifeBalance
n = min(value1)
m = max(value1)
x = ceiling(m/5)
binned <- bin_data(value1, bins=seq(n,m,length.out = 5), boundaryType = "[lorc")
summary(binned)
