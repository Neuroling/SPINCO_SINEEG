dirinput <- 'V:/spinco_data/SINON/Spreadsheets/PM/'
basefilename <- 'Spreadsheets_PM_Gorilla'
setwd(dirinput)



dat <- openxlsx::read.xlsx(paste0(basefilename,'.xlsx'))
dat$randomise_blocks
urRandTrials <- dat$randomise_trials
urBlockOrder <- dat$block
dat$set <- dat$block 
dat$set <- gsub('1','a',dat$set)
dat$set <- gsub('2','b',dat$set)
dat$set <- gsub('3','c',dat$set)
dat$set <- gsub('4','d',dat$set)

dat <- dplyr::relocate(dat, set, .before='block')


uridx1 <- which(dat$block=='1')
uridx2 <- which(dat$block=='2')
uridx3 <- which(dat$block=='3')
uridx4 <- which(dat$block=='4')


newdat <- dat
newdat[uridx1,] <- dat[uridx1,]
newdat[uridx2,] <- dat[uridx2,]
newdat[uridx3,] <- dat[uridx3,]
newdat[uridx4,] <- dat[uridx4,]
newdat$randomise_trials <- urRandTrials
newdat$block <- urBlockOrder
openxlsx::write.xlsx(paste0(basefilename,'_abcd.xlsx'),x = newdat)

newdat <- dat
newdat[uridx1,] <- dat[uridx3,]
newdat[uridx2,] <- dat[uridx2,]
newdat[uridx3,] <- dat[uridx1,]
newdat[uridx4,] <- dat[uridx4,]
newdat$randomise_trials <- urRandTrials
newdat$block <- urBlockOrder
openxlsx::write.xlsx(paste0(basefilename,'_cbad.xlsx'),x = newdat)

newdat <- dat
newdat[uridx1,] <- dat[uridx1,]
newdat[uridx2,] <- dat[uridx4,]
newdat[uridx3,] <- dat[uridx3,]
newdat[uridx4,] <- dat[uridx2,]
newdat$randomise_trials <- urRandTrials
newdat$block <- urBlockOrder
openxlsx::write.xlsx(paste0(basefilename,'_adcb.xlsx'),x = newdat)

newdat <- dat
newdat[uridx1,] <- dat[uridx3,]
newdat[uridx2,] <- dat[uridx4,]
newdat[uridx3,] <- dat[uridx1,]
newdat[uridx4,] <- dat[uridx2,]
newdat$randomise_trials <- urRandTrials
newdat$block <- urBlockOrder
openxlsx::write.xlsx(paste0(basefilename,'_cdab.xlsx'),x = newdat)


newdat <- dat
newdat[uridx1,] <- dat[uridx2,]
newdat[uridx2,] <- dat[uridx1,]
newdat[uridx3,] <- dat[uridx4,]
newdat[uridx4,] <- dat[uridx3,]
newdat$randomise_trials <- urRandTrials
newdat$block <- urBlockOrder
openxlsx::write.xlsx(paste0(basefilename,'_badc.xlsx'),x = newdat)


newdat <- dat
newdat[uridx1,] <- dat[uridx4,]
newdat[uridx2,] <- dat[uridx1,]
newdat[uridx3,] <- dat[uridx2,]
newdat[uridx4,] <- dat[uridx3,]
newdat$randomise_trials <- urRandTrials
newdat$block <- urBlockOrder
openxlsx::write.xlsx(paste0(basefilename,'_dabc.xlsx'),x = newdat)


newdat <- dat
newdat[uridx1,] <- dat[uridx2,]
newdat[uridx2,] <- dat[uridx3,]
newdat[uridx3,] <- dat[uridx4,]
newdat[uridx4,] <- dat[uridx1,]
newdat$randomise_trials <- urRandTrials
newdat$block <- urBlockOrder
openxlsx::write.xlsx(paste0(basefilename,'_bcda.xlsx'),x = newdat)


newdat <- dat
newdat[uridx1,] <- dat[uridx4,]
newdat[uridx2,] <- dat[uridx3,]
newdat[uridx3,] <- dat[uridx2,]
newdat[uridx4,] <- dat[uridx1,]
newdat$randomise_trials <- urRandTrials
newdat$block <- urBlockOrder
openxlsx::write.xlsx(paste0(basefilename,'_dcba.xlsx'),x = newdat)





