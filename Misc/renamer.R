
rm(list=ls())
basedir <- 'V:/spinco_data/Audio_recordings/LIRI_voice_DF/'
setwd(basedir)

files <- 
  dir(pattern = '^wald_*',recursive = TRUE)


file.rename(from = paste0(basedir,'/',files),
              to = paste0(basedir,'/', gsub('wald_','Wald_',files)))


       