library(ggplot2)
# Read data
rm(list=ls())
dirinput <- 'V:/gfraga/'
Merged <- openxlsx::read.xlsx(paste0(dirinput,'/Neuroling_SINON_stimuli.xlsx'),sheet = 'Merged')

# Select only valid cases (e.g., Phono info available)
dat <- Merged[!is.na(Merged$PhoWord),]
  
  # Preselection based on lgSubtlex
  boxstats <- boxplot.stats(dat$lgSUBTLEX)
  dat <- dat[dat$lgSUBTLEX > boxstats$stats[1] & dat$lgSUBTLEX < boxstats$stats[5],]
  rm(boxstats)
  
  # Preselection based on PTAN (neighbor metric: phonological, neighbor metric: all, neighborhood frequency: all, value: size)
  boxstats <- boxplot.stats(dat$PTAN)
  dat <- dat[dat$PTAN > boxstats$stats[1] & dat$PTAN < boxstats$stats[5],]
  rm(boxstats)
  
  #Select only top ned1_diff (for associated Wuggy-pseudowords)
  boxstats <- boxplot.stats(dat$Ned1_Diff)
  dat <- dat[dat$Ned1_Diff > boxstats$stats[1] & dat$Ned1_Diff < boxstats$stats[5],]
  

#  
dat<-dat[sample(1:nrow(dat)),]
dat$CORRECT_SPELL
# ggplot(dat,aes(y=lgSUBTLEX)) + geom_boxplot()+ theme_bw()

