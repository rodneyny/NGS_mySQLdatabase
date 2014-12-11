#!/usr/bin/python

import MySQLdb

# Open database connection
db = MySQLdb.connect("localhost","rodney","password","variants" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

# Prepare SQL query to INSERT a record into the database.
sql = "insert into genes(Gene, Chromosome,Disease)\
         values ('%s', '%d', '%s')" % \
		 ('ALMS1', 2, 'BBS')
try:
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