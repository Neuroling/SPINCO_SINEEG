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
audiofiles_nvoc <- 'V:/spinco_data/Audio_recordings/LIRI_voice_DF/segments/all_take1_OK_norm_vocoded/'
audiofiles_sissn <- 'V:/spinco_data/Audio_recordings/LIRI_voice_DF/segments/all_take1_OK_norm_SiSSN/'

# 
filesnvoc <- dir(audiofiles_nvoc,pattern = '*.mp3')
filessissn <- dir(audiofiles_sissn,pattern = '*.mp3')
 
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
   
 `%nin%` = Negate(`%in%`)

 audios[,1][which(audios[,1] %nin% names[,1])]

