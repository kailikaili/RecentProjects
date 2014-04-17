
decision.tree.old <- function(){
	library(rpart)
	cmb.train <- read.csv("train.csv")
	exist.age.mean.train <- mean(cmb.train[rowSums(is.na(cmb.train))==0, ]$age)
	cmb.train[rowSums(is.na(cmb.train))==1, ]$age <- exist.age.mean.train
	cmb.tree <- rpart(survived ~ pclass + sex + age + sibsp + parch + fare + embarked, data=cmb.train, parms=list(split='information'))
	plot(cmb.tree)
	text(cmb.tree, use.n=TRUE)
	
	cmb.train[cmb.train[,1]==1,1] = "live"
	cmb.train[cmb.train[,1]==0,1] = "die"
	
	cmb.test <- read.csv("test_labeled.csv")
	exist.age.mean.test <- mean(cmb.test[rowSums(is.na(cmb.test))==0, ]$age)
	cmb.test[rowSums(is.na(cmb.test))==1, ]$age <- exist.age.mean.test
	
	cmb.fit <- predict(cmb.tree,cmb.test[,c(2,4,5,6,7,9,11)],type="class")
	
	accuracy <- 0	
	for (i in 1:418)
 	{
 		if (cmb.fit[i]==cmb.test[i,1]+1)
 		    accuracy = accuracy + 1	
 	}
	for (i in 1:418)
  	{
  		if ((cmb.fit[i]=="die" && cmb.test[i,1]==0) || (cmb.fit[i]=="live" && cmb.test[i,1]==1))
  		    accuracy = accuracy + 1	
  	}
	accuracy/418	
	
}


decision.tree <- function(){
	
	library(rpart)
	cmb.train <- read.csv("train.csv")
	
	train.survived.mean <- mean(cmb.train[which(cmb.train[,1]==1&rowSums(is.na(cmb.train))==0), ]$age)
	cmb.train[which(cmb.train[,1]==1&rowSums(is.na(cmb.train))==1), ]$age<- train.survived.mean
	
	train.died.mean <- mean(cmb.train[which(cmb.train[,1]==0&rowSums(is.na(cmb.train))==0), ]$age)
	cmb.train[which(cmb.train[,1]==0&rowSums(is.na(cmb.train))==1), ]$age<- train.died.mean
	
	cmb.train[cmb.train[,1]==1,1] = "live"
	cmb.train[cmb.train[,1]==0,1] = "die"
	
	cmb.tree <- rpart(survived ~ pclass + sex + age + sibsp + parch + fare + embarked, data=cmb.train, parms=list(split='information'))
	plot(cmb.tree)
	text(cmb.tree, use.n=TRUE)
		
		
	cmb.test <- read.csv("test_labeled.csv")
		
	test.survived.mean <- mean(cmb.test[which(cmb.test[,1]==1&rowSums(is.na(cmb.test))==0), ]$age)
	cmb.test[which(cmb.test[,1]==1&rowSums(is.na(cmb.test))==1), ]$age<- test.survived.mean
	
	test.died.mean <- mean(cmb.test[which(cmb.test[,1]==0&rowSums(is.na(cmb.test))==0), ]$age)
	cmb.test[which(cmb.test[,1]==0&rowSums(is.na(cmb.test))==1), ]$age<- test.died.mean
	
	cmb.test[cmb.test[,1]==1,1] = "live"
	cmb.test[cmb.test[,1]==0,1] = "die"
		
	cmb.fit <- predict(cmb.tree,cmb.test[,c(2,4,5,6,7,9,11)],type="class")
	
	num.test <- dim(cmb.test)[1]
	
	accuracy <- 0	
	for (i in 1:num.test)
 	{
 		if (cmb.fit[i]==cmb.test[i,1])
 		    accuracy = accuracy + 1	
 	}
	
	return(accuracy/num.test)		
	
}


call.adaboost.old <- function()
{
	library(rpart)
	cmb.train <- read.csv("train.csv")
	exist.age.mean.train <- mean(cmb.train[rowSums(is.na(cmb.train))==0, ]$age)
	cmb.train[rowSums(is.na(cmb.train))==1, ]$age <- exist.age.mean.train
	
	cmb.train[cmb.train[,1]==1,1] = "live"
	cmb.train[cmb.train[,1]==0,1] = "die"
	
	cmb.test <- read.csv("test_labeled.csv")
	exist.age.mean.test <- mean(cmb.test[rowSums(is.na(cmb.test))==0, ]$age)
	cmb.test[rowSums(is.na(cmb.test))==1, ]$age <- exist.age.mean.test
	
	cmb.test[cmb.test[,1]==1,1] = "live"
	cmb.test[cmb.test[,1]==0,1] = "die"
	
	#result.ada <- my.adaboost(cmb.train[,c(1,2,4,5,6,7,9,11)], cmb.train[,1], cmb.test[,c(1,2,4,5,6,7,9,11)], 10)
	
	result.ada <- my.adaboost.modified(cmb.train[,c(1,2,4,5,6,7,9,11)], cmb.train[,1], cmb.test[,c(1,2,4,5,6,7,9,11)], 50)
	
	num.test <- dim(cmb.test)[1]
	
	cmb.rpart <- rpart(survived~.,data=cmb.train[,c(1,2,4,5,6,7,9,11)]) #first element, the label, count in?
	cmb.rpart.test <- predict(cmb.rpart,cmb.test[,c(2,4,5,6,7,9,11)],type="class")
		
	accuracy.rpart <- cal.acc(cmb.rpart.test, cmb.test[,1], num.test)
	
	return (c(result.ada, accuracy.rpart))
	
}


call.adaboost <- function()
{
	library(rpart)
	library(ada)
	cmb.train <- read.csv("train.csv")
	
	train.survived.mean <- mean(cmb.train[which(cmb.train[,1]==1&rowSums(is.na(cmb.train))==0), ]$age)
	cmb.train[which(cmb.train[,1]==1&rowSums(is.na(cmb.train))==1), ]$age<- train.survived.mean
	
	train.died.mean <- mean(cmb.train[which(cmb.train[,1]==0&rowSums(is.na(cmb.train))==0), ]$age)
	cmb.train[which(cmb.train[,1]==0&rowSums(is.na(cmb.train))==1), ]$age<- train.died.mean
		
	cmb.train[cmb.train[,1]==1,1] = "live"
	cmb.train[cmb.train[,1]==0,1] = "die"
	
	
	cmb.test <- read.csv("test_labeled.csv")
	
	test.survived.mean <- mean(cmb.test[which(cmb.test[,1]==1&rowSums(is.na(cmb.test))==0), ]$age)
	cmb.test[which(cmb.test[,1]==1&rowSums(is.na(cmb.test))==1), ]$age<- test.survived.mean
	
	test.died.mean <- mean(cmb.test[which(cmb.test[,1]==0&rowSums(is.na(cmb.test))==0), ]$age)
	cmb.test[which(cmb.test[,1]==0&rowSums(is.na(cmb.test))==1), ]$age<- test.died.mean
	
	cmb.test[cmb.test[,1]==1,1] = "live"
	cmb.test[cmb.test[,1]==0,1] = "die"
	
	#result.ada1 <- my.adaboost(cmb.train[,c(1,2,4,5,6,7,9,11)], cmb.train[,1], cmb.test[,c(1,2,4,5,6,7,9,11)], 10)
	
	result.ada <- my.adaboost.modified(cmb.train[,c(1,2,4,5,6,7,9,11)], cmb.train[,1], cmb.test[,c(1,2,4,5,6,7,9,11)], 50)
	
	num.test <- dim(cmb.test)[1]
	
	cmb.rpart <- rpart(survived~.,data=cmb.train[,c(1,2,4,5,6,7,9,11)])
	
	cmb.rpart.test <- predict(cmb.rpart,cmb.test[,c(2,4,5,6,7,9,11)],type="class")
		
	accuracy.rpart <- cal.acc(cmb.rpart.test, cmb.test[,1], num.test)
	
	#return (c(result.ada, accuracy.rpart))
	
	result.df <- data.frame(least.number.misclassified.by.ada = result.ada[1], iteration.number.giving.least.number.misclassified= result.ada[2], number.misclassified.by.single.tree = accuracy.rpart)
	return (result.df)
	
}



my.adaboost <- function(x.train, y.train, x.test, T_iter)
{
	x.ada <-ada(survived~., data=x.train, iter=T_iter, nu=1, type="discrete")
	x.ada.test <- addtest(x.ada, x.test[,-1], x.test[,1])
	x.ada.test2 <- predict(x.ada, x.test[,-1], type="vector")
	
	return(x.ada.test2)
	
}


my.adaboost.modified <- function(x.train, y.train, x.test, T_iter)
{
	
	misnum.ada.train <- rep(0,T_iter)
	
	misnum.ada.test <- rep(0,T_iter)
	
	num.test <- dim(x.test)[1]
	num.train <- dim(x.train)[1]
	
	min.misnum <- num.test
	best.t <- 0
	
	for(i in 1:T_iter)
	{
		x.ada <-ada(survived~., data=x.train, iter=i, nu=1, type="discrete")
		x.ada.test <- addtest(x.ada, x.test[,-1], x.test[,1])
		x.ada.test2 <- predict(x.ada, x.test[,-1], type="vector")
		
		misnum.ada.test[i] <- cal.acc(x.ada.test2, x.test[,1], num.test)
		
		if(misnum.ada.test[i] < min.misnum)
		{
			min.misnum <- misnum.ada.test[i]
			best.t <- i
		}
		
		x.ada <-ada(survived~., data=x.train, iter=i, nu=1, type="discrete")
		x.ada.train <- addtest(x.ada, x.train[,-1], x.train[,1])
		x.ada.train2 <- predict(x.ada, x.train[,-1], type="vector")
	
		misnum.ada.train[i] <- cal.acc(x.ada.train2, x.train[,1], num.train)
		
	}
	
	par(mfrow=c(1,2))
	
	plot(c(0,T_iter), c(0, 125), main = "Number Misclassified (Test)", xlab = "Number of Iteration", ylab = "Number of Passengers")
	
	lines(c(1:T_iter), misnum.ada.test, type = "o", col = "red")
	
	plot(c(0,T_iter), c(0, 160), main = "Number Misclassified (Train)", xlab = "Number of Iteration", ylab = "Number of Passengers")
	
	lines(c(1:T_iter), misnum.ada.train, type = "o", col = "blue")
	
	return(c(min.misnum, best.t))
	
}

cal.acc <- function(y.test, true.test, num)
{
	
	accuracy <- 0
	
	for (i in 1:num)
	{
		if (y.test[i]==true.test[i])
  		    accuracy = accuracy + 1	
	}
	
	return (num-accuracy)
}




cal.acc.old <- function(y.test, true.test, num)
{
	
	accuracy <- 0
	
	for (i in 1:num)
	{
		if ((y.test[i]=="die" && true.test[i,1]==0) || (y.test[i]=="live" && true.test[i,1]==1))
  		    accuracy = accuracy + 1	
	}
	
	return (accuracy/num)
}