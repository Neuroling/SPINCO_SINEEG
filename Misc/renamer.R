
rm(list=ls())
basedir <- 'V:/spinco_data/Audio_recordings/LIRI_voice_DF/segments/macro-output/normalized-25db/'
setwd(basedir)

files <- 
  dir(pattern = '*.mp3',recursive = TRUE)


file.rename(from = paste0(basedir,'/',files),
              to = paste0(basedir,'/', gsub('_trim','_norm',files)))


       