# descripts
library("Rmisc")
library(ggplot2)
# external script for flatviolins
source('V:/gfraga/scripts_neulin/Misc/geom_flat_violin.R')

# Read and preprocess
#-------------------------------------------------------------------------------------
df <- read.csv('C:/Users/gfraga/Downloads/SelectiveVoxelCounts.csv')
df_long <- tidyr::pivot_longer(df,colnames(df)[3:6],names_to = c('hemisphere','type'),names_sep = '_')
df_long$group <- ''
df_long$group[which(df_long$WordReading<=2)] <- 'poor'
df_long$group[which((df_long$WordReading>2)  & (df_long$WordReading<29)) ] <- 'mid'
df_long$group[which(df_long$WordReading>29)] <- 'good'
# factors?
df_long$group <- as.factor(df_long$group)
df_long$hemisphere <- as.factor(df_long$hemisphere)
df_long$type <- as.factor(df_long$type)


# make a plot for each 'Type' 
types = unique(df_long$type)
for (t in 1:length(types)){
      
      # filter
      d2plot <-  filter(df_long,type==types[t])
      #describe
      ds <- Rmisc::summarySE(d2plot,measurevar="value",groupvars = c("hemisphere","type","group")) 
      
      # some parameters for plotting  
      pd <- position_dodge(0.08) 
      
      #da plot 
      plot1 <- 
        ggplot(d2plot, aes(x=group, y = value,fill=group )) +
      geom_hline(yintercept=0,color = "black",linetype="dashed", size=.1,alpha=.8) +
      geom_flat_violin(aes(x=group),position = position_nudge(x = 0.04, y = 0), adjust = .9, trim = TRUE, alpha = .3)+
      geom_point(aes(x = as.numeric(group)-.13, y = value),shape=21, color="black",position=position_jitter(.05,0,4), size = 3, alpha=.5)+
      geom_boxplot(aes(x=as.numeric(group)-.2),width = .05, color="black",outlier.shape = NA, alpha = 0.1)  + 
      facet_grid(~hemisphere) +
      geom_errorbar(data=ds,aes(x= as.numeric(group)+.09, ymin=value-ci, ymax=value+ci),width=.05, size= 1, position=pd)  +
      geom_point(data=ds,aes(x= as.numeric(group)+.09,y = value),size=4,color="black",pch=21,alpha=1) +
      theme_bw() +
      #theme_classic() + # this has a cleaner style
      labs(x="Condition",title ='mytitle' , subtitle = 'mysubtitle',caption ="mycaption")+
      theme(axis.line.y = element_line(color = gray.colors(10)[3], size = 1, linetype = "solid"),
            axis.line.x = element_line(color = gray.colors(10)[3], size = 1, linetype = "solid"),
            axis.text.x = element_text(size=12,color="black"),
            axis.text.y = element_text(size=12,color="black"),
            axis.title.x = element_text(size=12,color="black"),
            axis.title.y = element_text(size=14,color="black"))
       
       print(plot1)
      #  SAVE 
       ggsave(paste0('RAINCLOUD_',types[t],'.jpg'),plot1,width = 150, height = 170, dpi=300, units = "mm")    
       
}
      






















 
