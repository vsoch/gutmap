# Create Gutmap: This script will read in gut microbiome data from pubmed 
# (created with script) download_pubmed.py, and create a map.
# Vsochat April 2014
# Property of Wall Lab

library(RJSONIO)
library(RCurl)
options(RCurlOptions = list(cainfo = system.file("CurlSSL", "cacert.pem", package = "RCurl")))

setwd('/home/vanessa/Documents/Dropbox/Code/Python/gutmap')

# Load in the data file
raw = read.table('gutmap52704.tab',sep="\t",head=FALSE)
raw[,16] = as.character(raw[,16])

# Set API key (must be generated when time to run!)
API = "APIKEYHERE"

# For each unique location, use Google API to look up
loc = unique(raw[,16])
loc = loc[-which(loc=="None")]

# We will save a list of latitudes and longitudes
lat = c()
long = c()
place = c()
formatted = c()
place = c()

# Format our query string to get json result
query = "https://maps.googleapis.com/maps/api/geocode/json?"

for (l in 1:length(loc)){
  location = as.character(loc[l])
  # If we have a location
  if (!(location %in% "None")) {
    # Get rid of colons
    location = sub(":","",location)
    location = strsplit(location," ")
    location = paste(location[[1]], collapse="+")
    q = paste(query,"address=",location,"&sensor=false&key=",API,sep="")
    result = getURL(q)
    data = fromJSON(result)
    if (data$status %in% "OK") {
      place = c(place,as.character(loc[l]))
      formatted = c(formatted,data$results[[1]]$formatted_address)
      lat = c(lat,as.numeric(data$results[[1]]$geometry$location[1]))
      long = c(long,as.numeric(data$results[[1]]$geometry$location[2]))
    }  
  } 
}

# Now filter results to those we have locations for
filtered = raw[which(raw[,16] != "None"),]

# Filter resuls to human
filtered = filtered[which(filtered$V20 == "human gut metagenome"),]

# Make a data frame to hold latitude, longitude, and places
locs = array(dim=c(dim(filtered)[1],4))
colnames(locs) = c("lat","long","formal_location","lat.long")
locs = as.data.frame(locs)

# Look up latitude, longitude, and formal location for each
for (r in 1:length(place)){
  locs$lat[which(filtered[,16] %in% place[r])] = lat[r]
  locs$long[which(filtered[,16] %in% place[r])] = long[r]
  locs$formal_location[which(filtered[,16] %in% place[r])] = formatted[r]
  locs$lat.long[which(filtered[,16] %in% place[r])] = paste(lat[r],long[r],sep=":")
}

# Append to our data
data = cbind(filtered,locs)


# Save to file
colnames(data) = c('Id','GBSeq_moltype','GBSeq_source','GBSeq_primary-accession','GBSeq_definition','GBSeq_topology','GBSeq_length','organism','organelle','mol_type','isolation_source','host','db_xref','clone','environmental_sample','country','metagenomic','GBSeq_taxonomy','GBReference_title','GBSeq_organism','GBSeq_locus',"lat","long","formal_location","lat.long")
write.table(data,file="/home/vanessa/Desktop/gmboime52704.csv",sep="\t")

# Now we can make a map in R, or export data to make with Google Tables
# http://www.r-bloggers.com/heatmap-of-toronto-traffic-signals-using-rgooglemaps/
