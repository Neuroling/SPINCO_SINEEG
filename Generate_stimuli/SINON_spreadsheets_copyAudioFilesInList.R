rm(list=ls())
library(dplyr)
library(tidyr)
###############################################################################
# READ SPREADSHEET AND COPY AUDIO FILES
# ----------------------------------------------------------------------------
# - Read xls spreadsheet for Gorilla containing file names
# - copy the corresponding files in the same folder as spreadsheet
###############################################################################
dirinput <- 'V:/spinco_data/SINON/Spreadsheets/2ForcedChoice/'
diroutput <- dirinput
filename <- 'TrialSequences_2FC.xlsx'
setwd(dirinput)

#audiofiles dir 
audiofiles_nvoc <- 'V:/spinco_data/AudioRecs/LIRI_voice_DF/segments/Take1_all_trimmed/trim_loudNorm-23LUFS_NV/'
audiofiles_sissn <- 'V:/spinco_data/AudioRecs/LIRI_voice_DF/segments/Take1_all_trimmed/trim_loudNorm-23LUFS_SiSSN/'

# 
filesnvoc <- dir(audiofiles_nvoc,pattern = 'N*.wav')
filessissn <- dir(audiofiles_sissn,pattern = 'S*.wav')

# `%nin%` = Negate(`%in%`)

#-----------------------------------------------------------------------
# search files and concat 
sheet <- openxlsx::read.xlsx(filename)
colwithfiles <- grepl('*.wav',sheet)
 
# save only if not previously saved
  files2copy <- sheet[,colwithfiles][grepl('.wav',sheet[,colwithfiles])]
  newdir <- paste0(diroutput, 'files')
  dir.create(newdir)
  file.copy(paste0(audiofiles_sissn,filessissn[which(filessissn %in% files2copy)]),newdir)
  file.copy(paste0(audiofiles_nvoc,filesnvoc[which(filesnvoc %in% files2copy)]),newdir)
   
if (grepl('PictureMatching',dirinput)) {
  
     pics <- dir('V:/spinco_data/LIRI_database/Multipic_pictures/colored_TIFF',pattern='*.tif')
     files2copy <-  pics[which(pics %in% paste0(sheet$pic,'.tif'))]
     file.copy(paste0('V:/spinco_data/LIRI_database/Multipic_pictures/colored_TIFF/',files2copy),newdir)
     
     
     library("jpeg")
     library("tiff")
     # Convert to jpg
     setwd(dirinput)
     tifs <- dir(path = dirinput, pattern='*.tif$')
     for (i in 1:length(tifs)){
       img <- readTIFF(tifs[i], native=TRUE)
       writeJPEG(img, target = gsub('.tif','.jpg',tifs[i]), quality = 1)  
     }
     
    
  
}
 