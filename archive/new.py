'''
Created on 14 Jan 2015

@author: nyanhr
'''
try:
	
    from Tkinter import *
except:
    pass
    print "You are using python 3"

try:
    from tkinter import *
except:
    pass
    print "You are using python 2.7"

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

class app_win(Tk):

    def __init__(self):

        Tk.__init__(self)
        self.title("MOlGEN NGS VARIANTS")

        self.n = ttk.Notebook(self)
        self.n.pack(fill=BOTH, expand=1)
        # first page, which would get widgets gridded into it
        self.f1 = login(self.n); 
        # second page of the frame
        self.f2 = query(self.n); 
        self.f3 = Example(self.n); 
        self.f4 = ttk.Frame(self.n); 
        self.f5 = ttk.Frame(self.n); 
        self.n.add(self.f1, text='Login')
        self.n.add(self.f2, text='Search')
        self.n.add(self.f3, text='Variant')
        self.n.add(self.f4, text='Sample')
        self.n.add(self.f5, text='Input/Output')

        self.ent_but = ttk.Button(self, text="Enter", command=self.frame1)
        self.ent_but.pack(side=LEFT)

        self.search_but =  ttk.Button(self,text="Search for Variants", command=self.frame2)
        self.search_but.pack(side=LEFT)

        self.file_but= ttk.Button(self, text="Input and Output files", command=self.frame4)
        self.file_but.pack(side=LEFT)
        
        self.exit_but = ttk.Button(self, text="Exit", command=self.exit)
        self.exit_but.pack(side=LEFT)
        
        for child in self.winfo_children(): child.pack_configure(padx=5, pady=5)

    def exit(self):
        """Close the database connection and close the window """
        try:
            cur.close()
            db.close()
            self.destroy()
        except:
            self.destroy()

    def frame1(self):
        self.n.select(self.f1)
        # app = login(self.f1)

    def frame2(self):
        self.n.select(self.f2)
        self.n.hide(self.f1)
        # app = query(self.f2)

    def frame3(self):
        self.n.select(self.f3)
        # app = getfile(self)

    def frame4(self):
        self.n.select(self.f5)
        # Example(self.f2).pack(side=TOP, fill=BOTH, expand=1)

class Example(ttk.Frame):
    def __init__(self, parent):

        ttk.Frame.__init__(self,parent)
        self.parent = parent
        self.pack()
        self.canvas = Canvas(self, borderwidth=0)
        self.frame = ttk.Frame(self.canvas)
        self.vsb = ttk.Scrollbar(self, orient=VERTICAL, command=self.canvas.yview)
        self.hsb = ttk.Scrollbar(self, orient=HORIZONTAL, command=self.canvas.xview)

        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.canvas.configure(xscrollcommand=self.hsb.set)
        self.exit_but = ttk.Button(self.canvas, text="Exit", command=self.frequency_query)
        self.exit_but.pack(side=BOTTOM)

        self.vsb.pack(side=RIGHT, fill=Y)
        self.hsb.pack(side=BOTTOM, fill=X)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=1)
        self.canvas.create_window((4,4), window=self.frame, anchor=NW, 
                                  tags="self.frame")

        self.frame.bind("<Configure>", self.OnFrameConfigure)

        # self.frequency_query()

    def frequency_query(self):
        print rlb.curselection()
      
        # cur.execute("select cDNA, Refseq from Variants")
        # samcount = cur.fetchall()

        # desc = cur.description
        # header = []

        # # Add the first item from each line in the description output
        # for line in desc:
        #     header.append(line[0])

        # # Length of header
        # lhead = len(header) 
        # # Number of rows in the results 
        # lsam = len(samcount)

        # for column in range(lhead):
        #     h = str(header[column])
        #     ilb = Listbox(self.frame, height=1)
        #     ilb.grid(row=0, column=column+1)
        #     ilb.insert(END, str(h))

        # for row in range(lsam):
        #     r = samcount[row]
        #     for e in range(len(r)):
        #         i = str(r[e])
        #         rlb = Listbox(self.frame, height=1)
        #         rlb.grid(row=row+1 , column=e+1)
        #         rlb.insert(END, str(i))

    def OnFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox(ALL))

class query(ttk.Frame):
    """ Visualisation frame for any searches"""

    def __init__(self, parent):

        ttk.Frame.__init__(self, parent)
        self.parent = parent
        self.config(relief=SUNKEN)
        self.pack(fill=BOTH, expand=1)

        self.select = Listbox(self, height=4)
        self.select.grid(column=1,  row=1, columnspan=2)

        global sel_query

        sel_query = ['Variant','Sample','Gene','Transcript']

        self.select.delete(0,END)

        for item in sel_query:
            self.select.insert(END, item)

        global in_val
        in_val = StringVar()
        
        global rlb
        
        rlb = None

        # Widgets
        self.in_val_entry = ttk.Entry(self, width=20, textvariable=in_val)
        self.in_val_lab = ttk.Label(self, text="Value")
        self.select_but = ttk.Button(self, text="Search", command=self.select_query)

        # Grid 
        self.select.grid(column=0,  row=0, rowspan=4)
        self.in_val_entry.grid(column=3, row=5, sticky=(W, E))
        self.in_val_lab.grid(column=0, row=5, sticky=W)
        self.select_but.grid(column=5, row=5)


        for child in self.winfo_children(): child.grid_configure(padx=5, pady=5)

    def select_query(self):
        """ This query will output data from the database when a specific
         variant, sample, gene or transcript is searched for""" 

        self.canvas = Canvas(self, borderwidth=0)
        self.frame = ttk.Frame(self.canvas)
        self.vsb = ttk.Scrollbar(self, orient=VERTICAL, command=self.canvas.yview)
        self.hsb = ttk.Scrollbar(self, orient=HORIZONTAL, command=self.canvas.xview)
        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.canvas.configure(xscrollcommand=self.hsb.set)
        self.exit_but = ttk.Button(self.canvas, text="Exit", command=self.can_exit)
        self.vsb.pack(side=RIGHT, fill=Y)
        self.exit_but.pack(side=BOTTOM)
        self.hsb.pack(side=BOTTOM, fill=X)

        self.canvas.pack(side=BOTTOM, fill=BOTH, expand=1)
        self.canvas.create_window((4,4), window=self.frame, anchor=NW, 
                                  tags="self.frame")

        self.frame.bind("<Configure>", self.OnFrameConfigure)
        self.search()

    def can_exit(self):
        self.canvas.pack_forget()

    def search(self):
        indx = int(self.select.curselection()[0])
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

        # Fetch all the rows in a list of lists.
        results = cur.fetchall()
        print results
        desc = cur.description
        header = []

        # Add the first item from each line in the description output
        for line in desc:
            header.append(line[0])

        # Length of header
        lhead = len(header) 
        # Number of rows in the results 
        lsam = len(results)

        for column in range(lhead):
            h = str(header[column])
            ilb = Listbox(self.frame, height=1)
            ilb.grid(row=0, column=column+1)
            ilb.insert(END, str(h))

        for row in range(lsam):
            r = results[row]
            for e in range(len(r)):
                i = str(r[e])
                rlb = Listbox(self.frame, height=1)
                rlb.grid(row=row+1 , column=e+1)
                rlb.insert(END, str(i))
		print rlb

    def OnFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox(ALL))

class login(ttk.Frame):
    """ Login frame for application """
    def __init__(self, parent):
        ttk.Frame.__init__(self,parent)
        self.parent = parent 
        self.pack(fill=BOTH, expand=1)

        global username
        global password

        username = StringVar()
        password = StringVar()

        self.username_entry = ttk.Entry(self, width=20, textvariable=username) 

        # show="*" provides a mask for password entry
        self.password_entry = ttk.Entry(self, show="*", width=20, textvariable=password)

        self.username_entry.grid(column=2, row=1, sticky=(W, E))
        self.password_entry.grid(column=2, row=2, sticky=(W, E))

        self.login_but = ttk.Button(self, text="Login", command=self.access)
        self.login_but.grid(column=2, row=4, sticky=S)

        self.username_lab = ttk.Label(self, text="Username")
        self.username_lab.grid(column=1, row=1, sticky=W)

        self.password_lab = ttk.Label(self, text="Password")
        self.password_lab.grid(column=1, row=2, sticky=W)

        for child in self.winfo_children(): child.grid_configure(padx=5, pady=5)

        self.username_entry.focus()

    def access(self):
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

        except:
            login_err = "Username or password is incorrect and could not be found"
            error_lab = ttk.Label(self, text=login_err)
            error_lab.grid(column=0, row=6, columnspan=3, sticky=(W,E))
        
class getfile(ttk.Frame):
    """ Input and output file frame"""    
    def __init__(self,parent):
        ttk.Frame.__init__(self,parent)
        self.parent = parent
        self.pack(fill=BOTH, expand=1)

        self.insf_but = ttk.Button(self, text="Input file")
        self.insf_but.grid(column=1, row=2)

        self.outf_but = ttk.Button(self, text="Output file")
        self.outf_but.grid(column=1, row=3)

        for child in self.winfo_children(): child.grid_configure(padx=5, pady=5)

if __name__=="__main__":
    app = app_win()
    app.mainloop()
