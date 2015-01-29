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
import tkFileDialog
import mysql.connector as dbm
import csv
from fromFile import filelist

# #MySQL connector connection 
# db = dbm.connect(host = "10.101.84.24", \
#             port = 3306, \
#             user = "user" , \
#             password = "passwrd" , \
#             database = "VEPvariants" )
# 
# # prepare a cursor object using cursor() method
# cur = db.cursor()

class App_win(Tk):

    def __init__(self):

        Tk.__init__(self)
        self.title("MOlGEN NGS VARIANTS")

        self.n = ttk.Notebook(self)
        self.n.pack(fill=BOTH, expand=1)
        # first page, which would get widgets packed into it
        # second page of the frame
    
        self.ent_but = ttk.Button(self, text="Enter", command=self.frame1)
        self.ent_but.pack(side=LEFT)

        self.search_but =  ttk.Button(self,text="Search for Variants", command=self.frame2)
        self.search_but.pack(side=LEFT)

        self.file_but= ttk.Button(self, text="Input and Output files", command=self.frame5)
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
        self.f1 = login(self.n)
        self.n.add(self.f1, text='Login')
        self.n.select(self.f1)


    def frame2(self):
        try:
            self.f2.destroy()
        except:
            pass 
        self.f2 = Query(self.n); 
        self.n.add(self.f2, text='Search')
        self.n.select(self.f2)
        try:
            self.n.hide(self.f1)
        except:
            pass


    def frame3(self):
        self.f3 = Results(self.n)
        self.n.add(self.f3, text='Results')
        self.n.select(self.f3)


    def frame4(self):
        self.f4 = ttk.Frame(self.n);
        self.n.add(self.f4, text='Sample')
        self.n.select(self.f4)

    def frame5(self):
        try:
            self.n.hide(self.f1)
        except:
            pass
        self.f5 = getfile(self.n); 
        self.n.add(self.f5, text='Input/Output')
        self.n.select(self.f5)

class Results(ttk.Frame):
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
        self.search_but = ttk.Button(self.canvas, text="Search", command=self.detail)
        self.exit_but = ttk.Button(self.canvas, text="Exit", command=self.can_exit)
        self.search_but.pack(side=BOTTOM)
        self.exit_but.pack(side=BOTTOM)

        self.vsb.pack(side=RIGHT, fill=Y)
        self.hsb.pack(side=BOTTOM, fill=X)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=1)
        self.canvas.create_window((4,4), window=self.frame, anchor=NW, 
                                  tags="self.frame")

        self.frame.bind("<Configure>", self.OnFrameConfigure)

        self.frequency_query()

    def frequency_query(self):

        cur.execute(sql,[value])

        # Fetch all the rows in a list of lists.
        global results
        results = cur.fetchall()
        desc = cur.description
        global header 
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
                self.rlb = Listbox(self.frame, height=1)
                self.rlb.grid(row=row+1 , column=e+1)
                self.rlb.insert(END, str(i))

#         variant = []
#         for row in results:
#             variant.append(row[0])
#         print variant

    def detail(self):
        indx = self.rlb.curselection()
        print indx


    def OnFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox(ALL))

    def can_exit(self):
        self.destroy()

class Query(ttk.Frame):
    """ Visualisation frame for any searches"""

    def __init__(self, parent):

        ttk.Frame.__init__(self, parent)
        self.parent = parent
        self.config(relief=SUNKEN)
        self.pack(fill=BOTH, expand=1)

        global sel_query

        sel_query = ['Variant','Sample','Gene','Transcript','Classification']

        global in_val
        in_val = StringVar()

        # Widgets
        self.select = Listbox(self, height=len(sel_query))
        self.select.delete(0,END)

        for item in sel_query:
            self.select.insert(END, item)

        self.in_val_entry = ttk.Entry(self, width=20, textvariable=in_val)
        self.in_val_lab = ttk.Label(self, text="Value")
        self.select_but = ttk.Button(self, text="Search", command=self.search)
        # Grid 
        self.select.grid(column=0,  row=0, rowspan=4)
        self.in_val_entry.grid(column=3, row=5, sticky=(W, E))
        self.in_val_lab.grid(column=0, row=5, sticky=W)
        self.select_but.grid(column=5, row=5)
        for child in self.winfo_children(): child.grid_configure(padx=5, pady=5)

    def search(self):
        """ This query will output data from the database when a specific
         variant, sample, gene or transcript is searched for""" 
         
        
        
        indx = int(self.select.curselection()[0])
        sel = sel_query[indx]

        global sql 
        sql = ""
        global value
        value = ""
        if sel == "Variant":
            sql = "select * from Variants where cDNA = %s"
            value = str(in_val.get())
        elif sel == "Sample":
            sql = "select * from Occurrence where SampleNumber = %s"
            value = str(in_val.get())
        elif sel == "Gene":
            sql = "select * from Variants \
            inner join Transcripts \
            on Variants.Refseq=Transcripts.Refseq \
            where Gene = %s"
            value = str(in_val.get())
        elif sel == "Transcript":
            sql = "select * from Variants where Refseq = %s"
            value = str(in_val.get())
        elif sel == "Classification":
            sql = "select * from Variants where Classification= %s"
            value = str(in_val.get())    
        else:
            print "You have not made a valid selection"

        App_win.frame3(app)

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

        self.insf_but = ttk.Button(self, text="Input file", command=self.data_update)
        self.insf_but.grid(column=2, row=2)
        
        inl = "Select your file"
        
        self.insf_lab = ttk.Label(self, text=inl)
        self.insf_lab.grid(column=1, row=2, sticky=W)
    
        
        outl= "Please enter your filename"
        
        self.outf_lab = ttk.Label(self, text=outl)
        self.outf_lab.grid(column=1, row=3, sticky=W)

        self.outf_but = ttk.Button(self, text="Output file", command=self.save_res)
        self.outf_but.grid(column=3, row=3)
        
        global filename
        
        filename =  StringVar()
        self.outf_entry = ttk.Entry(self, width=20, textvariable=filename)
        self.outf_entry.grid(column=2, row=3, sticky=(W, E)) 

        
        for child in self.winfo_children(): child.grid_configure(padx=5, pady=5)
        
        
    def save_res(self):
        
        newfile = str(filename.get())
 
        f = open(newfile,'w')
        c = csv.writer(f, delimiter ='\t')
         
        c.writerow(header)
         
        for row in results:
            c.writerow(row)
        print "Finished!"

    def data_update(self):
        ftypes = [('Python files', '*.py'), ('All files', '*')]
        dlg = tkFileDialog.Open(self, filetypes = ftypes)
        fl = dlg.show()
        
        if fl != '':
            record = filelist(fl,'record')
            
            # Remove the header from the dictionary
            record.remove(record[0])
            
            try:
                for line in record:
                    var = line[0:67]
                    var.remove(var[3])
            
                    # For floats use the %f placeholder instead of the %d placeholder
                    cur.executemany("""insert ignore into Variants (cDNA, 
                                Refseq, HGVSNomen, GT, GQ, SDP, DP, RD,
                                AD, FREQ, PVAL, RBQ, ABQ, RDF, RDR, ADF,
                                ADR, CHROM, POS, REF, ALT, ID, info_ADP,
                                info_WT, info_HET, info_HOM, info_NC, CSQ_Allele,    
                                CSQ_Gene, CSQ_Feature, CSQ_Feature_type, CSQ_Consequence,
                                CSQ_cDNA_position, CSQ_CDS_position, CSQ_Protein_position,
                                CSQ_Amino_acids, CSQ_Codons, CSQ_Existing_variation,    
                                CSQ_AA_MAF, CSQ_EA_MAF, CSQ_ALLELE_NUM, CSQ_EXON, CSQ_INTRON,
                                CSQ_DISTANCE, CSQ_CLIN_SIG, CSQ_CANONICAL, CSQ_SYMBOL,
                                CSQ_BIOTYPE, CSQ_ENSP, CSQ_DOMAINS, CSQ_CCDS, CSQ_AFR_MAF, CSQ_AMR_MAF,
                                CSQ_ASN_MAF, CSQ_EUR_MAF, CSQ_FATHMM, SIFT, SIFT_scoe, POLYPHEN, POLYPHEN_SCORE,    
                                1KG_Allele,    1KG_MAF, HGVS_transcript, HGVSc, HGVS_protein,    HGVSp) 
                                values (%s,%s,%s, %s,%s,%s,%s,%s,%s,%s,%s,%s,
                                %s,%s,%s,%s,%s,%s, %s,%s,%s,%s,%s,%s,%s,%s,%s,
                                %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, 
                                %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s,%s,%s,%s,%s,%s, 
                                %s, %s,%s,%s,%s,%s)""" , [var])
                    #print "Rows in the Variants table were populated"
            except:
                print "an error occurred inserting variants"
                db.rollback()
            
                
            try:
                for line in record:
                    PK = line[0]
                    sample = line[3]
                    gt = line[4]
                    cur.execute("insert ignore into Samples ( SampleNumber)\
                                  values ('%s')" % (sample))
                    #print "Rows in the Samples table were populated"
                    
                    cur.execute("insert into Occurrence (SampleNumber, cDNA, Genotype) \
                                   values ('%s', '%s', '%s')" % (sample, PK, gt))
                    #print "Rows in the Occurrence table were populated" 
                    db.commit()
                print "records successfully added to database"
            except:
                print "an error occurred inserting samples"
                db.rollback()
                
            # Add the number of times a variant has been seen previously in the lab    
            try:
                cur.execute("select cDNA ,count(SampleNumber)as EpisodeCount \
                                from Occurrence \
                                group by cDNA")    
                                
                samcount = cur.fetchall()
            
                for line in samcount:
                    cdna = line[0]
                    count = line[1]
                    
                    cur.execute("Update Variants set Frequency \
                                    = %s \
                                    where cDNA = %s" ,(count,cdna))
                    db.commit()
                print "Frequency updated"    
            except:
                print " The frequency was not updated"
                db.rollback()

if __name__=="__main__":
    app = App_win()
    app.mainloop()