rm(list=ls())

fileinput <- 'C:/Users/gfraga/Downloads/stimulus_words_german.xlsx'
fileoutput <- 'C:/Users/gfraga/Downloads/subtlex_select_sort.xlsx'
fileoutput2 <- 'C:/Users/gfraga/Downloads/clearpond_select_sort.xlsx'

# Read tables 
subtlex <- readxl::read_xlsx(fileinput,sheet="Subtlex-DE_all")
multipic <- readxl::read_xlsx(fileinput,sheet="Multipic-DE")
clearpond<- readxl::read_xlsx(fileinput,sheet="clearpond-DE")

# merge multipic ------------------------------------------------------------

# Select from subtlex only those available in multipic
subtlex_sel  <- subtlex[which(subtlex$Word %in% multipic$CorrectedSpelling),]
subtlex_sel[order(subtlex_sel$Word),]

#Add new variable to merge by
multipic$Word <- multipic$CorrectedSpelling 
merged <- merge(subtlex_sel,multipic,by='Word',all = TRUE)

# sort by item number
merged <- merged[order(merged$ITEM),]
merged <- dplyr::relocate(merged, ITEM,1)      # item index first 
merged <- merged[,1:which(colnames(merged)=="PICTURE")-1]# trim 
# save
openxlsx::write.xlsx(merged,fileoutput)

rm(merged)


# merge clearpond  ------------------------------------------------------------
clearpond <- clearpond[1:which(is.na(clearpond$Word)),]
clearpond <- clearpond[order(clearpond$Word),]

merged <- merge(clearpond,multipic,by='Word',all.y=TRUE)
merged <- merged[order(merged$ITEM),]
merged <- dplyr::relocate(merged, ITEM,1)      # item index first 
merged <- merged[!duplicated(merged$ITEM),]  # rmv duplicates

# save
openxlsx::write.xlsx(merged,fileoutput2)
