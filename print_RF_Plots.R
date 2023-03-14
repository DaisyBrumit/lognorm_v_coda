# 100 iteration RF plots
# Aaron Yerke test code via yerkeTest.py

library(tidyverse)

# set list of author names for input paths & identifiers
study <- c('Jones', 'Zeller', 'Noguera-Julian', 'Vangay')

# name procedures
proc <- c('alr', 'clr', 'ilr', 'log')

# run full process to generate figures by study
for (name in study) {
  # read in all Random Forest output files
  alr <- read_csv(paste0(name,"_",proc[1],'_RF_Results_100run.csv'))
  clr <- read_csv(paste0(name,"_",proc[2],'_RF_Results_100run.csv'))
  ilr <- read_csv(paste0(name,"_",proc[3],'_RF_Results_100run.csv'))
  log <- read_csv(paste0(name,"_",proc[4],'_RF_Results_100run.csv'))
  
  # combine all outputs to one list with transformtion IDs for easier plotting
  alr[['trans']] <- 'alr'
  clr[['trans']] <- 'clr'
  ilr[['trans']] <- 'ilr'
  log[['trans']] <- 'lognorm'
  full_table <- rbind(alr,clr,ilr,log) %>% select(-'...1')
  long_table <- pivot_longer(full_table, cols=1:ncol(full_table)-1, names_to = 'metaCol', values_to = 'metaValues')
  
  # generate and save a suite of ggplot objects
  pdf(paste0('plots/',name,'_catBoxplots.pdf'))
  plt <- ggplot(long_table, aes(x=metaCol, y=metaValues, fill=trans)) +
    geom_boxplot() +
    theme(axis.text.x = element_text(angle = 90))
  print(plt)
  dev.off()
  #ggsave(paste0('~/plots',name,'_catBoxplots.pdf', plt))
}

for (name in study) {
  # read in all Random Forest output files
  alr <- read_csv(paste0(name,"_",proc[1],'_RFquant_Results_100run.csv'))
  clr <- read_csv(paste0(name,"_",proc[2],'_RFquant_Results_100run.csv'))
  ilr <- read_csv(paste0(name,"_",proc[3],'_RFquant_Results_100run.csv'))
  log <- read_csv(paste0(name,"_",proc[4],'_RFquant_Results_100run.csv'))
  
  # combine all outputs to one list with transformtion IDs for easier plotting
  alr[['trans']] <- 'alr'
  clr[['trans']] <- 'clr'
  ilr[['trans']] <- 'ilr'
  log[['trans']] <- 'lognorm'
  full_table <- rbind(alr,clr,ilr,log) %>% select(-'...1')
  long_table <- pivot_longer(full_table, cols=1:ncol(full_table)-1, names_to = 'metaCol', values_to = 'metaValues')
  
  # generate and save a suite of ggplot objects
  pdf(paste0('plots/',name,'_quantBoxplots.pdf'))
  plt <- ggplot(long_table, aes(x=metaCol, y=metaValues, fill=trans)) +
    geom_boxplot() +
    theme(axis.text.x = element_text(angle = 90))
  print(plt)
  dev.off()
  #ggsave(paste0('~/plots',name,'_catBoxplots.pdf', plt))
}