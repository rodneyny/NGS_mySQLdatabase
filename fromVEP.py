#!/usr/bin/python

import MySQLdb as dbm
import sys 
from fromFile import filelist

#file = os.path.abspath(sys.argv[1])

record = filelist('vep.txt','record')

# Remove the header from the dictionary
record.remove(record[0])

# Open database connection
db = dbm.connect("localhost","rodney","password","variants" )

# # prepare a cursor object using cursor() method
cursor = db.cursor()

# Prepare SQL query to INSERT a record into the database.

try:
	for line in record:
		PK = line[0]
		refseq = line[1]
		hgvsnomen = line[2]
		sample = line[3]
		gt = line[4]
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
		# For floats use the % placeholder instead of the %d placeholder
		cursor.execute("insert ignore into Variants (cDNA, Refseq, \
		      HGVSNomen, Effect, dbSNP, MAF, ESP_AA, ESP_EA, SIFT, SIFTweight, \
		      Polyphen, PolyphenScore, Protein, ProteinDomain ) \
              values ('%s', '%s', '%s', '%s', '%s', '%f', '%f', '%f', '%s', '%f', \
			  '%s', '%f', '%s', '%s')"% \
		      (PK, refseq, hgvsnomen, effect, dbsnp, maf, espaa, \
			  espea, sift, siftscore, polyphen, polyphenscore, protein, proteindom ))
		cursor.execute("insert ignore into Episodes ( EpisodeNumber)\
					  values ('%s')" % (sample))
		cursor.execute("insert into Occurrence (EpisodeNumber, cDNA, Genotype) \
					   values ('%s', '%s', '%s')" % (sample, PK, gt))
	   # Commit your changes in the database 
		db.commit()
	print "records successfully added to database"
except:
	print "an error occured"
	# Rollback in case there is any error
	db.rollback()




# disconnect from server
db.close()