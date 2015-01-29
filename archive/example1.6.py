'''
Created on 14 Jan 2015

@author: nyanhr
'''

''' to do:
	# Make the search queries work and be more specific
	# Tidy up gui so that it looks more user friendly 
	# Use not book notation more effectively  
'''
from Tkinter import *
import ttk 
import mysql.connector as dbm


def access(*args):
	""" This function allows the user to connect to the databse with their username
	and password. """
	# Global variables for the database connection and the cursor 
	global db
	global cur

	user = str(username.get())
	passw = str(password.get())
	try:
		#MySQL connector connection 
		db = dbm.connect(host = "10.101.84.24", \
					port = 3306, \
					user = user , \
					password = passw , \
					database = "VEPvariants" )


		# prepare a cursor object using cursor() method
		cur = db.cursor()

		login.loginframe.destroy()
	except:
		error_lab = ttk.Label(login.loginframe, text="Username or password is incorrect \
			and could not be found")
		error_lab.grid(column=0, row=6, columnspan=3, sticky=(W,E))
	
def exit(*args):
	"""Close the database connection and close the window """
	try:
		cur.close()
		db.close()
		root.destroy()
	except:
		root.destroy()


def frequency_query():
	""" """
	cur.execute("select * from Variants")
							
	samcount = cur.fetchall()
	desc = cur.description

	#Create a header based on the description values of each column
	#Use index [0] from the description

	header = []

	for line in desc:
		header.append(line[0])

	for column in range(len(header)):
		#print column
		#print str(column) + str(header[column])
		h = str(header[column])	
		ilb = Listbox(canvas, height=1, width=5)
		ilb.grid(row=0, column=column)
		ilb.insert(END, str(h))


	# for row in samcount:
	# 	#print row
	# 	for e in range(len(row)):
	# 		print str(e) + str(row[e])
	# 		rlb = Listbox(query.canvas, height=1)
	# 		rlb.pack()
	# 		rlb.insert(END, str(e))

def select_query():
	# """ This query will output data from the database when a specific
	# variant, sample, gene or transcript is searched for"""
	indx = int(select.curselection()[0])
	sel = sel_query[indx]

	sql = ""

	if sel == "Variant":
		sql = "select * from Variants where cDNA = %s"
		value = str(in_val.get())
	elif sel == "Sample":
		sql = "select * from Samples where SampleNumber = %s"
		value = str(in_val.get())
	elif sel == "Gene":
		sql = "select * from Genes where Gene = %s"
		value = str(in_val.get())
	elif sel == "Transcript":
		sql = "select * from Variants where Refseq = %s"
		value = str(in_val.get())
	else:
		print "You have not made a valid selection"

	
	sql1 = cur.execute(sql,[value])

	##Fetch all the rows in a list of lists.
	results = cur.fetchall()
	print results
	# desc = cur.description

	# header = []
	# for line in desc:
	# 	header.append(line[0])
	# header = '\t'.join(header) + "\n"
	# query.tb.insert(END, header)

	# for row in results:
	# 	print row
	# 	row = '\t'.join(row)
	# 	row =row + "\n"
	# 	query.tb.insert(END, row)

def frame2():
	n.select(f1)
	# try:
	# 	login.loginframe.destroy()
	# except:
	# 	pass
	app = login(f1)

def frame3():
	n.select(f3)
	app = query(f3)

def frame4():
	app = getfile(root)

def frame5():
	n.select(f2)
	Example(f2).pack(side=TOP, fill=BOTH, expand=1)

# root is the activity window    
root = Tk()
#root.geometry("1440x900" )
root.title("MOlGEN NGS VARIANTS")

ent_but = ttk.Button(root, text="Enter", command=frame2)
search_but = ttk.Button(root,text="Search for Variants", command=frame5)
file_but= ttk.Button(root, text="Input and Output files", command=frame3)
exit_but = ttk.Button(root, text="Exit", command=exit)

n = ttk.Notebook(root)
f1 = ttk.Frame(n); # first page, which would get widgets gridded into it
f2 = ttk.Frame(n); # second page
f3 = ttk.Frame(n); 
f4 = ttk.Frame(n); 
f5 = ttk.Frame(n); 
n.add(f1, text='Login')
n.add(f2, text='Variants')
n.add(f3, text='Variant')
n.add(f4, text='Input/Output')
n.add(f5, text='Genes')

n.pack(side=TOP, fill=BOTH, expand=1)
ent_but.pack(side=LEFT)
search_but.pack(side=LEFT)
file_but.pack(side=LEFT)
exit_but.pack(side=LEFT)


for child in root.winfo_children(): child.pack_configure(padx=5, pady=5)

class Example(ttk.Frame):
    def __init__(self, root):

        ttk.Frame.__init__(self, f2)
        self.canvas = Canvas(f2, borderwidth=0)
        self.frame = ttk.Frame(self.canvas)
        self.vsb = ttk.Scrollbar(f2, orient=VERTICAL, command=self.canvas.yview)
        self.hsb = ttk.Scrollbar(f2, orient=HORIZONTAL, command=self.canvas.xview)

        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.canvas.configure(xscrollcommand=self.hsb.set)

        self.vsb.pack(side=RIGHT, fill=Y)
        self.hsb.pack(side=BOTTOM, fill=X)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=1)
        self.canvas.create_window((4,4), window=self.frame, anchor=NW, 
                                  tags="self.frame")

        self.frame.bind("<Configure>", self.OnFrameConfigure)

        self.frequency_query()

    def frequency_query(self):
		cur.execute("select * from Variants")
								
		samcount = cur.fetchall()
		desc = cur.description
		header = []

		for line in desc:
			header.append(line[0])

		for column in range(len(header)):
			h = str(header[column])	
			#ilb = ttk.Label(self.frame, text=str(h))
			ilb = Listbox(self.frame, height=1 )
			ilb.grid(row=0, column=column)
			ilb.insert(END, str(h))

		for row in range(len(samcount)):
			r = samcount[row]
			for e in range(len(r)):
				i = str(r[e])
				#rlb = ttk.Label(self.frame, text=str(i))
				rlb = Listbox(self.frame, height=1 )
				rlb.grid(row=row+1 , column=e)
				rlb.insert(END, str(i))

    def OnFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox(ALL))

class query(ttk.Frame):
	""" Visualisation frame for any searches"""

	def __init__(self, root):

		ttk.Frame.__init__(self, f3)

		self.root = f3
		self.queryframe = ttk.Frame(self.root, relief=SUNKEN)
		self.queryframe.pack(fill=BOTH, expand=1)
		
		global select
		select = Listbox(self.queryframe, height=4)
		self.select = select
		
		# global canvas
		# canvas = Canvas(self.queryframe)
		# self.canvas = canvas
		
		global sel_query
		sel_query = ['Variant','Sample','Gene', 'Transcript']
		self.select.delete(0,END)
		for item in sel_query:
			self.select.insert(END, item)

		global in_val
		in_val = StringVar()

		self.in_val_entry = ttk.Entry(self.queryframe, width=20, textvariable=in_val)
		self.in_val_lab = ttk.Label(self.queryframe, text="Value")
		self.select_but = ttk.Button(self.queryframe, text="Search", command=select_query)
		#self.freq_but = ttk.Button(self.queryframe, text="Search", command=frequency_query)

		
		# Grid 
		self.select.grid(column=0,  row=0, rowspan=4)
		# self.canvas.grid(column=0 , row=3 , columnspan=10 , rowspan=10 )
		self.in_val_entry.grid(column=3, row=5, sticky=(W, E))
		self.in_val_lab.grid(column=0, row=5, sticky=W)
		self.select_but.grid(column=5, row=5)
		#self.freq_but.grid(column=7, row=2, rowspan=2, columnspan=2)

		for child in self.queryframe.winfo_children(): child.grid_configure(padx=5, pady=5)


class login():

		loginframe = ttk.Frame(f1)
		loginframe.pack(side=BOTTOM, fill=BOTH, expand=1)

		def __init__(self, parent):

			self.parent = parent 

			""" Login frame for application """

			global username
			global password
			username = StringVar()
			password = StringVar()

			self.username_entry = ttk.Entry(self.loginframe, width=20, textvariable=username) 

			# show="*" provides a mask for password entry
			self.password_entry = ttk.Entry(self.loginframe, show="*", width=20, textvariable=password)

			self.username_entry.grid(column=2, row=1, sticky=(W, E))
			self.password_entry.grid(column=2, row=2, sticky=(W, E))

			self.login_but = ttk.Button(self.loginframe, text="Login", command=access)
			self.login_but.grid(column=2, row=4, sticky=S)

			self.username_lab = ttk.Label(self.loginframe, text="Username")
			self.username_lab.grid(column=1, row=1, sticky=W)

			self.password_lab = ttk.Label(self.loginframe, text="Password")
			self.password_lab.grid(column=1, row=2, sticky=W)

			for child in self.loginframe.winfo_children(): child.grid_configure(padx=5, pady=5)

			self.username_entry.focus()


class getfile:
	""" Input and output file frame"""
	fileframe = ttk.Frame(root)
	fileframe.pack(fill=BOTH, expand=1)

	def __init__(self, parent):
		self.parent = parent

		self.insf_but = ttk.Button(self.fileframe, text="Input file")
		self.insf_but.grid(column=1, row=2)

		self.outf_but = ttk.Button(self.fileframe, text="Output file")
		self.outf_but.grid(column=1, row=3)
		for child in self.fileframe.winfo_children(): child.grid_configure(padx=5, pady=5)

root.mainloop()

if __name__=="main":
	logintest=login()
	print dir(logintest)
