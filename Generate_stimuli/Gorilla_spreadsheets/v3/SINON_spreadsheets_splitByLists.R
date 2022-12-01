rm(list=ls())
dirinput <- 'V:/spinco_data/SINON/Spreadsheets/PM/'
diroutput <- 'V:/spinco_data/SINON/Spreadsheets/PM/'


files <- dir(pattern = '*_GorillaC_.*.xlsx')

# Loop s
setwd(dirinput)
for (fileinput in files){
  print(fileinput)
  dat <- openxlsx::read.xlsx(xlsxFile = fileinput)  
  
  listColumns <- grep('list_',colnames(dat))
  for (c in listColumns) {
        dat2save <- dat[,-listColumns[listColumns!=c]] # remove the list columns not selected
        #save 
        outputfilename <- gsub('.xlsx',paste0('-',colnames(dat)[c],'.xlsx'),fileinput)
        openxlsx::write.xlsx(x = dat2save,file = paste0(diroutput,'/',outputfilename))          
    
  }
}

# 

