#!/usr/bin/python

import MySQLdb as dbm
import sys 

f = open('Genes.txt','r')
genes = []
for row in f:
	row = row.strip().split('\t')
	genes.append(row)

genes.remove(genes[0])

# Open database connection
db = dbm.connect("localhost","rodney","password","variants" )

# # prepare a cursor object using cursor() method
cursor = db.cursor()

# # Prepare SQL query to INSERT a record into the database.

try:
	for line in genes:
		gene = line[0]
		chr = int(line[1])
		dis = line[2]
		sql = "insert into genes(Gene, Chromosome,Disease)\
         values ('%s', '%d', '%s')" % \
		 (gene, chr, dis)
	   # Execute the SQL command
		cursor.execute(sql)
	   # Commit your changes in the database
		db.commit()
except:
	print "an error occured"
	# Rollback in case there is any error
	db.rollback()

# disconnect from server
db.close()