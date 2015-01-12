import MySQLdb as dbm
import getpass

def connect():
	# fetches username of person logged into the system
	# this username must match the username in the mysql user table 
	userid = getpass.getuser()
	
	# mysql password for user 
	upass = getpass.getpass('Please enter your password: ')

	# Open database connection
	data = dbm.connect("localhost", userid, upass,"VEPvariants" )

	# prepare a cursor object using cursor() method
	cur = data.cursor()
	
	return cur, data