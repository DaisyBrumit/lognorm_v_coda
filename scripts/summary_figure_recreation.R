library(tidyverse)

## SET GLOBAL VARS THAT WILL NEED TO BE LOOPED
# set working dirctory from files tab as necessary to follow expected dir layout
study.list <- c('Jones', 'Vangay', 'Zeller', 'Noguera-Julian')
metric.list <- c('RF_accuracy', 'RF_r2', 'multinomial_accuracy')

## DEFINE CORE FUNCTIONS

# df_filter: remove nonsense output from incoming tables
df_filter <- function(df) {
  df.nas <- df %>% mutate(across(everything(), ~ifelse(.x == 999, NA, .x))) # turn all 999 into na
  df.filtered <- df.nas %>% select_if(~ !any(is.na(.))) # remove whole column if all labels are na
  return(df.filtered)
}
## 
for (metric in metric.list) {
  for (study in study.list) {
    data.raw <- readr::read_tsv(paste0(study,'/',metric,'.txt')) # import data "as is"
    data <- df_filter(data.raw) # filter out cols that didn't make ml requirements
  }
} 
