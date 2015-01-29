'''
Created on 14 Jan 2015

@author: nyanhr
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

	#MySQL connector connection 
	db = dbm.connect(host = "10.101.84.24", \
				port = 3306, \
				user = user , \
				password = passw , \
				database = "VEPvariants" )


	# prepare a cursor object using cursor() method
	cur = db.cursor()

	login.loginframe.destroy()
	
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
	# cur.execute("select cDNA ,count(SampleNumber)as EpisodeCount \
	# 					from Occurrence \
	# 					group by cDNA")	

	cur.execute("select * from Variants")
							
	samcount = cur.fetchall()
	print len(samcount)
	desc = cur.description
	#print desc

	#Create a header based on the description values of each column
	#Use index [0] from the description

	header = []

	for line in desc:
		header.append(line[0])
	print len(header)

	for column in range(len(header)):
		#print column
		print str(column) + str(header[column])
		h = str(header[column])	
		ilb = Listbox(query.canvas, height=1)
		ilb.pack(side=LEFT)
		ilb.insert(END, str(h))
	# header = '\t'.join(header) + "\n"

	# lab = ttk.Label(query.canvas, text=header)
	# lab.pack(side=BOTTOM)
	# # print header
	
	# # query.tb.insert(END, header)

	# for row in samcount:
	# 	print len(row)

		# for e in row:
		# 	print e
		# 	rlb = Listbox(query.canvas, height=1)
		# 	rlb.pack()
		# 	rlb.insert(END, str(e))

		# print row
		# row = '\t'.join(str(e) for e in row)
		# lab = ttk.Label(query.canvas, text=row)
		# lab.pack(side=BOTTOM)
		# row = ' | '.join(str(e) for e in row)
		# row =row + "\n"
		# query.tb.insert(END, row)


def select_query():
	# """ This query will output data from the database when a specific
	# variant, sample, gene or transcript is searched for"""
	indx = int(query.select.curselection()[0])
	sel = sel_query[indx]

	sql = " "

	if sel == "Variant":
		sql = "select * from Variants where cDNA = '%s'"
		value = str(in_val.get())
	elif sel == "Sample":
		sql = "select * from Samples where SampleNumber = '%s'"
		value = str(in_val.get())
	elif sel == "Gene":
		sql = "select * from Genes where Gene = '%s'"
		value = str(in_val.get())
	elif sel == "Transcript":
		sql = "select * from Variants where Refseq = '%s'"
		value = str(in_val.get())
	else:
		print "You have not made a valid selection"
	
	cur.execute(sql,value)
	##Fetch all the rows in a list of lists.
	results = cur.fetchall()
	print results
	desc = cur.description

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


#def insert_query():
# """ """

# def pipeline_query():	
# """ """

def hello():
    print "hello!"

# root is the activity window    
root = Tk()
#root.geometry("1440x900" )
root.title("MOlGEN NGS VARIANTS")

menubar = Menu(root)

# create a pulldown menu, and add it to the menu bar
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Open", command=hello)
filemenu.add_command(label="Save", command=hello)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)

# create more pulldown menus
editmenu = Menu(menubar, tearoff=0)
editmenu.add_command(label="Cut", command=hello)
editmenu.add_command(label="Copy", command=hello)
editmenu.add_command(label="Paste", command=hello)
menubar.add_cascade(label="Edit", menu=editmenu)

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="About", command=hello)
menubar.add_cascade(label="Help", menu=helpmenu)

# display the menu
root.config(menu=menubar)

class main_frame:
	mainframe= ttk.Frame(root)
	mainframe.pack(fill=BOTH )

	def __init__(self, root):
		self.root = root

		# self.sb3 = Scrollbar(self.mainframe, orient=HORIZONTAL)
		# self.mainframe.configure(xscrollcommand=self.sb3.set)
		# self.sb3.config(command=self.mainframe.xview)
		# self.sb3.pack(side=BOTTOM) #grid(column=0, row=21, sticky=(E,S))

		# self.main_lab = ttk.Label(self.mainframe, text="I am the mainframe")
		# self.main_lab.pack(side=LEFT, fill=BOTH, expand=1)
		#grid(column=1, row=20, columnspan=10, sticky=W)

		self.ent_but = ttk.Button(self.mainframe, text="Enter", command=self.frame2)
		self.ent_but.pack(side=LEFT)#, expand=1)
		#grid(column=1, row=1, rowspan=2, columnspan=2, sticky=S)

		self.search_but =  ttk.Button(self.mainframe,text="Search for Variants", command=self.frame3)
		self.search_but.pack(side=LEFT)#, expand=1)
		#grid(column=3, row=1, rowspan=2, columnspan=3, sticky=S)

		self.file_but= ttk.Button(self.mainframe, text="Input and Output files", command=self.frame4)
		self.file_but.pack(side=LEFT)#, expand=1)
		#grid(column=7, row=1, rowspan=2, columnspan=3, sticky=S)

		self.exit_but = ttk.Button(self.mainframe, text="Exit", command=exit)
		self.exit_but.pack(side=LEFT)#, expand=1)
		#grid(column=1, row=3, rowspan=2, columnspan=2, sticky=S) 

		for child in self.mainframe.winfo_children(): child.pack_configure(padx=5, pady=5)

	def frame2(self):
		# try:
		# 	query.queryframe.destroy()
		# except:
		# 	pass

		self.app = login(self.mainframe)

	def frame3(self):
		self.app = query(self.root)

	def frame4(self):
		self.app = getfile(self.mainframe)

class query:
	""" Visualisation frame for any searches"""
	canvas = Canvas(root)
	#queryframe = ttk.Frame(canvas, relief=SUNKEN)
	#canvas.create_window((4,4), window=queryframe, anchor=NW, 
						  #tags="queryframe")
	# queryframe = ttk.Frame(main_frame.mainframe, relief=SUNKEN)
	# queryframe.pack(fill=BOTH, expand=1)

	#select = Listbox(queryframe, height=4)
	select = Listbox(canvas, height=4)
	# select.pack(side=TOP)
	# tb = Listbox(queryframe)
	# tb.pack(side=BOTTOM, fill=BOTH, expand=1)

	def __init__(self, root):
		self.root = root
		self.canvas.pack(fill=BOTH, expand=1)
		self.select.pack(side=TOP)
		self.vsb = Scrollbar(self.root, orient=VERTICAL, command=self.canvas.yview)
		#self.canvas.configure(yscrollcommand=self.vsb.set)
		self.canvas['yscrollcommand'] = self.vsb.set
		#self.vsb.pack(side=RIGHT, fill=Y)
		self.hsb = Scrollbar(self.root, orient=HORIZONTAL, command=self.canvas.xview)
		#self.canvas.configure(xscrollcommand=self.hsb.set)
		self.canvas['xscrollcommand'] = self.hsb.set
		self.vsb.pack(side=RIGHT, fill=Y, expand=1)
		self.hsb.pack(side=BOTTOM, fill=X, expand=1)
		

		# self.tb.pack(side=BOTTOM, fill=BOTH, expand=1)
		# self.sb1 = Scrollbar(self.tb, orient=VERTICAL)
		# self.sb2 = Scrollbar(self.tb, orient=HORIZONTAL)
		# self.tb.configure(yscrollcommand=self.sb1.set)
		# self.tb.configure(xscrollcommand=self.sb2.set)
		# self.sb1.config(command=self.tb.yview)
		# self.sb2.config(command=self.tb.xview)
		# self.tb.grid(column= 1, row=9, columnspan=20,rowspan=6, sticky=(N, W, E, S) )
		# self.tb.columnconfigure(0, weight=1)
		# self.tb.rowconfigure(0, weight=1)
		# self.sb1.grid(column=6, row=0, sticky=(E, S))
		# self.sb2.grid(column=0, row=6, sticky=(E,S))

		# self.select.grid(column=1,  row=1, columnspan=2)

		global sel_query
		sel_query = ['Variant','Sample','Gene', 'Transcript']

		self.select.delete(0,END)

		for item in sel_query:
			self.select.insert(END, item)

		global in_val
		in_val = StringVar()

		self.in_val_entry = ttk.Entry(self.canvas, width=20, textvariable=in_val)
		self.in_val_entry.pack()
		# grid(column=3, row=2, rowspan=2, columnspan=2, sticky=(W, E))

		self.in_val_lab = ttk.Label(self.canvas, text="Value")
		self.in_val_lab.pack()
		# grid(column=3, row=1, rowspan=2, columnspan=3, sticky=W)

		self.select_but = ttk.Button(self.canvas, text="Search", command=select_query)
		self.select_but.pack()
		# grid(column=5, row=2, rowspan=2, columnspan=2)

		self.freq_but = ttk.Button(self.canvas, text="Search", command=frequency_query)
		self.freq_but.pack()
		# grid(column=7, row=2, rowspan=2, columnspan=2)
		for child in self.canvas.winfo_children(): child.pack_configure(padx=5, pady=5)


class login:

	loginframe = ttk.Frame(main_frame.mainframe)
	loginframe.pack(fill=BOTH, expand=1)

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
	fileframe = ttk.Frame(main_frame.mainframe)
	fileframe.pack(fill=BOTH, expand=1)

	def __init__(self, parent):
		self.parent = parent

		self.insf_but = ttk.Button(self.fileframe, text="Input file")
		self.insf_but.grid(column=1, row=2)

		self.outf_but = ttk.Button(self.fileframe, text="Output file")
		self.outf_but.grid(column=1, row=3)
		for child in self.fileframe.winfo_children(): child.grid_configure(padx=5, pady=5)


app = main_frame(root)
root.mainloop()