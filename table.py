#!/usr/bin/python

import MySQLdb

# Open database connection
db = MySQLdb.connect("localhost","rodney","password","variants" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

# Drop table if it already exist using execute() method.
cursor.execute("DROP TABLE IF EXISTS genes")

# Create table as per requirement
sql = """create table genes (
		Gene char(20) not null,
		Chromosome int,
		Disease char(20),
		primary key(Gene)
          )"""

cursor.execute(sql)

# disconnect from server
db.close()