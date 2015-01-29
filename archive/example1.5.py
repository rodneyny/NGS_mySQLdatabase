'''
Created on 14 Jan 2015

@author: nyanhr
'''
from Tkinter import *
import ttk 
import mysql.connector as dbm

#MySQL connector connection 
db = dbm.connect(host = "10.101.84.24", \
            port = 3306, \
            user = "user" , \
            password = "passwrd" , \
            database = "VEPvariants" )


# prepare a cursor object using cursor() method
cur = db.cursor()

# def access(*args):
#     """ This function allows the user to connect to the databse with their username
#     and password. """
#     # Global variables for the database connection and the cursor 
#     global db
#     global cur

#     user = str(username.get())
#     passw = str(password.get())

#     #MySQL connector connection 
#     db = dbm.connect(host = "10.101.84.24", \
#                 port = 3306, \
#                 user = user , \
#                 password = passw , \
#                 database = "VEPvariants" )


#     # prepare a cursor object using cursor() method
#     cur = db.cursor()

#     login.loginframe.destroy()
    
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
    #   #print row
    #   for e in range(len(row)):
    #       print str(e) + str(row[e])
    #       rlb = Listbox(query.canvas, height=1)
    #       rlb.pack()
    #       rlb.insert(END, str(e))

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
    #   header.append(line[0])
    # header = '\t'.join(header) + "\n"
    # query.tb.insert(END, header)

    # for row in results:
    #   print row
    #   row = '\t'.join(row)
    #   row =row + "\n"
    #   query.tb.insert(END, row)

def frame2():
    app = login(f1)

def frame3():
    app = query(f2)

def frame4():
    app = getfile(root)

def frame5():
    Example(f2).pack(side=TOP, fill=BOTH, expand=1)



# root is the activity window    
root = Tk()
#root.geometry("1440x900" )
root.title("MOlGEN NGS VARIANTS")

n = ttk.Notebook(root)
n.pack(fill=BOTH, expand=1)
f1 = ttk.Frame(n); # first page, which would get widgets gridded into it
f2 = ttk.Frame(n); # second page
n.add(f1, text='Login')
n.add(f2, text='Variants')

ent_but = ttk.Button(root, text="Enter", command=frame2)
ent_but.pack(side=LEFT)#, expand=1)
#grid(column=1, row=1, rowspan=2, columnspan=2, sticky=S)

search_but =  ttk.Button(root,text="Search for Variants", command=frame5)
search_but.pack(side=LEFT)#, expand=1)
#grid(column=3, row=1, rowspan=2, columnspan=3, sticky=S)

file_but= ttk.Button(root, text="Input and Output files", command=frame3)
file_but.pack(side=LEFT)#, expand=1)
#grid(column=7, row=1, rowspan=2, columnspan=3, sticky=S)

exit_but = ttk.Button(root, text="Exit", command=exit)
exit_but.pack(side=LEFT)#, expand=1)
#grid(column=1, row=3, rowspan=2, columnspan=2, sticky=S) 

for child in root.winfo_children(): child.pack_configure(padx=5, pady=5)

class notebook():
    def __init__(self, root):

        #ttk.Notebook.__init__(self, root)
        self.n = ttk.Notebook(root)
        self.n.pack()
        self.f1 = ttk.Frame(self.n); # first page, which would get widgets gridded into it
        self.f2 = ttk.Frame(self.n); # second page
        self.n.add(self.f1, text='One')
        self.n.add(self.f2, text='Two')

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
        big_dict = {}
        cur.execute("select * from Variants")
        samcount = cur.fetchall()

        
        desc = cur.description
        header = []



        for line in desc:
            header.append(line[0])

        for h in header:
            big_dict[h] = []
        
        for row in samcount:

            row_dict = {}

            for h, v in big_dict.items():
                for key,value in zip(header, row):
                    if h == key:
                        v.append(value)


                # row_dict[key] = value
            # print row_dict

        print big_dict



        lhead = len(header)
        lsam = len(samcount)
        ahead = header[1:]

        for k in big_dict:
            k= Listbox(self.frame, height=lsam+1)


        vlb = Listbox(self.frame, height=lsam+1 )
        vlb.grid(row=0, column=0, rowspan=lsam+1)
        #vlb.grid_columnconfigure(0, weight=1)
        #vlb.grid_rowconfigure(0,weight=1)
        vlb.insert(END, str(header[0]))

        for row in samcount:
            vlb.insert(END, str(row[0]))

        for column in range(len(ahead)):
            h = str(ahead[column])
            ilb = ttk.Label(self.frame, text=h)
            ilb.grid(row=0, column=column+1)
            # ilb.insert(END, str(h))   
            # ilb = Listbox(self.frame, height=1)
            # ilb.grid(row=0, column=column+1)
            # ilb.insert(END, str(h))

        for row in range(lsam):
            r = samcount[row]
            q = r[1: ]
            # print q
            for e in range(len(q)):
                i = str(q[e])
                rlb = ttk.Label(self.frame, text=i)
                rlb.grid(row=row+1 , column=e+1)
                # rlb.insert(END, str(i))
                # rlb = Listbox(self.frame, height=1)
                # rlb.grid(row=row+1 , column=e+1)
                # rlb.insert(END, str(i))

    def OnFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox(ALL))

class query(ttk.Frame):
    """ Visualisation frame for any searches"""

    def __init__(self, root):

        ttk.Frame.__init__(self, f2)

        self.root = f2

        self.queryframe = ttk.Frame(self.root, relief=SUNKEN)
        self.queryframe.pack(fill=BOTH, expand=1)

        self.select = Listbox(self.queryframe, height=4)
        self.select.grid(column=1,  row=1, columnspan=2)
        global canvas

        canvas = Canvas(self.queryframe)
        self.canvas = canvas
        self.canvas.grid(column=0 , row=3 , columnspan=10 , rowspan=10 )

        self.vsb = ttk.Scrollbar(self.queryframe, orient=VERTICAL, command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(side=RIGHT, fill=Y, expand=1)

        self.hsb = ttk.Scrollbar(self.queryframe, orient=HORIZONTAL, command=self.canvas.xview)
        self.canvas.configure(xscrollcommand=self.hsb.set)
        self.hsb.pack(side=BOTTOM, fill=X, expand=1)


        global sel_query

        sel_query = ['Variant','Sample','Gene', 'Transcript']

        self.select.delete(0,END)

        for item in sel_query:
            self.select.insert(END, item)

        global in_val
        in_val = StringVar()

        self.in_val_entry = ttk.Entry(self.canvas, width=20, textvariable=in_val)
        self.in_val_entry.grid(column=3, row=2, rowspan=2, columnspan=2, sticky=(W, E))

        self.in_val_lab = ttk.Label(self.canvas, text="Value")
        self.in_val_lab.grid(column=3, row=1, rowspan=2, columnspan=3, sticky=W)

        self.select_but = ttk.Button(self.canvas, text="Search", command=select_query)
        self.select_but.grid(column=5, row=2, rowspan=2, columnspan=2)

        self.freq_but = ttk.Button(self.canvas, text="Search", command=frequency_query)
        self.freq_but.grid(column=7, row=2, rowspan=2, columnspan=2)

        for child in self.queryframe.winfo_children(): child.grid_configure(padx=5, pady=5)


class login:

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