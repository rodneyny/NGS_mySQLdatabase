#!/usr/bin/python

# import MySQLdb
import mysql.connector as dbm

db = dbm.connect(host = "10.101.84.24", \
      port = 3306, \
      user = 'rodney', \
      password = 'munetsi' , \
      database = "VEPvariants" )

# Open database connection
# db = MySQLdb.connect("localhost","rodney","password","variants" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

# Prepare SQL query to INSERT a record into the database.
sql = "select * from Genes where Gene =%s" 
value = 'LDLR'

print sql
# Execute the SQL command
cursor.execute(sql, [value])
# Fetch all the rows in a list of lists.
results = cursor.fetchall()
for row in results:
   Gene = row[0]
   Chromosome = row[1]
   Disease = row[2]
   # Now print fetched result
   print "Gene=%s,Chromosome=%s,Disease=%s" % \
          (Gene, Chromosome, Disease )

# disconnect from server
db.close()