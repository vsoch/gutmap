#!/bin/python

# This script will read in a list of genbank IDs, and download locations from pubmed.  The file (genback_ids.txt) should be a single column of genbank ids.
# PROPERTY OF WALL LAB, NOT FOR PUBLIC USE

# Example page
# "http://www.ncbi.nlm.nih.gov/nuccore/FR851252.1"

from Bio import Entrez
import time

# Entrez needs to know your email
email = 'vsochat@stanford.edu'

# Authenticate Entrez
Entrez.email = email

# We need to search nuccore for "gut metagenome" to get our ids
handle = Entrez.esearch(db='nuccore',term="gut+metagenome",retmax=10000000)
record = Entrez.read(handle)
ids = record['IdList']

# Here are the fields we will keep
fields = ['Id','GBSeq_moltype','GBSeq_source','GBSeq_primary-accession','GBSeq_definition','GBSeq_topology','GBSeq_length','organism','organelle','mol_type','isolation_source','host','db_xref','clone','environmental_sample','country','metagenomic','GBSeq_taxonomy','GBReference_title','GBSeq_organism','GBSeq_locus']

data = []
count = 1
# For each ID, obtain the record
for id in ids:
  # Tell the user our progress
  print "Parsing " + str(count) ": " + str(id) + " of " + str(len(ids)) 
  # Pause for one second
  time.sleep(1)
  handle = Entrez.esearch(db='nuccore',term=id)
  record = Entrez.read(handle)
  if "IdList" in record:
    tmp = ["None"] * len(fields)  # List to hold all fields for this ID
    theid = record['IdList'][0]
    # Now fetch the paper!
    handle = Entrez.efetch(db="nuccore", id=theid, rettype="gb", retmode="xml")
    record = Entrez.read(handle)
    # Now construct the field 
    tmp[0] = theid
    tmp[1] = record[0]['GBSeq_moltype']
    tmp[2] = record[0]['GBSeq_source']
    tmp[3] = record[0]['GBSeq_primary-accession']
    tmp[4] = record[0]['GBSeq_definition']
    tmp[5] = record[0]['GBSeq_topology']
    tmp[6] = record[0]['GBSeq_length']
    # Here are features from the table (strings)
    for feat in range(0,len(record[0]['GBSeq_feature-table'][0]['GBFeature_quals'])):
      if record[0]['GBSeq_feature-table'][0]['GBFeature_quals'][feat]['GBQualifier_name'] == 'organism':
        if 'GBQualifier_value' in record[0]['GBSeq_feature-table'][0]['GBFeature_quals'][feat]:
          tmp[7] = record[0]['GBSeq_feature-table'][0]['GBFeature_quals'][feat]['GBQualifier_value']
      elif record[0]['GBSeq_feature-table'][0]['GBFeature_quals'][feat]['GBQualifier_name'] == 'organelle':
        if 'GBQualifier_value' in record[0]['GBSeq_feature-table'][0]['GBFeature_quals'][feat]:
          tmp[8] = record[0]['GBSeq_feature-table'][0]['GBFeature_quals'][feat]['GBQualifier_value']
      elif record[0]['GBSeq_feature-table'][0]['GBFeature_quals'][feat]['GBQualifier_name'] == 'mol_type':
        if 'GBQualifier_value' in record[0]['GBSeq_feature-table'][0]['GBFeature_quals'][feat]:    
          tmp[9] = record[0]['GBSeq_feature-table'][0]['GBFeature_quals'][feat]['GBQualifier_value']
      elif record[0]['GBSeq_feature-table'][0]['GBFeature_quals'][feat]['GBQualifier_name'] == 'isolation_source':
        if 'GBQualifier_value' in record[0]['GBSeq_feature-table'][0]['GBFeature_quals'][feat]:    
          tmp[10] = record[0]['GBSeq_feature-table'][0]['GBFeature_quals'][feat]['GBQualifier_value']
      elif record[0]['GBSeq_feature-table'][0]['GBFeature_quals'][feat]['GBQualifier_name'] == 'host':
        if 'GBQualifier_value' in record[0]['GBSeq_feature-table'][0]['GBFeature_quals'][feat]:    
          tmp[11] = record[0]['GBSeq_feature-table'][0]['GBFeature_quals'][feat]['GBQualifier_value']
      elif record[0]['GBSeq_feature-table'][0]['GBFeature_quals'][feat]['GBQualifier_name'] == 'db_xref':
        if 'GBQualifier_value' in record[0]['GBSeq_feature-table'][0]['GBFeature_quals'][feat]:    
          tmp[12] = record[0]['GBSeq_feature-table'][0]['GBFeature_quals'][feat]['GBQualifier_value']
      elif record[0]['GBSeq_feature-table'][0]['GBFeature_quals'][feat]['GBQualifier_name'] == 'clone':
        if 'GBQualifier_value' in record[0]['GBSeq_feature-table'][0]['GBFeature_quals'][feat]:    
          tmp[13] = record[0]['GBSeq_feature-table'][0]['GBFeature_quals'][feat]['GBQualifier_value']
      elif record[0]['GBSeq_feature-table'][0]['GBFeature_quals'][feat]['GBQualifier_name'] == 'environmental_sample':
        if 'GBQualifier_value' in record[0]['GBSeq_feature-table'][0]['GBFeature_quals'][feat]:    
          tmp[14] = record[0]['GBSeq_feature-table'][0]['GBFeature_quals'][feat]['GBQualifier_value']
      elif record[0]['GBSeq_feature-table'][0]['GBFeature_quals'][feat]['GBQualifier_name'] == 'country':
        if 'GBQualifier_value' in record[0]['GBSeq_feature-table'][0]['GBFeature_quals'][feat]:    
          tmp[15] = record[0]['GBSeq_feature-table'][0]['GBFeature_quals'][feat]['GBQualifier_value']
      elif record[0]['GBSeq_feature-table'][0]['GBFeature_quals'][feat]['GBQualifier_name'] == 'metagenomic':
        if 'GBQualifier_value' in record[0]['GBSeq_feature-table'][0]['GBFeature_quals'][feat]:    
          tmp[16] = record[0]['GBSeq_feature-table'][0]['GBFeature_quals'][feat]['GBQualifier_value']
    tmp[17] = record[0]['GBSeq_taxonomy']
    tmp[18] = record[0]['GBSeq_references'][0]['GBReference_title']
    tmp[19] = record[0]['GBSeq_organism']
    tmp[20] = record[0]['GBSeq_locus']
    data.append(tmp)
    count = count + 1

# Save to text file
filey = open('/scratch/users/vsochat/DATA/GUTMAP/gutmap.tab','w')
filey.writelines("\t".join(fields) + "\n")
for d in data:
  filey.writelines("\t".join(d) + "\n")

filey.close()


