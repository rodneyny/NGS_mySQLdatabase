import mysql.connector as con
#import MySQLdb as con
import getpass

# use raw_input() instead of input()
#upass = raw_input('Password:')

userid = getpass.getuser()

upass = getpass.getpass('Password:')

print userid

db = con.connect(host = "localhost", \
				user = userid, \
				password = upass, \
				database = "VEPvariants" )

# db = con.connect("localhost", \
				# userid, \
				# upass, \
				# "VEPvariants" )
				
#prepare a cursor object using cursor() method
cursor = db.cursor()

sql = "select * from Genes"

cursor.execute(sql)
results = cursor.fetchall()

for row in results:
	print row 
	
db.close()
	