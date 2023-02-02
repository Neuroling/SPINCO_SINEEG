
# Read in the file names
file.list = list.files("/Users/diana/STUDY/UZH/SpringSemester2019/MA/ExpGit/PsychoPy/statistics/excelStats", full.name=T, pattern = ".+_MA.+csv")

# Package for combining files
library(dplyr)

# Function to read files into  list
Binder = function(filelist){
  file.out = list()
  for(i in 1:length(filelist)){
    file.out[[i]] = read.csv(filelist[i])
    #part = gsub(".+(\\d+)_MA.+", "\\1", filelist[i], perl=T)
    #part = gsub(".+(\\d+)_MA.+", "\\1", filelist[i], perl=T)
    #print(part)
    #file.out[[i]]$participant = part
  }
  return(file.out)
}


# Easy way to bind the files 
dat = Binder(file.list)

# Bind everything together
full_dat = bind_rows(dat)
#select interesting colums in a new data set
working_dat <- select(full_dat, callSignCorrect, colourCorrect, numberCorrect, condition, video, speaker, videoFile, order, participant) 

#---------
library(lmerTest)
#???
#l = glmer(as.factor(callSignCorrect) ~ video condition + (1|participant), data=final_dat, family="binomial")
#-----------

#-------First steps of statistical analysis------------------

library(stringr)

#exclude the first 10 Training trials
expTrials <- filter(working_dat, str_detect(working_dat$videoFile, "^video/Experiment"))
#  TODO add a new field for block A and B expTrials$half <- 

#count correct answers (there is certainly a better way to do that using R power)
count_true <- function(values) {
  counter = 0
  for (i in 1:length(values)) { 
    if (length(values[i]) & values[i] == "True") counter = counter + 1
  }
  #across all participants !! partcipant count is hardcoded
  #return(counter/(64*22))
  #within one participant
  return(counter/(64))
  
}
#across all participants - correct answers per condition for each element (sign, color, number)
aggregate(expTrials[1:3], list(condition = expTrials$condition, video = expTrials$video), count_true)

#within participant
withinPartDat <- aggregate(expTrials[1:3], list(condition = expTrials$condition, video = expTrials$video, participant = expTrials$participant), count_true)
#add a merged column condition and video (for plotting)
withinPartDat$condition_video <-  paste(withinPartDat$condition,withinPartDat$video)

#-------Plotting----------

#simple boxplots
boxplot(withinPartDat$callSignCorrect~withinPartDat$condition+withinPartDat$video, xlab="Conditions", ylab="Correct")
boxplot(withinPartDat$colourCorrect~withinPartDat$condition+withinPartDat$video, xlab="Conditions", ylab="Correct")
boxplot(withinPartDat$numberCorrect~withinPartDat$condition+withinPartDat$video, xlab="Conditions", ylab="Correct")

#install fancy boxplots (really fancy!)
install.packages(c("tidyverse", "ggstatsplot"))
library("tidyverse", "ggstatsplot")

# plot callSign
ggstatsplot::ggbetweenstats(data = withinPartDat, 
               x = condition_video,
               y = callSignCorrect,
               outlier.tagging = TRUE,
               outlier.label = participant)
# plot colour
ggstatsplot::ggbetweenstats(data = withinPartDat, 
                            x = condition_video,
                            y = colourCorrect,
                            outlier.tagging = TRUE,
                            outlier.label = participant)
# plot number
ggstatsplot::ggbetweenstats(data = withinPartDat, 
                            x = condition_video,
                            y = numberCorrect,
                            outlier.tagging = TRUE,
                            outlier.label = participant)



#----------Correctness over whole sentences--------
sentCorrDat <- expTrials
sentCorrDat <- transform(sentCorrDat, 
                                         sentenceCorrect=ifelse(callSignCorrect=="True" 
                                                                & colourCorrect=="True"
                                                                & numberCorrect=="True",
                                                                "True", "False")
                                         )

count_true <- function(values) {
  counter = 0
  for (i in 1:length(values)) { 
    if (length(values[i]) & values[i] == "True") counter = counter + 1
  }
  #across all participants !! partcipant count is hardcoded
  #return(counter/(64*22))
  #within one participant
  return(counter/(64))
  
}


withinPartSentDat <- aggregate(sentCorrDat[10], list(condition = sentCorrDat$condition, video = sentCorrDat$video, participant = sentCorrDat$participant), count_true)
withinPartSentDat$condition_video <-  paste(withinPartSentDat$condition,withinPartSentDat$video)

# plot sentence correctness
ggstatsplot::ggbetweenstats(data = withinPartSentDat, 
                            x = condition_video,
                            y = sentenceCorrect,
                            outlier.tagging = TRUE,
                            outlier.label = participant)
