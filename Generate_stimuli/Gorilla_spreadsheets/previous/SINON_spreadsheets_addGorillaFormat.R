rm(list=ls())
library(dplyr)
#  Prepare spreadsheets for Gorilla
#-----------------------------------------
#[GFragaGonzalez]
# - Read spreadsheets with lists of stimuli
# - Add some instructions in the breaks and format for Gorilla presentation 

dirinput <- 'V:/spinco_data/SINON/Spreadsheets'
diroutput <-  'V:/spinco_data/SINON/Spreadsheets'

# read old 
setwd(dirinput)
fileinput <- paste0(dirinput,"/LexicalDecision/TrialSequences_LD.xlsx")
tbl <- openxlsx::read.xlsx(fileinput)


# prepare for new 
if (grepl('LexicalDecision',fileinput,perl=TRUE)) {
  tbl <- tbl %>%  dplyr::rename(audio=file, correctAnswer= answer, type = noise)  
    tbl$display <- 'trial_LD'
    tbl$type <- gsub('NVoc','NV',tbl$type)
     
} else if (grepl('PictureMatching',fileinput,perl=TRUE)){
  tbl <- tbl %>%  dplyr::rename(correctAnswer= match, 
                                audio=file,
                                image_presentation=pic)  
  tbl$display <- 'trial_PM' 
  tbl$image_presentation <- paste0(tbl$image_presentation,'.tif')
  
  } else if (grepl('2ForcedChoice',fileinput,perl=TRUE)){
  tbl <- tbl %>%  dplyr::rename(audio=file_target)  
  tbl$display <- 'trial_2FC' 
  tbl$display_left <- paste0( '<h4><strong>',tbl$item_left,'</strong></h4>')
  tbl$display_right <- paste0( '<h4><strong>',tbl$item_right,'</strong></h4>')
  
}


tbl$randomise_trials <- ''
  tbl$randomise_trials[which(tbl$block=='block1')] <- 1
  tbl$randomise_trials[which(tbl$block=='block2')] <- 2
  tbl$randomise_trials[which(tbl$block=='block3')] <- 3
  tbl$randomise_trials[which(tbl$block=='block4')] <- 4


tbl$randomise_blocks <- ''
 
tbl <- tbl%>% relocate(display)
tbl <- tbl%>% relocate(randomise_trials)
tbl <- tbl%>% relocate(randomise_blocks)


  
# ADD HEADER TEXTS
headRows <- data.frame(matrix('',nrow = 3,ncol = ncol(tbl)))
colnames(headRows) <- colnames(tbl)

tbl <- rbind(headRows,tbl)
tbl$display[1:3] <- c('instruction','example','block_start')


# ADD BREAK TEXTS
# break text in between blocks
breakRow <- data.frame(matrix('',nrow = 1,ncol = ncol(tbl)))
colnames(breakRow) <- colnames(tbl)
breakRow$display <- 'break' 
  
  
idxBlockBreaks <- which(!duplicated(tbl$block))[c(-1,-2)]

newtbl <- rbind(tbl[1:idxBlockBreaks[1]-1,],
              breakRow,
              tbl[idxBlockBreaks[1]:(idxBlockBreaks[2]-1),],
              breakRow,
              tbl[idxBlockBreaks[2]:(idxBlockBreaks[3]-1),],
              breakRow,
              tbl[idxBlockBreaks[3]:nrow(tbl),])

# ADD END TEXT
# break text in between blocks
endRow <- data.frame(matrix('',nrow = 1,ncol = ncol(tbl)))
colnames(endRow) <- colnames(tbl)
endRow$display <- 'end' 
newtbl <- rbind(newtbl,endRow)



###### save table 
openxlsx::write.xlsx(newtbl,gsub('.xlsx','_Gorilla.xlsx',fileinput))

