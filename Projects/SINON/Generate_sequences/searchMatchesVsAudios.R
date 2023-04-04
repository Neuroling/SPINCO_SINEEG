rm(list=ls())

spreadsheet <- 'V:/spinco_data/SINON/Spreadsheets/LexicalDecision/TrialSequences_LD.xlsx'
audiodir <- 'V:/spinco_data/Audio_recordings/LIRI_voice_DF/segments/All_mp3s/SiSSN'

#read spreadsheet
sel <- openxlsx::read.xlsx(spreadsheet)

# read mp3s available 
mp3s <- dir(audiodir,pattern='*.mp3')
mp3s_names <- as.character(sapply(sapply(mp3s,strsplit,'_'),'[[',2))
mp3s_snr  <- as.character(sapply(sapply(mp3s,strsplit,'OK'),'[[',2) %>% gsub('.mp3','',.))
  
`%nin%` = Negate(`%in%`)
sel$item[which(sel$item %nin% mp3s_names)][order(sel$item[which(sel$item %nin% mp3s_names)])]
head(mp3s_names[order(mp3s_names)],65)




##
subs <- list()
setwd(dirinput)
for (i in 1:4){
  currSet <-read.table(paste0('list2match_set',i,'.txt'))
  subs[[i]] <- as.data.frame(currSet$V1)
}
subs <- data.table::rbindlist(subs)
colnames(subs) <- 'name'

# 
files <- c(dir(wordAudiofiles),dir(pseudowordAudiofiles))
files <- as.character(sapply(sapply(files,strsplit,'_'),'[[',1))

