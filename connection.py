import mysql.connector as dbm
import getpass

def connect():
	# fetches username of person logged into the system
	# this username must match the username in the mysql user table 
	userid = getpass.getuser()
	#userid = raw_input('username: ')
	
	# mysql password for user 
	upass = getpass.getpass('Please enter your password: ')

	# Open database connection
	# MySQLdb connection 
	#data = dbm.connect("localhost", userid, upass,"VEPvariants" )
	
	#MySQL connector connection 
	data = dbm.connect(host = "10.101.84.24", \
				port = 3306, \
				user = userid , \
				password = upass , \
				database = "VEPvariants" )

	# prepare a cursor object using cursor() method
	cur = data.cursor()
	
	return cur, data

def closecon():
	db = connect()[1]
	db.close()