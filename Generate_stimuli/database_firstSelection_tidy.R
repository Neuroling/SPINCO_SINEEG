rm(list=ls())
library(dplyr)
library(tidyr)

fileinput <- 'V:/spinco_data/Database_stimuli/Neuroling_stimuli.xlsx'
fileoutput <- 'V:/spinco_data/Database_stimuli/tmp_merged.xlsx'


# Read tables 
w0 <- openxlsx::read.xlsx(fileinput,sheet="Wuggy_selected",detectDates = FALSE)
w1 <- openxlsx::read.xlsx(fileinput,sheet="Wuggy_selected_alt",detectDates = FALSE)
w2 <-openxlsx::read.xlsx(fileinput,sheet="Wuggy_selected_alt2",detectDates = FALSE)
merged <-openxlsx::read.xlsx(fileinput,sheet="Merged",detectDates = FALSE) 

# select cols
cols0 <- c("Word","Match","Lexicality","Old20", "Old20_Diff","Ned1","Ned1_Diff","Overlap_Ratio","Maxdeviation","Summed_Deviation","Maxdeviation_Transition")
w0<-select(w0,all_of(cols0))

cols1 <- c("Word","Alternative","Lexicality","Old20", "Old20_Diff","Ned1","Ned1_Diff","Overlap_Ratio","Maxdeviation","Summed_Deviation","Maxdeviation_Transition")
w1<-select(w1,all_of(cols1))

cols2 <- c("Word","Alternative2","Lexicality","Old20", "Old20_Diff","Ned1","Ned1_Diff","Overlap_Ratio","Maxdeviation","Summed_Deviation","Maxdeviation_Transition")
w2<-select(w2,all_of(cols2))

# fill new table 
ww <-w0 
colnames(ww)[which(colnames(ww)=='Match')] <- 'Pseudoword'

idx2 <- which(!is.na(w2$Alternative2))
idx1 <- which(!is.na(w1$Alternative))

ww[idx2,] <- w2[idx2,]
ww[idx1,] <- w1[idx1,]

# save into 'merged' table 
ww$urword <- ww$Word # for verification purposes 
merged$Word <- merged$CORRECT_SPELL
newmerged <- merge(ww,merged, by = 'Word',all = FALSE)


#
openxlsx::write.xlsx(newmerged,fileoutput) # this is just a temporary file 