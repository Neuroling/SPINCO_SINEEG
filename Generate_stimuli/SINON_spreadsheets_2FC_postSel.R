rm(list=ls())
library(dplyr)
library(tidyr)
###############################################################################
# SPREADSHEETS TO USE IN GORILLA
# ----------------------------------------------------------------------------
# - Read subsets of items
# - Assign balanced SNR levels
# - Export XLS file (indicating block etc)
###############################################################################
dirinput <- 'V:/spinco_data/LIRI_database/LIRI_database_subsets/'
diroutput <- 'V:/spinco_data/SINON/Spreadsheets'
setwd(dirinput)
#audiofiles
audiofiles_nvoc <- 'V:/spinco_data/Audio_recordings/LIRI_voice_DF/segments/items_OK_norm_vocoded/'
audiofiles_sissn <- 'V:/spinco_data/Audio_recordings/LIRI_voice_DF/segments/items_OK_norm_SiSSN/'
# 
filesnvoc <- dir(audiofiles_nvoc,pattern = '*.mp3')
filessissn <- dir(audiofiles_sissn,pattern = '*.mp3')
#directory with matching subsets
matchDir <- 'V:/spinco_data/LIRI_database/SINON_MATCH_v2/SINON_MATCH_subsets_2FC'

#------
# search files and concat
urdat <- openxlsx::read.xlsx('liri_2FC_postselection_Zoe.xlsx')
# SNR assignments to file suffices
snrLev <-   c('snr1','snr2','snr3','snr4','snr5')
snrs_voco <- c('4chans','5chans','6chans','7chans','8chans')
snrs_sissn <- c('10db','5db','0db','-5db','-10db')


`%nin%` = Negate(`%in%`) #some function that may be handy later
# SPREADSHEETS  ###################################################################

dat <- urdat[!is.na(urdat$new_distractor),]


# Version of data table in which target and distractor are exchanged
dat <- relocate(dat,new_distractor) #relocate most important cols at the beginning
dat <- relocate(dat,target)
datRev <- dat[,c(2,1,3:ncol(dat))]
colnames(datRev)<-colnames(dat)

# 2 Forced choice
trials <- list()
for (i in 1:4){
    
  currSet <-read.table(paste0(matchDir,'/list2match_2FC_set',i,'.txt'))
   
   # select the corresponding items from my main dataset
   dat1 <-  dat[which(dat$target %in% currSet$V1),]
   if (nrow(dat1) %% length(snrLev)!=0){
       print(paste0("not possible to balance n trials per snr. Removing ",nrow(dat1) %% length(snrLev)," rows to create a balanced SNR distribution."))
       dat1 <- dat1[1:(nrow(dat1)-(nrow(dat1) %% length(snrLev))),]
    }
 
     trials[[i]] <- select(dat1,target,new_distractor)
     colnames(trials[[i]]) <- c('item_target','item_distractor')
     
       # additional columns with info
     trials[[i]]$snr  <- rep(snrLev,nrow(trials[[i]])/5)
     trials[[i]]$block <- rep(paste0('block',i),nrow(trials[[i]]))
     
     # add position info, flip half of them  
     randomhalf <- sample(1:nrow(trials[[i]]))[1:(nrow(trials[[i]])/2)]
     
     trials[[i]]$item_left <- trials[[i]]$item_target
     trials[[i]]$item_left[randomhalf] <- trials[[i]]$item_distractor[randomhalf]
     
     trials[[i]]$item_right <- trials[[i]]$item_distractor
     trials[[i]]$item_right[randomhalf] <- trials[[i]]$item_target[randomhalf]
     
     trials[[i]]$correctAnswer <- 'L'
     trials[[i]]$correctAnswer[randomhalf] <- 'R'
         
     
             
}
ds <- data.table::rbindlist(trials)

#shuffle and then order by block
ds <- ds[sample(1:nrow(ds)),] 
ds <- ds[order(block),]

# fill the file names based on multiple matching/replacements 
ds$file_target <- paste0(ds$snr,'.mp3')
ds$file_target <- ifelse(ds$block=='block1' | ds$block=='block3',
                         stringi::stri_replace_all_regex(ds$file,pattern = snrLev,replacement = paste0('norm_',snrs_voco),vectorize = FALSE),
                         stringi::stri_replace_all_regex(ds$file,pattern = snrLev,replacement = paste0('norm',snrs_sissn),vectorize = FALSE))

ds$file_target <- ifelse(ds$block=='block1' | ds$block=='block3',
                         paste('NV',ds$item_target,ds$file_target,sep='_'),
                         paste('SiSSN',ds$item_target,ds$file_target,sep='_'))




ds$type <- ifelse(ds$block=='block1' | ds$block=='block3','NV','SiSSN') 
print(ds)
# save in output dir 
dirout <-  paste0(diroutput,'/2ForcedChoice/')
outputname <- paste0(dirout,'TrialSequences_2FC.xlsx')
openxlsx::write.xlsx(ds,outputname)

