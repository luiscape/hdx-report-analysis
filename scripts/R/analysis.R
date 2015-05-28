#
# Script designed to answer the following questions:
#
# 1. The average number of organizations contributing datasets per week/month was __.
# 2. HDX holds operational data at sub-national level in __ of the countries where OCHA has an office or HAT; 
# 3. The median number of orgs contributing data per country was __.
#
# 
# Author: Luis Capelo | capelo@un.org
#

library(dplyr)
library(sqldf)

#
# Load data from a SQLite table into a data.frame
#
LoadAndTransform <- function(db='scraperwiki', table='') {

  #
  # Sanity check.
  #
  if(is.null(db) == TRUE) stop("Please provide a database name.")
  if(is.null(table) == TRUE) stop("Please provide the table name.")

  #
  # Create database and establish connection.
  #
  db_name <- paste0(db, ".sqlite")
  db <- dbConnect(SQLite(), dbname = db_name)


  #
  # Load data, check, and return.
  #
  loaded_data <- dbReadTable(db, table)
  if (is.data.frame(loaded_data)) {
    
    #
    # Transform dates and adding month.
    #
    if (table == 'package_activity_data') {
      loaded_data$timestamp <- as.Date(loaded_data$timestamp)
      loaded_data$month <- format(loaded_data$timestamp, "%B")
      loaded_data$year <- format(loaded_data$timestamp, "%Y")
    }
    if (table == 'organization_activity_data') {
      loaded_data$dataset_date_created <- as.Date(loaded_data$dataset_date_created)
    }
    return(loaded_data)
  }
  else print('Something went wrong loading data.')

}

#
# Calculate the average number of organizations 
# contributing datasets per week/month was __.
#
CalculateAverageContributingOrganization <- function(df=NULL, start_date=NULL, end_date=NULL) {
  
  #
  # Use dplyr to group and find data.
  #
  if (!is.null(end_date)) { data <- filter(df, timestamp < as.Date(end_date), timestamp > as.Date(start_date)) }
  else { data <- df }
  
  #
  # Perform analysis using dplyr.
  #
  analysis <- data %>%
              group_by(year) %>%
              group_by(month) %>%
              summarize(count = n_distinct(owner_org))
  #
  # Return.
  #
  return(analysis)
}


#
# Calculate median number of organizations
# contributing data per country.
#
CalculateMedianOrgsPerCountry <- function(df=NULL, start_date=NULL, end_date=NULL) {
  
  #
  # Use dplyr to group and find data.
  #
  if (!is.null(end_date)) { 
    data <- filter(df, 
                   dataset_date_created < as.Date(end_date), 
                   dataset_date_created > as.Date(start_date)) 
    }
  else { data <- df }
  
  #
  # Perform analysis using dplyr.
  #
  analysis <- data %>%
              group_by(country_id) %>%
              summarize(count = n_distinct(dataset_owner_org))
  
  #
  # Return
  # 
  return(analysis)
}

#
# Program wrapper.
#
Main <- function() {
  
  #
  # Loading data and making calculations.
  #
  package_activity_data = LoadAndTransform(table='package_activity_data')
  organization_activity_data = LoadAndTransform(table='organization_activity_data')
  orgs_contributing_per_month <- CalculateAverageContributingOrganization(df=package_activity_data, 
                                                                          start_date='2014-07-01', 
                                                                          end_date='2014-12-31')
  
  orgs_contributing_per_country <- CalculateMedianOrgsPerCountry(df=organization_activity_data,
                                                                 start_date='2014-07-01',
                                                                 end_date='2014-12-31')
  #
  # Printing answers to questions.
  #
  
  # Question 1
  average_orgs = round(mean(orgs_contributing_per_month$count))
  answer_1 = paste0("The average number of organizations contributing datasets per month was ", average_orgs,".")
  print(answer_1)
  
  # Question 2
  
  
  # Question 3
  average_contributions = round(median(filter(orgs_contributing_per_country, count > 3)$count))
  answer_3 = paste0("The median number of orgs contributing data per country was ", average_contributions,".")
  print(answer_3)
  
}


Main()
