rm (list=ls())
library("jpeg")
library("tiff")



## Select pictures to copy to Gorilla
spreadsheet <- openxlsx::read.xlsx("V:/spinco_data/SINON/Spreadsheets/PictureMatching/TrialSequences_PIC.xlsx")
picdir <- "V:/spinco_data/LIRI_database/Multipic_pictures/colored_TIFF/"
diroutput <- "V:/spinco_data/SINON/Spreadsheets/PictureMatching/files/"

# files 

files <- dir(picdir)
 
files2copy <- files[which(gsub('.tif','',files) %in%  spreadsheet$pic )]

for (i in 1:length(files2copy)){
  
  img <- readTIFF(paste0(picdir,files2copy[i]), native=TRUE)
   
  writeJPEG(img, target = paste0(diroutput,gsub('.tif','.jpeg',files2copy[i])), quality = 1)
    
  
}

 