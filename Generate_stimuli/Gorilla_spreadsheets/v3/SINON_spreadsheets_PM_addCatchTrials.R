rm(list=ls())
###############################################################################
#  ADD CATCH TRIALS:
# - add trials of very low degradation/noise levels as catch trials 
# - check there is no repetition (except for 2AFC were not enough stimuli sets)

###############################################################################

# ----------------------------------------------
### LEXICAL DECISION TASK 
dirinput <- 'V:/spinco_data/SINON/Spreadsheets/PM/'
basefilename <- 'Spreadsheets_PM_Gorilla'
matchedSets <- 'V:/spinco_data/LIRI_database/SINON_MATCH_v4/PM_20items/'
databasefile <-'V:/spinco_data/LIRI_database/LIRI_database_stimuli.xlsx'

setwd(dirinput)
dat <- openxlsx::read.xlsx(paste0(basefilename,'.xlsx'))
database <- openxlsx::read.xlsx(databasefile,sheet = 'Merged')

# find 4  additional sets..
catches <- list()
for (i in 1:4){
  fileinput <- paste0(matchedSets,'list2match10_set',20+i,'.txt')
  tab <- read.delim(fileinput,header = FALSE)  
  items <- tab$V1 
  pseudos <- gsub('-','',database$Pseudoword[which(database$CORRECT_SPELL %in% items)])
  # compose catch trials
  catches [[i]]<- 
    as.data.frame(rbind(cbind('',i,'catch_trial',i,items,'word',
                              replicate(n=5,paste0('SiSSN_',items,'_norm15db.wav')),
                              replicate(n=5,paste0('NV_',items,'_norm_32ch_1p.wav'))),
                        #
                        cbind('',i,'catch_trial',i,pseudos,'pseudo',
                              replicate(n=5,paste0('SiSSN_',pseudos,'_norm15db.wav')),
                              replicate(n=5,paste0('NV_',pseudos,'_norm_32ch_1p.wav')))))
  colnames(catches[[i]]) <- colnames(dat)
}
idx1 <- which(dat$block==1)[1]
idx2 <- which(dat$block==2)[1]
idx3 <- which(dat$block==3)[1]
idx4 <- which(dat$block==4)[1]
# Insert
newdat <- 
rbind(dat[1:(idx1-1),],catches[[1]],dat[idx1:(idx2-1),],
      catches[[2]],dat[idx2:(idx3-1),],
      catches[[3]],dat[idx3:(idx4-1),],
      catches[[4]],dat[idx4:nrow(dat),])

# save 
setwd(dirinput)
openxlsx::write.xlsx(x = newdat,paste0(basefilename,'C.xlsx'))

 