rm(list=ls())

fileinput <- 'C:/Users/gfraga/Downloads/stimulus_words_german.xlsx'

# Read tables 
subtlex <- readxl::read_xlsx(fileinput,sheet="Subtlex-DE")
multipic <- readxl::read_xlsx(fileinput,sheet="Multipic-DE")
clearpond<- readxl::read_xlsx(fileinput,sheet="Clearpond-DE")
wuggy <- readxl::read_xlsx(fileinput,sheet="Wuggy-DE") 

# Summary info 

subtlex_cols <- ncol(subtlex)
subtlex_missing <- length(which(is.na(subtlex[,3])))
subtlex_completed <- nrow(subtlex)- length(which(is.na(subtlex[,3])))

clearpond_cols <- ncol(clearpond)
clearpond_missing <- length(which(is.na(clearpond[,3])))
clearpond_completed <- nrow(clearpond)- length(which(is.na(clearpond[,3])))




# summary wuggy 

wuggy$Word_plain <- gsub('-','',wuggy$Word)
wuggy$ITEM <- wuggy$Word_plain
wuggy <- dplyr::relocate(wuggy,ITEM)
wuggywords <- unique(wuggy$Word_plain)

for (i in 1:length(wuggywords)){
  
  item <- multipic$ITEM[which(multipic$CORRECT_SPELL==wuggywords[i])]  
  if (length(item)!=0){
    
    wuggy$ITEM[which(wuggy$Word_plain==wuggywords[i])] <- item
    
    
  } else {
    wuggy$ITEM[which(wuggy$Word_plain==wuggywords[i])] <- '0'
    
    
  }
  
}
wuggy$ITEM <- as.numeric(wuggy$ITEM)
wuggy <- wuggy[order(wuggy$ITEM),]

wuggy_cols <- ncol(wuggy)
wuggy_completed <- length(which(multipic$ITEM %in% unique(wuggy$ITEM)))
wuggy_missing <- nrow(multipic)-wuggy_completed



### Gather 


tbl <-rbind(c('multipic',ncol(multipic),nrow(multipic),nrow(multipic)),
            c('subtlex',subtlex_cols,subtlex_completed,subtlex_missing),
            c('clearpond', clearpond_cols,clearpond_completed,clearpond_missing),
            c('wuggy', wuggy_cols,wuggy_completed,wuggy_missing))

colnames(tbl) <- c('database','n_variables','items_completed','items_missing')
tbl <- as.data.frame(tbl)


#
openxlsx::write.xlsx(tbl, 'C:/Users/gfraga/Downloads/sinon_database_summary.xlsx')
