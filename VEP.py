#!/usr/bin/python

import MySQLdb as dbm
import sys 
from file import filelist

#file = os.path.abspath(sys.argv[1])

record = filelist('vep.txt','record')

# Remove the header from the dictionary
record.remove(record[0])

# Open database connection
db = dbm.connect("localhost","rodney","password","variants" )

# # prepare a cursor object using cursor() method
cursor = db.cursor()

# Prepare SQL query to INSERT a record into the database.


for line in record:
	PK = line[0]
	refseq = line[1]
	hgvsnomen = line[2]
	effect = line[32]
	dbsnp = line[38]
	maf = float(line[62])
	espaa = float(line[39])
	espea = float(line[40])
	sift = line[57]
	siftscore = float(line[58])
	polyphen = line[59]
	polyphenscore = float(line[60])
	protein = line[66]
	proteindom = line[50]
	
	cursor.execute("insert ignore into Variants (cDNA, Refseq, \
		  HGVSNomen, Effect, dbSNP, MAF, ESP_AA, ESP_EA, SIFT, SIFTweight, \
		  Polyphen, PolyphenScore, Protein, ProteinDomain) \
		  values ('%s', '%s', '%s', '%s', '%s', '%d', '%d', '%d', '%s', '%d' \
		  '%s', '%d', '%s', '%s')" % \
		  (PK, refseq, hgvsnomen, effect, dbsnp, maf, espaa \
		  , espea, sift, siftscore, polyphen, polyphenscore \
		  , protein, proteindom))
   # Commit your changes in the database
	db.commit()
print "records successfully added to database"


# disconnect from server
db.close()