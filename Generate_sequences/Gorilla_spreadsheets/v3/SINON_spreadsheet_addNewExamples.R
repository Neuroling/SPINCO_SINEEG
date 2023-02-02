rm(list=ls())
###############################################################################
#  MODIFY THE EXAMPLES 
# - Insert new example 
# - Do NOT touch the rest... 
# - OVERWRITES!

###############################################################################

# ----------------------------------------------
### Read files
dirinput <- 'V:/spinco_data/SINON/Spreadsheets/2FC/'
diroutput <- dirinput 

files <- dir(dirinput,pattern= '*GorillaC_.*.xlsx')
setwd(dirinput)

for (f in 1:length(files)){
  dat <- openxlsx::read.xlsx(files[f])  
  newexample <- dat[2,]
  newexample[1,9:18] <- gsub('_SiSSN_Mais_norm10db.wav','_NV_Mais_norm_0.95p.wav',newexample[1,9:18])
  # 
  newdat <- rbind(dat[1:2,],newexample,dat[3:nrow(dat),])

  # save 
  setwd(dirinput)
  openxlsx::write.xlsx(x = newdat,files[f])
  
  
}

