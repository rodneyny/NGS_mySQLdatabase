#!/usr/bin/python

import MySQLdb as dbm
import sys 

g = open('Genes.txt','r')
c = open('Classes.txt', 'r')
d = open('Diseases.txt', 'r')
t = open('Transcripts.txt', 'r')

#Create an empty list to insert values
genes = []
for row in g:
	row = row.strip().split('\t')
	#Append each row from the file into the genes list
	genes.append(row)

classes = []
for row in c:
	row = row.strip().split('\t')
	classes.append(row)
	
diseases = []
for row in d:
	row = row.strip().split('\t')
	diseases.append(row)

transcripts = []
for row in t:
	row = row.strip().split('\t')
	transcripts.append(row)

# Open database connection
db = dbm.connect("localhost","rodney","password","variants" )

# # prepare a cursor object using cursor() method
cursor = db.cursor()

# Prepare SQL query to INSERT a record into the database.

try:
	for line in genes:
		gene = line[0]
		chr = line[1]
		dis = line[2]
		sql = "insert into Genes(Gene, Chromosome,Disease)\
         values ('%s', '%s', '%s')" % \
		 (gene, chr, dis)
	   # Execute the SQL command
		cursor.execute(sql)
	   # Commit your changes in the database
		db.commit()
	print "Rows in the Genes table were populated"	
except:
	print "An error occurred"
	# Rollback in case there is any error
	db.rollback()
	
try:
	for line in classes:
		classification = line[0]
		description = line[1]
		cursor.execute("insert into Classes(Classification, Description)\
         values ('%s','%s')" % \
		 (classification, description))
		 
		db.commit()
	print "Rows in the Classes table were populated"
except:
	print "An error occurred inserting Classes"
	db.rollback()
	
try:
	for line in diseases:
		disease = line[0]
		code = line[1]
		cursor.execute("insert into Diseases(Disease,code)\
         values ('%s','%s')" % \
		 (disease, code))
		db.commit()
	print "Rows in the Diseases table were populated"
except:
	print "No diseases were added to the Diseases table"
	db.rollback()
	
try:
	for line in transcripts:
		refseq = line[0]
		ensembl = line[1]
		gene = line[2]
		cursor.execute("insert into Transcripts(Refseq, Ensembl,Gene)\
         values ('%s', '%s', '%s')" % \
		 (refseq, ensembl, gene))
		db.commit()
	print "Rows in the Transcripts table have been populated"
except:
	print "No Transcripts were added to the Transcripts table"
	db.rollback()
	
# disconnect from server
db.close()