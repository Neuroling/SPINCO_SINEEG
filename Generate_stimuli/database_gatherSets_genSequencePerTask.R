rm(list=ls())
library(dplyr)
library(tidyr)
# directories 
dirinput<- 'V:/spinco_data/Database_stimuli/Matched_sets_50words'
databasedfile <-'V:/spinco_data/Database_stimuli/Neuroling_stimuli.xlsx'
diroutput <- 'V:/spinco_data/SINON/Spreadsheets'

# search files and concat
database <- openxlsx::read.xlsx(databasedfile,sheet = 'Merged')
snrLev <- c('snr1','snr2','snr3','snr4','snr5')
setwd(dirinput)

# Lexical Decision ------------------------------------------

ds <- list()
for (i in 1:5){
  currSet <-read.table(paste0('list2match_set',i,'.txt'))
  
  if (nrow(currSet) %% length(snrLev)!=0){
    stop("not possible to balance n trials per snr ! ")
  }
  #find matching pseudowords  
  wordsInSet <- currSet$V1   %>% paste0(.,'_',snrLev)
  pseudoInSet <- database$Pseudoword[which(currSet$V1 %in% database$CORRECT_SPELL)]
  pseudoInSet <- gsub('-','',pseudoInSet) %>% paste0(.,'_',snrLev)
  
 
  ds[[i]] <-as.data.frame(cbind(rep(paste0('set',i),length(wordsInSet)+length(pseudoInSet)),
                                c(wordsInSet,pseudoInSet)))
}

ds <- data.table::rbindlist(ds)
colnames(ds) <- c('set','item') 

# save in output dir 
openxlsx::write.xlsx(ds,paste0(diroutput,'/LexicalDecision/TrialSequences_LD.xlsx'))
rm(ds)

# 4FC ----------------------------------------------------------
ds <- list()
for (i in 1:5){
  currSet <-read.table(paste0('list2match_set',i,'.txt'))
  
  if (nrow(currSet) %% length(snrLev)!=0){
    stop("not possible to balance n trials per snr ! ")
  }
  
  
  wordsInSet <- database$CORRECT_SPELL[which(database$CORRECT_SPELL %in% currSet$V1)]
  ##  find pseudowords, split in two (shuffle first )
  pseudoInSet <- database$Pseudoword[which( database$CORRECT_SPELL %in% currSet$V1)]
  pseudoInSet <- gsub('-','',pseudoInSet) 
    
  half1 <- cbind(wordsInSet[1:(length(wordsInSet)/2)],
                   pseudoInSet[1:(length(pseudoInSet)/2)])
                   
  half2 <- cbind(wordsInSet[(1+length(wordsInSet)/2):length(wordsInSet)],
                   pseudoInSet[(1+length(pseudoInSet)/2):length(pseudoInSet)])
  
  
    #  put in table 
    spreadsheet <- as.data.frame(cbind(half1,half2))
    
    # select targets (half words, half pseudowords) 
    targets <- spreadsheet$V1
    targets[1:(nrow(spreadsheet)/2)] <- spreadsheet$V2[1:(nrow(spreadsheet)/2)]
    targets <- paste0(targets,'_',snrLev);
    
    #shuffle the columns for positions per row, keep targets locked ,add target as first column
    spreadsheet <- cbind(targets,as.data.frame(t(apply(spreadsheet,FUN=sample,1))))
    spreadsheet <- cbind(rep(paste0('set',i),nrow(spreadsheet)), spreadsheet)
    colnames(spreadsheet)<-c('set','target','up','right','down','left')
    ds[[i]] <-spreadsheet
}

ds <- data.table::rbindlist(ds)
 
# save in output dir 
openxlsx::write.xlsx(ds,paste0(diroutput,'/4ForcedChoice/TrialSequences_4FC.xlsx'))
rm(ds)
rm(spreadsheet)

# Picture matching task ----------------------------------------------------------

ds <- list()
for (i in 1:5){
  currSet <-read.table(paste0('list2match_set',i,'.txt'))
  
  if (nrow(currSet) %% length(snrLev)!=0){
    stop("not possible to balance n trials per snr ! ")
  }
  # first add all matching pictures 
  picture <- paste0(database$PICTURE[which(currSet$V1 %in% database$CORRECT_SPELL)],'_',
                    database$CORRECT_SPELL[which(currSet$V1 %in% database$CORRECT_SPELL)])
  match <- rep(1,nrow(currSet))
  
  wordsInSet <- currSet$V1
  spreadsheet  <- as.data.frame(cbind(rep(paste0('set',i),nrow(currSet)), paste0(wordsInSet,'_',snrLev),picture,match))
    #
  
  ds[[i]]
}

ds <- data.table::rbindlist(ds)
colnames(ds) <- c('set','item','pic') 


# save in output dir 
openxlsx::write.xlsx(ds,paste0(diroutput,'/PictureMatching/TrialSequences_PIC.xlsx'))
