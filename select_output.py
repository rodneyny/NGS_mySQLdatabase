import csv
import sys
from fromFile import openfile
from connection import connect 

sql = openfile(sys.argv[1])

database = connect()
cursor = database[0]
db = database[1]

f = open('variants2.txt','w')
c = csv.writer(f, delimiter ='\t')

# Take an SQL statement as the first argument.


try:
	# Execute the SQL command
	cursor.execute(sql)
	# Fetch all the rows in a list of lists.
	results = cursor.fetchall()
	desc = cursor.description

   # Create a header based on the description values of each column
   # Use index [0] from the description
	header = []
	for line in desc:
		header.append(line[0])
	c.writerow(header)
	
	for row in results:
		c.writerow(row)
	print "Finished!"

except:
   print "Error: unable to fetch data"

db.close()