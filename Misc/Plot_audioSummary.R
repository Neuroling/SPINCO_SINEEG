rm(list=ls())
library('raincloudplots')
library('ggdist')
library('ggplot2')
#dir 
dirinput <- 'V:/spinco_data/SINON/Spreadsheets/LexicalDecision/'
diroutput <- 'V:/spinco_data/SINON/Spreadsheets/LexicalDecision/'

# read file with info 
setwd(dirinput)
tab <- openxlsx::read.xlsx("audio_info.xlsx") 
head(tab)


foldername <- strsplit(dirinput,'/')[[1]][[length(strsplit(dirinput,'/')[[1]])]]

variables <- c('duration', 'rms')

for (i in 1:length(variables)){
  
    var2plot <- variables[i]
    rain <- ggplot(tab, aes_string(x = 'block' , y = var2plot, fill='block')) + 
      ## add half-violin from {ggdist} package
      ggdist::stat_halfeye(
        alpha=.4,
        adjust = .5, 
        width = .6, 
        ## move geom to the right
        justification = -.5, 
        point_colour = 'black'
      ) + 
      geom_boxplot(
        width = .12, 
        outlier.shape = 3,
        outlier.size = 2
      ) +
      gghalves::geom_half_point(
        side = "l", 
        range_scale = .4, 
        alpha = .3,
        shape=21
      ) +
      theme_bw()+ 
      facet_grid(~type)+
      ggtitle(paste0(foldername, ' (', var2plot,')'))
    
    
    histo<- ggplot(tab, aes_string(x = var2plot, fill='block')) + 
      geom_histogram(aes(y=..density..), colour='black',alpha=.7)+
      geom_density(alpha=.3, fill="#FF6666") +
      facet_grid(~type*block) + theme_bw() +
      ggtitle(paste0(foldername, ' (', var2plot,')'))
    
    
   combo <- gridExtra::arrangeGrob(rain,histo)  
  ggplot2::ggsave(plot = combo, filename = paste0(diroutput,'plot_',var2plot,'.jpg'),height=1750, width = 2500,units='px',dpi=150)
  dev.off()
}
