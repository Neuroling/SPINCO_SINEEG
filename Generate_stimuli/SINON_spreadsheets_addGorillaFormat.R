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
  tbl <- tbl %>%  dplyr::rename(audio=file)  
  #excess block removal (in LD task)
  tbl <- tbl[-which(tbl$block=='block5'),]
  tbl$display <- 'trial_LD'
  
} else if (grepl('PictureMatching',fileinput,perl=TRUE)){
  tbl <- tbl %>%  dplyr::rename(ANSWER= match, 
                                audio=file,
                                image_presentation=pic)  
  tbl$display <- 'trial_PM' 
}

tbl$randomise_trials <- 1
tbl$instruction_left <- ''
tbl$instruction_right<- ''
tbl$randomise_blocks <- ''
tbl <- tbl%>% relocate(display)
tbl <- tbl%>% relocate(randomise_trials)
tbl <- tbl%>% relocate(randomise_blocks)

# TEXTS
 
ins_left <- "<h3>Instruction</h3> <h4>During the experimental blocks you will first see a fixation cross, followed by a brief audio of degraded speech. 
         After the sound, an image will be presented. Your task is to indicate whether the image matches the sound.
         <br/><ul><li>Press L<strong><span style=\"font-size: 250%;\"><span>&#8592;</span></strong></span> if they <strong>match</strong>.
         <br/><li>Press R<strong><span style =\"font-size: 250%;\"><span>&#8594;</span></span></strong> if they <strong>differ</strong>.
          </ul><br/>There is 4 blocks in this experiment, every block will last ~<strong>TIMING</strong> and the instruction are the same for each block. 
          Before starting, click <strong>PLAY</strong> to see an example.</h4>"

ins_right <-"<h3>Instruction</h3> <h4>During the experimental blocks you will first see a fixation cross, followed by a brief audio of degraded speech. 
         After the sound, an image will be presented. Your task is to indicate whether the image matches the sound.
         <br/><ul><li>Press R<strong><span style=\"font-size: 250%;\"><span>&#8592;</span></strong></span> if they <strong>match</strong>.
         <br/><li>Press L<strong><span style =\"font-size: 250%;\"><span>&#8594;</span></span></strong> if they <strong>differ</strong>.
          </ul><br/>There is 4 blocks in this experiment, every block will last ~<strong>TIMING</strong> and the instruction are the same for each block. 
          Before starting, click <strong>PLAY</strong> to see an example.</h4>"

ins_left_ex <- "<h3>Example</h3><h4>Here the sound presented and the image were \"blabla\", so you would have pressed <strong> L <span style=\"font-size: 250%;\"><span>&#8592;</span></strong></span>  for <strong>match</strong>.</h4>"
ins_right_ex <- "<h3>Example</h3><h4>Here the sound presented and the image were \"blabla\", so you would have pressed <strong> R <span style=\"font-size: 250%;\"><span>&#8592;</span></strong></span>  for <strong>match</strong>.</h4>"

ins_left_2 <- "<h3>Experimental block</h3> <h4>By pressing <strong>START</strong> you will start an experimental block. Reminder:<ul><li>Press <strong><span style=\"font-size: 250%;\"><span>&#8592;</span></strong></span> if the sound and the picture <strong>match</strong>.<br/><li>Press <strong><span style =\"font-size: 250%;\"><span>&#8594;</span></span></strong> if they <strong>differ</strong>.</ul><br/> After each sound you have 2 seconds to answer. </h4>"
ins_right_2 <- "<h3>Experimental block</h3> <h4>By pressing <strong>START</strong> you will start an experimental block. Reminder:<ul><li>Press <strong><span style=\"font-size: 250%;\"><span>&#8592;</span></strong></span> if the sound and the picture <strong>match</strong>.<br/><li>Press <strong><span style =\"font-size: 250%;\"><span>&#8594;</span></span></strong> if they <strong>differ</strong>.</ul><br/> After each sound you have 2 seconds to answer. </h4>"

brk <- "<h3>Break</h3><h4> You have completed an experimental block. By pressing <strong>START</strong> you will start the next one. Reminder: <ul><li> Press <strong><span style=\"font-size: 250%;\"><span>&#8592;</span></strong></span> if the sound and the picture <strong>match</strong>.<br/><li>Press <strong><span style =\"font-size: 250%;\"><span>&#8594;</span></span></strong> if they <strong>differ</strong>.</ul><br/> After each sound you have 2 seconds to answer. </h4>"
end <- "<h3>FINISH</h3><h4> Congratus <strong> YOU ARE DONE </strong> that's it  <ul><li> Press <strong><span style=\"font-size: 250%;\"><span>&#8592;</span></strong></span> </h4>"

# ADD HEADER TEXTS
headRows <- data.frame(matrix('',nrow = 3,ncol = ncol(tbl)))
colnames(headRows) <- colnames(tbl)

tbl <- rbind(headRows,tbl)
tbl$display[1:3] <- c('instruction','example','block_start')
tbl$instruction_left[1:3] <- c(ins_left,ins_left_ex,ins_left_2)
tbl$instruction_right[1:3] <- c(ins_right,ins_right_ex,ins_right_2)

# ADD BREAK TEXTS
# break text in between blocks
breakRow <- data.frame(matrix('',nrow = 1,ncol = ncol(tbl)))
colnames(breakRow) <- colnames(tbl)
breakRow$display <- 'break'
breakRow$instruction_left <- brk
breakRow$instruction_right <- brk
  
  
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
endRow$instruction_left <- end
endRow$instruction_right <- end
newtbl <- rbind(newtbl,endRow)
#add count of trials 

newtbl$trialNum <- newtbl$block  
trialidxseq <- paste0('trial_',sprintf("%03d", 1:length(which(newtbl$trialNum == 'block1'))))
newtbl$trialNum[which(newtbl$trialNum == 'block1')] <- trialidxseq
newtbl$trialNum[which(newtbl$trialNum == 'block2')] <- trialidxseq
newtbl$trialNum[which(newtbl$trialNum == 'block3')] <- trialidxseq
newtbl$trialNum[which(newtbl$trialNum == 'block4')] <- trialidxseq


###### save table 
openxlsx::write.xlsx(newtbl,gsub('.xlsx','_Gorilla.xlsx',fileinput))

