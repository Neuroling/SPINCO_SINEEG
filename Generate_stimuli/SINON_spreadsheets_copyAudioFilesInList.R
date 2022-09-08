rm(list=ls())
library(dplyr)
library(tidyr)
###############################################################################
# READ SPREADSHEET AND COPY AUDIO FILES
# ----------------------------------------------------------------------------
# - Read xls spreadsheet for Gorilla containing file names
# - copy the corresponding files in the same folder as spreadsheet
###############################################################################
dirinput <- 'V:/spinco_data/SINON/Spreadsheets/PictureMatching/'
diroutput <- dirinput
filename <- 'TrialSequences_PM.xlsx'
setwd(dirinput)

#audiofiles dir 
audiofiles_nvoc <- 'V:/spinco_data/Audio_recordings/LIRI_voice_DF/segments/all_take1_OK_norm_vocoded/'
audiofiles_sissn <- 'V:/spinco_data/Audio_recordings/LIRI_voice_DF/segments/all_take1_OK_norm_SiSSN/'

# 
filesnvoc <- dir(audiofiles_nvoc,pattern = '*.mp3')
filessissn <- dir(audiofiles_sissn,pattern = '*.mp3')

# `%nin%` = Negate(`%in%`)

#-----------------------------------------------------------------------
# search files and concat 
sheet <- openxlsx::read.xlsx(filename)
colwithfiles <- grepl('*.mp3',sheet)
 
# save only if not previously saved
  files2copy <- sheet[,colwithfiles][grepl('.mp3',sheet[,colwithfiles])]
  newdir <- paste0(diroutput, paste0('files_',gsub('.xlsx','',filename)))
  dir.create(newdir)
  file.copy(paste0(audiofiles_sissn,filessissn[which(filessissn %in% files2copy)]),newdir)
  file.copy(paste0(audiofiles_nvoc,filesnvoc[which(filesnvoc %in% files2copy)]),newdir)
   
if (grepl('PictureMatching',dirinput)) {
  
     pics <- dir('V:/spinco_data/LIRI_database/Multipic_pictures/colored_TIFF',pattern='*.tif')
     files2copy <-  pics[which(pics %in% paste0(sheet$pic,'.tif'))]
    file.copy(paste0('V:/spinco_data/LIRI_database/Multipic_pictures/colored_TIFF/',files2copy),newdir)
  
}
 