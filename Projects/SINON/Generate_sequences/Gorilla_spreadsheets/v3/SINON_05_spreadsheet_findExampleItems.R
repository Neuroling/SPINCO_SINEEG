rm(list=ls())

# Find example items not prsent in any of the task  
###########################################################
dirinput <- 'V:/spinco_data/SINON/Spreadsheets/'
diroutput <-  'V:/spinco_data/SINON/Spreadsheets/ExampleItem'
dir.create(diroutput)

setwd(dirinput)
# Find all items in database 
database <- openxlsx::read.xlsx('V:/spinco_data/LIRI_database/LIRI_database_stimuli.xlsx',sheet = 'Merged')
# Discards those for which there is no audiofile 
audiofiles_sissn <- 'V:/spinco_data/AudioRecs/LIRI_voice_DF/segments/Take1_all_trimmed/trim_loudNorm-23LUFS_SiSSN/'
filessissn <- dir(audiofiles_sissn,pattern = 'S*.wav')
itemsWithFiles <- sapply(strsplit(filessissn,'_'),'[[',2)
indices <- c(which(database$CORRECT_SPELL %in% itemsWithFiles),which(gsub('-','',database$Pseudoword) %in% itemsWithFiles))
database <- database[indices[duplicated(indices)],]

# list items
itemsInDatabase <- c(database$CORRECT_SPELL)


# find files in experiment
setwd(dirinput)
files <- dir(pattern = '*.wav',recursive = TRUE)
files <- files[grepl('files/',files)]
itemsInExperiment <- unique(sapply(strsplit(files,'_'),'[[',2))

# Find an item in database that is not used in the experiment
`%nin%` = Negate(`%in%`)
itemsExample <- itemsInDatabase[which(itemsInDatabase %nin% itemsInExperiment)]


# Find corresponding files 
      myselection <- 3 # eyeballing items I picked this 
      idx <- c(which(database$CORRECT_SPELL==itemsExample[myselection]))
    # Picture 
    file.copy( from = paste0('V:/spinco_data/LIRI_database/Multipic_pictures/colored_TIFF/',paste0(database[idx,]$PICTURE,'.tif')),
              to= diroutput)
        library("jpeg")
        library("tiff")
        # Convert to jpg
        setwd(diroutput)
        tifs <- dir(pattern='*.tif$')
        for (i in 1:length(tifs)){
          img <- readTIFF( tifs[i], native=TRUE)
          writeJPEG(img, target = gsub('.tif','.jpg',tifs[i]), quality = 1)  
        }
        
    
    # Sounds (with lowest level of noise)
      file.copy(from = paste0(audiofiles_sissn,paste0('/SiSSN_',itemsExample[myselection],'_norm10db.wav')),
               to = diroutput)
      
    
    
    
    
# examples2use <- list()
# for (i in length(itemsExample)){
#   
#   findword <- which(database$CORRECT_SPELL==itemsExample[i])  
#   findpseudo <- which(gsub('-','',database$Pseudoword)==itemsExample[i])  
#   
#   if (length(findword) != 0){
#         databfindword
#   } else if (length(findpseudo != 0)){
#     
#   }
# }



