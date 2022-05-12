 
# Function to read EEG data, save summary of dimensions and basic marker info 
check_eeg <- function(headerfile) {
        if (file.info(headerfile)$size!=0) { #some files of size 0 existed...
            
            #gather basic eeg data info
            header  <-   raveio::read_eeg_header(file = headerfile)
            eeg     <-      raveio::read_eeg_data(header, path = gsub('.vhdr','.eeg',headerfile))
            dimensions <<- t(c(dim(eeg$data)))
            colnames(dimensions) <- c('rows','columns')
            
            #gather basic markers info
            mrkrs   <- ini::read.ini(gsub('.vhdr','.vmrk',headerfile))
            mrkrs   <- mrkrs$`Marker Infos`
            
            mrkrsTab  <- data.frame(matrix(unlist(mrkrs), nrow=length(mrkrs), byrow=TRUE))
            colnames(mrkrsTab) <- 'Name'
            mrkrsTab <- mrkrsTab %>% separate(Name, c('type', 'label','time','v1','v2'),sep = ',')
            mrkrsInfo <- as.data.frame(t(c(length(unique(mrkrsTab$label)),mrkrsTab$time[1],mrkrsTab$time[nrow(mrkrsTab)],mrkrsTab$label[1],mrkrsTab$label[nrow(mrkrsTab)])))
            mrkrsInfo <<- mrkrsInfo
            
        } else { 
            warning(paste0(headerfile, ' has size 0!'))
            dimensions<<-  as.data.frame(matrix(NA,nrow=1,ncol=2))
            mrkrsInfo <<- as.data.frame(matrix(NA,nrow=1,ncol=5))
          
        }  
          colnames(dimensions) <<- c('rows','cols')
          colnames(mrkrsInfo) <<- c('n_unique_markers','first_marker_time','last_marker_time','first_marker_label','last_marker_label')
  }
   