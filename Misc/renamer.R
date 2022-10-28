
rm(list=ls())
basedir <- 'V:/spinco_data/AudioRecs/LIRI_voice_DF/segments/Take1_all_trimmed/trim_loudNorm-23LUFS_NV32ch_cued/'
setwd(basedir)

files <- 
  c(dir(pattern = '*.1p*'))


file.rename(from = paste0(basedir,'/',files),
              to = paste0(basedir,'/', gsub('.1p','_32ch_1p',files)))



       