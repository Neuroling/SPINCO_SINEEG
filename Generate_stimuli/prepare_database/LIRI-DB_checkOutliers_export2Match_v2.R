rm(list=ls())
library(dplyr)
library(tidyr)

fileinput <- 'V:/spinco_data/LIRI_database/LIRI_database_stimuli.xlsx'
fileoutput <- 'V:/spinco_data/LIRI_database/SINON_MATCH_v3/tmp_markOutliers.xlsx'
setwd('V:/spinco_data/LIRI_database/SINON_MATCH_v3/')
# read 
Merged <- openxlsx::read.xlsx(fileinput,sheet = 'Merged')
dat <- Merged
# Discards those for which there is no audiofile 
audiofiles_sissn <- 'V:/spinco_data/AudioRecs/LIRI_voice_DF/segments/Take1_all_trimmed/trim_loudNorm-23LUFS_SiSSN2/'
filessissn <- dir(audiofiles_sissn,pattern = 'S*.wav')
itemsWithFiles <- sapply(strsplit(filessissn,'_'),'[',2)
indices <- c(which(dat$CORRECT_SPELL %in% itemsWithFiles),which(gsub('-','',dat$Pseudoword) %in% itemsWithFiles))
dat <- dat[indices[duplicated(indices)],]

# Outlier marking:
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
# Export data for the different tasks
# Picture matching
dat2export <- dat[which(dat$outlier_lgSUBTLEX==FALSE & !is.na(dat$PTAN)),]
dat2export <- select(dat2export,c('CORRECT_SPELL','lgSUBTLEX','PTAN','Ned1','nSyllables','PTAF'))
write.table(dat2export,'list2match_PM.txt',col.names=FALSE,row.names = FALSE,sep = "\t")

# Lexical decision  
dat2export <- dat[which(dat$outlier_any==FALSE),]
dat2export <- select(dat2export,c('CORRECT_SPELL','lgSUBTLEX','PTAN','Ned1','nSyllables','PTAF'))
write.table(dat2export,'list2match_hard.txt',col.names=FALSE,row.names = FALSE,sep = "\t")

# 2FC
SUBTLEX <- openxlsx::read.xlsx('V:/spinco_data/LIRI_database/SINON_LEXOPS_genMatched/SUBTLEX-DE.xlsx')

    # Get frequency information 
    sel <- openxlsx::read.xlsx('V:/spinco_data/LIRI_database/LIRI_database_subsets/2FC_postselection_ZH_AS_GFG.xlsx')
    sel <- sel %>% filter(Include==1)
    
    SelInf <- SUBTLEX[c(which(SUBTLEX$Word %in% sel$target),which(SUBTLEX$Word %in% sel$Final_distractor)),]
    
    selidx <-  match(sel$target, SUBTLEX$Word)
    freqs <- cbind(select(SelInf[match(sel$target,SelInf$Word),],c('Word','lgSUBTLEX')),
                select(SelInf[match(sel$Final_distractor,SelInf$Word),],c('Word','lgSUBTLEX')))
    colnames(freqs) <- c('target','target_freq','distract','distract_freq')
    
    freqs$freq_diff <- freqs$target_freq - freqs$distract_freq
    freqs <- freqs[!is.na(freqs$freq_diff),]
    
    
    
dat2export <- dat[which(dat$CORRECT_SPELL %in% sel$target),]
dat2export <- dat2export[which(!is.na(dat2export$OSAW) | !is.na(dat2export$PSAW)),]
dat2export <- dat2export[!is.na(dat2export$PTAF),]
dat2export <- select(dat2export,c('CORRECT_SPELL','lgSUBTLEX','PTAN','Ned1','nSyllables','PTAF'))

dat2export$target <- dat2export$CORRECT_SPELL
dat2export <- merge(dat2export,freqs,by='target')
dat2export <- select(dat2export,c('CORRECT_SPELL','lgSUBTLEX','PTAN','Ned1','nSyllables','PTAF','freq_diff'))

write.table(dat2export,'list2match_2FC.txt',col.names=FALSE,row.names = FALSE,sep = "\t")
