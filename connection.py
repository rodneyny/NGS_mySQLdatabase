import MySQLdb as dbm

def connect():
	# Open database connection
	db = MySQLdb.connect("localhost","rodney","password","VEPvariants" )

	# prepare a cursor object using cursor() method
	cursor = db.cursor()
