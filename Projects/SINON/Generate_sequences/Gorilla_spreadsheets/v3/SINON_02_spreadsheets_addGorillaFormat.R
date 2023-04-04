rm(list=ls())
library(dplyr)
#  Prepare spreadsheets for Gorilla
#-----------------------------------------
#[GFragaGonzalez]
# - Read spreadsheets with lists of stimuli
# - Add some instructions in the breaks and format for Gorilla presentation 

dirinput <- 'V:/spinco_data/SINON/Spreadsheets/LD'
diroutput <-  'V:/spinco_data/SINON/Spreadsheets/LD'

# read old 
setwd(dirinput)
fileinput <- paste0(dirinput,"/Spreadsheets_2FC.xlsx")
tbl <- openxlsx::read.xlsx(fileinput)

# prepare for new 
if (grepl('_LD',fileinput,perl=TRUE)) {
  tbl <- tbl %>%  dplyr::rename( correctAnswer= answer)  
    tbl$display <- 'trial_LD'
      
} else if (grepl('_PM',fileinput,perl=TRUE)){
  tbl <- tbl %>%  dplyr::rename(correctAnswer= match, 
                                image_presentation=picture)  
  tbl$display <- 'trial_PM' 
  tbl$image_presentation <- paste0(tbl$image_presentation,'.jpg')
  
  } else if (grepl('_2FC',fileinput,perl=TRUE)){
  #tbl <- tbl %>%  dplyr::rename(audio=file_target)  
  tbl$display <- 'trial_2FC' 
  tbl$display_left <- paste0( '<h1><strong>',tbl$item_left,'</strong></h1>')
  tbl$display_right <- paste0( '<h1><strong>',tbl$item_right,'</strong></h1>')
  
}


tbl$randomise_trials <- ''
  tbl$randomise_trials[which(tbl$block=='1')] <- 1
  tbl$randomise_trials[which(tbl$block=='2')] <- 2
  tbl$randomise_trials[which(tbl$block=='3')] <- 3
  tbl$randomise_trials[which(tbl$block=='4')] <- 4


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


### ADD example item 
exIdx <- which(newtbl$display=='example')
example_audiofile <- 'EXAMPLE_SiSSN_Mais_norm10db.wav'
example_item <- 'Mais'


if (grepl('_LD',fileinput,perl=TRUE)) { # depends on the task
    newtbl$item[exIdx] <-  example_item  
    newtbl$correctAnswer[exIdx] <- 'word'
    newtbl[exIdx,which(grepl('list',colnames(newtbl)))] <-  example_audiofile
  
} else if (grepl('_PM',fileinput,perl=TRUE)){
    newtbl$item[exIdx] <-  example_item
    newtbl$image_presentation[exIdx] <- 'PICTURE_587.jpg'
    newtbl$correctAnswer[exIdx] <- 1
    newtbl[exIdx,which(grepl('list',colnames(newtbl)))] <-  example_audiofile

 
} else if (grepl('_2FC',fileinput,perl=TRUE)){
  newtbl$correctAnswer[exIdx] <- 'left'
  
  newtbl$item_left[exIdx] <- example_item
  newtbl$item_right[exIdx] <- 'Maus'
  
  newtbl$item_target[exIdx] <- example_item 
  newtbl$item_distractor[exIdx] <- 'Maus'
  newtbl[exIdx,which(grepl('list',colnames(newtbl)))] <-  example_audiofile
  
}

###### save table 
openxlsx::write.xlsx(newtbl,gsub('.xlsx','_Gorilla.xlsx',fileinput))

