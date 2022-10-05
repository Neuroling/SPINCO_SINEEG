rm (list = ls())
library(R.matlab)
library(ggplot2)
library(Rmisc)
library(dplyr)
##############################################################
#  Decoding Accuracy
#---------------------------------------------------
# author: GFG 2022
# 
#
##############################################################

dirinput <- 'V:/spinco_data/SINEEG/analysis/mvpa'
setwd(dirinput)

# read structure array from matlab 
S <- R.matlab::readMat('Results_Infants_included_decode_within_SVM_03-Aug-2022_70912.mat')
results <- S$results
res <- lapply(results,unlist) #extract lists with values (cell arrays in matlab)
names(res) <-attributes(results)$dimnames[[1]] #preserve names 
res$times <- sprintf("%03d", as.numeric(res$times))
# Compute menas 
 meanDA <- list()
for (i in 1:dim(res$DA)[1]){
  meanDA[[i]] <- 0
  for (j in 1:dim(res$DA)[2]){
      meanDA[[i]][[j]] <-  mean(res$DA[i,j,,],na.rm = TRUE) 
      
  }
}

meanDA <- do.call(rbind,meanDA)
meanDA <- as.data.frame(meanDA)
colnames(meanDA) <- res$times
meanDA$subj <- paste0('s',1:dim(meanDA)[1])
meanDA <- dplyr::relocate(meanDA,subj)

# arrange 
longMeanDA <- meanDA %>% tidyr::pivot_longer(names_to = 'time',values_to='value',cols = 2:dim(meanDA)[2])
longMeanDA
longMeanDA$subj <- as.factor(longMeanDA$subj)
longMeanDA$time <- as.factor(longMeanDA$time)
#levels(longMeanDA$time)  <- times


# Permutation statistcs
library(lmPerm)

permute::permu.test 


norm(50)
var.test(longMeanDA$value[which(longMeanDA$time=='-50')],rep(50,10))




 



# plot 
longMeanDA$group <- 'x'
longMeanDA %>%
      ggplot(., aes(x=time,y=value)) + 
        geom_line(size=1,aes(color=subj,group=subj))+ 
        theme_bw()  + 
        stat_summary(aes(group=group),fun = mean,geom = "line",size = 1.2, alpha=0.8) + 
        stat_summary(fun.data = mean_cl_normal,geom = "ribbon",size = 1,aes(group = group),linetype="dashed",alpha = 0.25) + #confidence interval
        scale_x_discrete(breaks=seq(-50,550,50))+ 
        theme(text = element_text(size=20))
  
        





#print(fig)         
#plotly::ggplotly(fig)
apply(DA,c(1,2),function(x)mean(na.omit(x)))



DA <- res$DA
apply(DA,c(1,2),function(x) mean(na.omit(x)))

sapply(DA,function(x)mean(x,c(2,3)))

sapply()
apply(DA,1,function(x) function(y) apply(x,c(2,3),mean(na.omit(y))))


dat2plot <- apply(DA,c(1,2),function(x)mean(x))

str(dat2plot)
plot(dat2plot)


x <- DA[1,,,]
x
str(x)
#rowMeans(y)
#lot(y)







 v
