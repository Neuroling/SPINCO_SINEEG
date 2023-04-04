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
matchedSets <- 'V:/spinco_data/LIRI_database/SINON_MATCH_v3/PM_20items/'
databasefile <-'V:/spinco_data/LIRI_database/LIRI_database_stimuli.xlsx'

setwd(dirinput)
dat <- openxlsx::read.xlsx(paste0(basefilename,'.xlsx'))
database <- openxlsx::read.xlsx(databasefile,sheet = 'Merged')

# find 4  additional sets..
catches <- list()
for (i in 1:4){
  fileinput <- paste0(matchedSets,'list2match20_set',20+i,'.txt')
  tab <- read.delim(fileinput,header = FALSE)  
  items <- tab$V1 
  # picture selection  ------------------------------------------------
  pic <- ''
    for (p in 1:nrow(tab)){
      pic[p] <- database$PICTURE[which(database$CORRECT_SPELL == items[p])]    
    }
  urpic <- pic  #this one is just for testing
  
    # shuffle the pictures for the trials marked as not a match
    match <- c(rep(1,length(items)/2),rep(0,length(items)/2)) %>% sample()
    original  <-pic[which(match==0)]
    replacement <- sample(original)
    while (length(which(original==replacement)>0)!=0) {# shuffle again until no name repeats position 
      replacement <- sample(original)
    } 
    pic[match==0] <- replacement
  # ------------------------------------------------
  # compose catch trials
  catches [[i]]<- 
    as.data.frame(rbind(cbind('',i,'catch_trial',i,items,paste0(pic,'.jpg'),match,
                              replicate(n=5,paste0('SiSSN_',items,'_norm15db.wav')),
                              replicate(n=5,paste0('NV_',items,'_norm_32ch_1p.wav')))))
  

    colnames(catches[[i]]) <- colnames(dat)

  
}

catches <-  do.call(rbind,catches)
# Alternating NV/ SISSN order
order1 = which(catches$block==1 | catches$block==3)
catches[order1,grepl('list.*',colnames(catches))] <-  cbind(replicate(n=5,paste0('SiSSN_',catches$item[order1],'_norm15db.wav')),replicate(n=5,paste0('NV_',catches$item[order1],'_norm_32ch_1p.wav')))

order2 = which(catches$block==2 | catches$block==4)
catches[order2,grepl('list.*',colnames(catches))] <-  cbind(replicate(n=5,paste0('NV_',catches$item[order2],'_norm_32ch_1p.wav')),replicate(n=5,paste0('SiSSN_',catches$item[order2],'_norm15db.wav')))



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

 