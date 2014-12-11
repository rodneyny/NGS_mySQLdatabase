#!/usr/bin/python

import MySQLdb

# Open database connection
db = MySQLdb.connect("localhost","rodney","password","variants" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

# Prepare SQL query to INSERT a record into the database.
sql = "select * from genes" 

try:
   # Execute the SQL command
   cursor.execute(sql)
   # Fetch all the rows in a list of lists.
   results = cursor.fetchall()
   for row in results:
      Gene = row[0]
      Chromosome = row[1]
      Disease = row[2]
      # Now print fetched result
      print "Gene=%s,Chromosome=%d,Disease=%s" % \
             (Gene, Chromosome, Disease )
except:
   print "Error: unable to fecth data"

# disconnect from server
db.close()