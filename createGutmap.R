# Create Gutmap: This script will read in gut microbiome data from pubmed 
# (created with script) download_pubmed.py, and create a map.
# Vsochat April 2014
# Property of Wall Lab

library(RJSONIO)
library(RCurl)
options(RCurlOptions = list(cainfo = system.file("CurlSSL", "cacert.pem", package = "RCurl")))

setwd('/home/vanessa/Documents/Dropbox/Code/Python/gutmap')

# Load in the data file
raw = read.table('gutmap.tab',sep="\t",head=TRUE)

# Set API key (must be generated when time to run!)
API = "#"

# For each unique location, use Google API to look up
loc = unique(raw$country)

# We will save a list of latitudes and longitudes
lat = c()
long = c()
place = c()
formatted = c()

# Format our query string to get json result
query = "http://maps.googleapis.com/maps/api/geocode/json?"
query = "https://maps.googleapis.com/maps/api/geocode/json?"

for (l in 1:length(loc)){
  location = as.character(loc[l])
  # If we have a location
  if !(location %in% "None") {
    # Get rid of colons
    location = sub(":","",location)
    location = strsplit(location," ")
    location = cat(location[[1]],sep="+")
    q = paste(query,"address=","USA+Chicago,+IL","&sensor=false&key=",API,sep="")
    result = getURL(q)
    data = fromJSON(result)
    if (data$status %in% "OK") {
      place = c(place,loc[l])
      lat = c(lat,)
      long = c(long,)
      formatted = c(formatted,data$results[[1]]$formatted_address)
      lat = c(lat,as.numeric(data$results[[1]]$geometry$location[1]))
      long = c(long,as.numeric(data$results[[1]]$geometry$location[1]))
    }  
  } 
}

# TODO Filter results to only human relevant gut microbiome (use organism)

# Add a row on for latitude and longitude and count
toappend = list(lat=array(dim=dim(raw)[1]), long=array(dim=dim(raw)[1]), count=array(dim=dim(raw)[1]))
raw = cbind(raw,toappend)

# Now, for each record, add the latitude and longitude.  We may also need
# to aggregate results by common location and species, and then make a count 
# variable to indicate intensity on the heatmap
for (r in 1:dim(raw)[1]){
  idx = which(place %in% raw$country[r])
  raw$lat[r] = lat[idx]
  raw$long[r] = long[idx]
}

# Now we can make a map in R, or export data to make with Google Tables