'''
Created on 14 Jan 2015

@author: nyanhr
'''
from Tkinter import *
import ttk 
import mysql.connector as dbm


""" """

def access(*args):
	#print "Hiya!!!"
	""" This function allows the user to connect to the databse with their username
	and password. """
	# Global variables for the database connection and the cursor 
	global db
	global cur

	user = str(username.get())
	passw = str(password.get())

	#MySQL connector connection 
	db = dbm.connect(host = "10.101.84.24", \
				port = 3306, \
				user = user , \
				password = passw , \
				database = "VEPvariants" )


	# prepare a cursor object using cursor() method
	cur = db.cursor()
	
	username_entry.destroy()
	username_lab.destroy()
	password_lab.destroy()
	password_entry.destroy()
	login_but.destroy()


def exit(*args):
	""" """
	try:
		cur.close()
		db.close()
		root.destroy()
	except:
		root.destroy()

def frequency_query():
	""" """
	# cur.execute("select cDNA ,count(SampleNumber)as EpisodeCount \
	# 					from Occurrence \
	# 					group by cDNA")	

	cur.execute("select * \
							from Genes")
							
	samcount = cur.fetchall()

	# for line in samcount:
	# 	cdna = line[0]
	# 	count = line[1]
	desc = cur.description

#Create a header based on the description values of each column
#Use index [0] from the description
	header = []
	for line in desc:
		header.append(line[0])
	header1 = '|'.join(header) + "\n"
	tb.insert(INSERT, header1)

	for row in samcount:
		row = ' '.join(row)
		row1 =row + "\n"
		tb.insert(INSERT, row1)


# def select_query():
	# """ This query will output data from the database when a specific
	# variant, sample, gene or transcript is searched for"""
	# sql = "select * from  where "
	
	# cur.execute(sql)
	##Fetch all the rows in a list of lists.
	# results = cur.fetchall()


#def insert_query():
# """ """

# def pipeline_query():	
# """ """

# root is the activity window    
root = Tk()
root.geometry("800x800" )
root.title("MOlGEN NGS VARIANTS")

""" Visualisation frame for any searches"""
queryframe = ttk.Frame(root, relief=SUNKEN, height=500)
queryframe.grid(column=3, row=1, columnspan=6, rowspan=8)
queryframe.columnconfigure(0, weight=1)
queryframe.rowconfigure(0, weight=1)
tb = Text(queryframe)
sb1 = Scrollbar(tb, orient=VERTICAL)
sb2 = Scrollbar(tb, orient=HORIZONTAL)
tb.configure(yscrollcommand=sb1.set)
tb.configure(xscrollcommand=sb2.set)
#yscrollcommand=sb1.set, xscrollcommand=sb2.set )
sb1.config(command=tb.yview)
sb2.config(command=tb.xview)
tb.grid(column= 1, row=4, columnspan=6,rowspan=6, sticky=(N, W, E, S) )
tb.columnconfigure(0, weight=1)
tb.rowconfigure(0, weight=1)
#tb.pack(side=LEFT, fill=BOTH, expand=1)
sb1.grid(column=6, row=1, sticky=(E, S))
sb2.grid(column=1, row=6, sticky=(E,S))

queryframe.columnconfigure(0, weight=1)
queryframe.rowconfigure(0, weight=1)

variant = StringVar()
sample = StringVar()
gene = StringVar()
transcript = StringVar()

variant_entry = ttk.Entry(queryframe, width=20, textvariable=variant)
sample_entry = ttk.Entry(queryframe, width=20, textvariable=sample)
gene_entry = ttk.Entry(queryframe, width=20, textvariable=gene)
transcript_entry = ttk.Entry(queryframe, width=20, textvariable=transcript)

variant_entry.grid(column=1, row=2, sticky=(W, E))
sample_entry.grid(column=2, row=2, sticky=(W, E))
gene_entry.grid(column=3, row=2, sticky=(W, E))
transcript_entry.grid(column=4, row=2, sticky=(W, E))

variant_lab = ttk.Label(queryframe, text="Variant")
variant_lab.grid(column=1, row=1, sticky=W)
sample_lab = ttk.Label(queryframe, text="Sample")
sample_lab.grid(column=2, row=1, sticky=W)
gene_lab = ttk.Label(queryframe, text="Gene")
gene_lab.grid(column=3, row=1, sticky=W)
transcript_lab = ttk.Label(queryframe, text="Refseq Transcript")
transcript_lab.grid(column=4, row=1, sticky=W)

select_but = ttk.Button(queryframe, text="Search", command=frequency_query)
select_but.grid(column=5, row=2)

""" Login frame for application """
loginframe = ttk.Frame(root)
loginframe.grid(column=1, row=1, columnspan=2,rowspan=4)
loginframe.columnconfigure(0, weight=1)
loginframe.rowconfigure(0, weight=1)

username = StringVar()
password = StringVar()

username_entry = ttk.Entry(loginframe, width=10, textvariable=username) 

# show="*" provides a mask for password entry
password_entry = ttk.Entry(loginframe, show="*", width=10, textvariable=password)

username_entry.grid(column=2, row=1, sticky=(W, E))
password_entry.grid(column=2, row=2, sticky=(W, E))

login_but = ttk.Button(loginframe, text="Login", command=access)
login_but.grid(column=2, row=4, sticky=S)

username_lab = ttk.Label(loginframe, text="Username")
username_lab.grid(column=1, row=1, sticky=W)

password_lab = ttk.Label(loginframe, text="Password")
password_lab.grid(column=1, row=2, sticky=W)

""" Input and output file frame"""
fileframe = ttk.Frame(root)
fileframe.grid(column=1, row=5, columnspan=2, rowspan=3)
fileframe.columnconfigure(0, weight=1)
fileframe.rowconfigure(0, weight=1)

insf_but = ttk.Button(fileframe, text="Input file")
insf_but.grid(column=1, row=2)

outf_but = ttk.Button(fileframe, text="Output file")
outf_but.grid(column=1, row=3)

exit_but = ttk.Button(root, text="Exit", command=exit)
exit_but.grid(column=3, row=9, rowspan=2,sticky=S)


for child in root.winfo_children(): child.grid_configure(padx=5, pady=5)
for child in loginframe.winfo_children(): child.grid_configure(padx=5, pady=5)
for child in queryframe.winfo_children(): child.grid_configure(padx=5, pady=5)
for child in fileframe.winfo_children(): child.grid_configure(padx=5, pady=5)

username_entry.focus()

root.bind('<Return>', access)
root.bind('<Return>', exit)
root.bind('<Return>', frequency_query)

root.mainloop()