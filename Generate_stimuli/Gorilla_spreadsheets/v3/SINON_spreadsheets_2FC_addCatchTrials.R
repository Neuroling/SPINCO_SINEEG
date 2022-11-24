rm(list=ls())
###############################################################################
#  ADD CATCH TRIALS:
# - add trials of very low degradation/noise levels as catch trials 
# - check there is no repetition (except for 2AFC were not enough stimuli sets)

###############################################################################

# ----------------------------------------------
### LEXICAL DECISION TASK 
dirinput <- 'V:/spinco_data/SINON/Spreadsheets/2FC/'
basefilename <- 'Spreadsheets_2FC_Gorilla'
databasefile <-'V:/spinco_data/LIRI_database/LIRI_database_stimuli.xlsx'

setwd(dirinput)
dat <- openxlsx::read.xlsx(paste0(basefilename,'.xlsx'))
database <- openxlsx::read.xlsx(databasefile,sheet = 'Merged')

# Select 13 stimuli from one block to be presented in the other blocks as catches
catches <-  rbind(dat[which(dat$block==1),][1:12,],
              dat[which(dat$block==2),][1:12,],
              dat[which(dat$block==3),][1:12,],
              dat[which(dat$block==4),][1:12,])
catches$display <-'catch_trial'

catches$block <- rep(c('3','4','1','2'),each=12) #exchange block identifier 
catches$randomise_trials <- catches$block

catches[,grepl('list.*',colnames(catches))] <-  cbind(replicate(n=5,paste0('SiSSN_',catches$item_target,'_norm15db.wav')),replicate(n=5,paste0('NV_',catches$item_target,'_norm_32ch_1p.wav')))
  
  
idx1 <- which(dat$block==1)[1]
idx2 <- which(dat$block==2)[1]
idx3 <- which(dat$block==3)[1]
idx4 <- which(dat$block==4)[1]
# Insert
newdat <- 
  rbind(dat[1:(idx1-1),],catches[which(catches$block==1),],dat[idx1:(idx2-1),],
        catches[which(catches$block==2),],dat[idx2:(idx3-1),],
        catches[which(catches$block==3),],dat[idx3:(idx4-1),],
        catches[which(catches$block==4),],dat[idx4:nrow(dat),])

# save 
setwd(dirinput)
openxlsx::write.xlsx(x = newdat,paste0(basefilename,'C.xlsx'))

