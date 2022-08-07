rm(list=ls())
library(dplyr)
library(tidyr)

fileinput <- 'V:/spinco_data/Database_stimuli/Neuroling_stimuli.xlsx'
fileoutput <- 'V:/spinco_data/Database_stimuli/tmp_markOutliers.xlsx'

# read 
Merged <- openxlsx::read.xlsx(fileinput,sheet = 'Merged')
dat <- Merged
# Outlier rejection:
#lgSubtlex
boxstats <- boxplot.stats(dat$lgSUBTLEX)
dat$outlier_lgSUBTLEX <- !(dat$lgSUBTLEX > boxstats$stats[1] & dat$lgSUBTLEX < boxstats$stats[5])

 
#PTAN (neighbor metric: phonological, neighbor metric: all, neighborhood frequency: all, value: size)
boxstats <- boxplot.stats(dat$PTAN)
dat$outlier_PTAN <- !(dat$PTAN > boxstats$stats[1] & dat$PTAN < boxstats$stats[5])
 
#ned1_diff (for associated Wuggy-pseudowords)
boxstats <- boxplot.stats(dat$Ned1_Diff)
dat$outlier_Ned1_Diff <- !(dat$Ned1_Diff > boxstats$stats[1] & dat$Ned1_Diff < boxstats$stats[5])
 
#Outlier in any
dat$outlier_any <-  (dat$outlier_lgSUBTLEX==TRUE | dat$outlier_PTAN==TRUE | dat$outlier_Ned1_Diff==TRUE)
dat$nSyllables <- sapply(strsplit(dat$Pseudoword,'-'),length)

# save 
openxlsx::write.xlsx(dat,fileoutput)


##################################################
# Export a selection for matching  
dat2export <- dat[which(dat$outlier_lgSUBTLEX==FALSE & !is.na(dat$PTAN)),]
dat2export <- select(dat2export,c('CORRECT_SPELL','lgSUBTLEX','PTAN','Ned1_Diff','nSyllables'))
write.table(dat2export,'list2match.txt',col.names=FALSE,row.names = FALSE,sep = "\t")

dat2export <- dat[which(dat$outlier_any==FALSE),]
dat2export <- select(dat2export,c('CORRECT_SPELL','lgSUBTLEX','PTAN','Ned1_Diff','nSyllables'))
write.table(dat2export,'list2match_hard.txt',col.names=FALSE,row.names = FALSE,sep = "\t")


