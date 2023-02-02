######################################
# List sequences of wav files 
###################################
# Read data
rm(list=ls())
dirinput <- 'V:/spinco_data/Sound_files/LIRI_voice_SM/words_v1_speechDetect_OK'
dirinput_vocoded <- 'V:/spinco_data/Sound_files/LIRI_voice_SM/words_v1_speechDetect_OK_vocoded'
diroutput <- 'V:/spinco_data/Sound_files/LIRI_voice_SM/'


### Split in sets   
#-------------------------------------
files <- dir(path = dirinput, pattern='*.wav')
nTrialsInSet <- 100 
nSets <- 5 
# Select files from set 
files <- as.data.frame(files[sample(length(files))])  # first shuffle to avoid bias by alphabetic sorting

if(nTrialsInSet*nSets !=nrow(files)){ 
  warning('Trimming dataset to match nTrialsInSet*nSets')
  files <- as.data.frame(files[1:(nTrialsInSet*nSets),])
}
colnames(files) <- 'item'

# Add info for subsetting 
files$setIdx <- as.factor(rep(1:nSets, each = nTrialsInSet))
files$setTrial <- as.factor(rep(1:nTrialsInSet,nSets))

## Split the data 
sets <- split(files,files$setIdx)
  
#generate versions for the different snr 

snr = c('3chans','4chans','5chans','7chans','9chans')
nvfiles <- dir(dirinput_vocoded,'*.wav')
setsWithNoise <- list()
for (i  in 1:length(sets)) {
  
  currset <- sets[[i]]
  snr <- snr[sample(length(snr))]
  versions <- list()
  for(ii in 1:length(snr)){
    versions[[ii]] <- paste0("NoVoc_",gsub('.wav',paste0('_',snr[ii],'.wav'),currset$item))    
  
  }
  versions <- as.data.frame(do.call(cbind,versions))
  versions <- as.data.frame(t(apply(versions,1,sample))) # shuffle the rows of each column independently 
  setsWithNoise[[i]] <- cbind(paste0('set',i),versions)
  colnames(setsWithNoise[[i]])[1] <- 'setNum'
}
#setsWithNoise <- data.table::rbindlist(setsWithNoise)
#colnames(setsWithNoise)[1] <- 'setNum'

#Write to file
for (i in 1:length(setsWithNoise)){
  outputfile <- paste0(diroutput,'/sequence_',i,'.xlsx')
  openxlsx::write.xlsx(setsWithNoise[[i]],outputfile)  
  
}




