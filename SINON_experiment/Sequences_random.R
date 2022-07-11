dirinput <- 'V:/gfraga/SPINCO/Sound_files/Digits_16k'
files <- dir(path = dirinput, pattern = '*.wav') # assuming no duplicates in folder 
idx <- 1:length(files)
seq <- as.data.frame(cbind(idx,files)) # table with idx and filename 

# Some shuffled variations of the list of file names 
lists <- list()
for (i in 1:20) {
    
  lists[[i]] <- seq[order(sample(seq$idx)),] 
  colnames(lists[[i]]) <- c(paste0('idx_',i), paste0('files_',i)) # name columns with iteration n
    
}
sequences <- cbind(seq,do.call(cbind,lists))  # merge all list elemento
openxlsx::write.xlsx(file = paste0(dirinput,'/sequences.xlsx'), x = sequences)





