library(readr)
library(dplyr)
library(readxl)
library(LexOPS)
library(stringr)
################################################################
# Generate table with target + distractor in a 2FC task
#-----------------------------------------------------------------
# [GFragaGonz] 
# - Find in  our LIRI database words with neighbours provided 
# - Save them and include ina new column those neighbours that are nouns (upCase)

################################################################

dirinput <- "V:/spinco_data/LIRI_database/LIRI_database_subsets"
diroutput <- dirinput
mydatabase <- 'V:/spinco_data/LIRI_database/LIRI_database_stimuli.xlsx'

setwd(dirinput)
# Read my LIRI database with potential stimuli
mytab <- openxlsx::read.xlsx(mydatabase,sheet = 'Merged')
mytab <- mytab[which(!is.na(mytab$OSAW) | !is.na(mytab$PSAW)),]

liri <- select(mytab, c('urword','PTAW','OTAW','lgSUBTLEX','nSyllables','PTAN'))

liri$altP <- liri$PSAW
liri$altO <- liri$OSAW
for (i in 1:nrow(liri)) {
  tmp <- strsplit(liri$PTAW[i],';','')   
  liri$nounPhono[i] <- paste0(tmp[[1]][which(sapply(tmp,str_detect,"[[:upper:]]")==TRUE)],collapse=';')
  liri$distractor[i] <- tmp[[1]][which(sapply(tmp,str_detect,"[[:upper:]]")==TRUE)][1]
  
  tmp <- strsplit(liri$OTAW[i],';','')  
  liri$nounOrtho[i] <- paste0(tmp[[1]][which(sapply(tmp,str_detect,"[[:upper:]]")==TRUE)],collapse=';')

}
liri$target <- liri$urword  
liri <- relocate(liri,target)
liri <- relocate(liri,distractor)
openxlsx::write.xlsx(liri,'liri_2FC_preselection.xlsx')




# 

# # read databases
# subtlex <- openxlsx::read.xlsx('V:/spinco_data/LIRI_database/SINON_LEXOPS_genMatched/SUBTLEX-DE.xlsx')
# clearpond <- openxlsx::read.xlsx('V:/spinco_data/LIRI_database/SINON_LEXOPS_genMatched/ClearPOND_edited.xlsx')
# 
# # Use some database of nouns to select only nouns from our compound database. 
# nouns <- read.csv("V:/spinco_data/LIRI_database/SINON_LEXOPS_genMatched/nouns.txt")
# # A small cheat as some plural nouns  were not found included 
# nouns$lemma <- stringi::stri_replace_all_regex(nouns$lemma,pattern = c("Olive","Wurzel","Karte", "Erbse", "Haar","Traube"), 
#                                                replacement = c("Oliven","Wurzeln","Karten", "Erbsen", "Haare","Trauben"),vectorize = FALSE)
# 
# 
# # combine info and select those from the 'nouns' file
# datbase <- merge(subtlex,clearpond, by = 'Word',all.x = FALSE, all.y=FALSE)
# datbase <- datbase[which(datbase$Word %in% nouns$lemma),]
# 
# 
# # Read my list of matched stimuli for the trials 
# setwd(dirmatched)
# matched <- list()
# for (i in 1:4){ 
#   tbl <- read.csv(dir(dirmatched,pattern=paste0('*_set',i,'.txt')),sep = '\t',header = FALSE)
#   colnames(tbl) <- c('item', 'lgSUBTLEX','PTAN','Ned1_Diff','nSyllables')
#   tbl$set <-  rep(i,nrow(tbl))
#   matched[[i]] <-tbl 
#   
# }
# matched <- data.table::rbindlist(matched)


# 
# 
# ######################################################
# # prepare main source database for using in LEXOPS package
# LANG <- datbase 
# LANG$nSyllables <- sapply(strsplit(LANG$Syllables,'-'),length)
# LANG <- relocate(LANG, nSyllables)
# LANG$string <- LANG$Word
# 
# 
# 
# 
# #################################################################################
# sel <- datbase[which(datbase$Word %in% myselecteditems),] %>% 
#         select(c('Word','gPSAW'))
# 
# sel_neighbours <- strsplit(x = sel$gPSAW,';')
# 
# sapply(sel_neighbours,length)
# all <- unlist(sel_neighbours)[!is.na(unlist(sel_neighbours))]
# 
# stringdist("aOlf","wolf",method='lv')
# 
# 
# 
#   LANG %>% mutate(phon_sim = adist(LANG$Phono, as.data.frame(LANG$Phono[which(LANG$Word==item2match)]))) %>% 
#     match_item(item2match, phon_sim )
# #####################################################
# # USING LEX OPS --------------------------------------------------------------------
# myselecteditems <- matched$item
# 
# # Find  alternatives from LexOPS for each item of matched sets ---------------
# newstim <- list() 
# for (i in 1:nrow(matched)){
#   
#   item2match <- myselecteditems[[i]]
#   
#   #find alternatives from clearpond
#   newstim[[i]] <- LANG %>% match_item(item2match,nSyllables=-0.2:0.2, gPTAN = -1:1,lgSUBTLEX=-0.25:0.25)  
#   
#   # limit them to 150
#   if (nrow(newstim[[i]])>150) {
#     newstim[[i]] <- newstim[[i]][1:150,]
#   }
#   
#    # add the info about the reference item 
#   newstim[[i]]$reference <-  rep(item2match,times = nrow(newstim[[i]]))
#   
#   # select 
#   newstim[[i]] <- select(newstim[[i]],c("reference","string","euclidean_distance","nSyllables","gPTAN","lgSUBTLEX","Phono",))
#   print(paste0('found ',nrow(newstim[[i]]),' alternatives for item ',i, ', ',item2match))
# }
# tab2save <- data.table::rbindlist(newstim)
# 
# 
# # Now select one alternative per reference item so that there is no repetitions
# refs <- unique(tab2save$reference)
# alts <- list()
# for (i in 1:length(refs)){
#  
#   curr <- tab2save[which(tab2save$reference == refs[i]),]
#   refpronounce <- LANG$Phono[which(LANG$Word==refs[i])]
#   curr<- curr %>% mutate(phon_sim = as.numeric(adist(curr$Phono,refpronounce)))
#    
#   if (i == 1){
#     alts[[i]] <- curr
# 
#   }else if (i > 1){
#       while (length(which(data.table::rbindlist(alts)[,2]==curr$string))!=0){  # if there is repetition from previous rows, shuffle the alternatives 
#             curr <- tab2save[which(tab2save$reference == refs[i]),]
#             curr <- curr[sample(nrow(curr))[1:3],]
#             print(paste0(i, ' not OK'))
#           }    
#           alts[[i]] <- curr 
#           print(paste0(i, ' OK'))
#   }
# }
# T <- data.table::rbindlist(alts)
# 
# openxlsx::write.xlsx(T, paste0(diroutput,'/LexOPS_matching.xlsx'))
#  
# 
# 
# 
# 
# 
# 
# 
