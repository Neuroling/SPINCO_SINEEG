
rm(list=ls())
basedir <- 'V:/spinco_data/AudioRecs/LIRI_voice_DF/segments/Take1_all_trimmed/trim_loudNorm-23LUFS_SiSSN/'
setwd(basedir)

files <- 
  c(dir(pattern = '*.1_*'))
file.rename(from = paste0(basedir,'/',files),
              to = paste0(basedir,'/', gsub('.1_','_',files)))


files <- 
  c(dir(pattern = '*.2_*'))
file.rename(from = paste0(basedir,'/',files),
            to = paste0(basedir,'/', gsub('.2_','_',files)))


       