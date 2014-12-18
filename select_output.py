import MySQLdb as dbm
import csv
import sys
 
data = sys.argv[1]
sql = sys.argv[2]

db = dbm.connect("localhost","rodney","password",data )

cursor = db.cursor()

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
	print header

	c.writerow(header)
	for row in results:
		c.writerow(row)
		print row

except:
   print "Error: unable to fetch data"
   

db.close()