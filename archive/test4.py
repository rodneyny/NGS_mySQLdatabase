'''
Created on 14 Jan 2015

@author: nyanhr
'''
from Tkinter import *
#from connection import connect 
import mysql.connector as dbm


""" """

def access():
	print "hello"


def exit():
	root.destroy()

# root is the activity window    
root = Tk()
root.geometry("1000x1000" )
root.title("MOlGEN NGS VARIANTS")

#main_sb=Scrollbar(root, orient=VERTICAL)
#root.configure(yscrollcommand=main_sb)
#main_sb.pack()

""" Visualisation frame for any searches"""
queryframe = Frame(root)
queryframe.pack(side=RIGHT)

tb = Text(queryframe)
sb1 = Scrollbar(queryframe, orient=VERTICAL, command=tb.yview)
sb2 = Scrollbar(queryframe, orient=HORIZONTAL, command=tb.xview)
tb.configure(yscrollcommand=sb1.set)
tb.configure(xscrollcommand=sb2.set)
#sb1.config(command=tb.yview)
#sb1.pack(side=RIGHT)
#sb2.pack(side=BOTTOM)
tb.pack(side=BOTTOM)
#queryframe.columnconfigure(0, weight=1)
#queryframe.rowconfigure(0, weight=1)

variant = StringVar()
sample = StringVar()
gene = StringVar()
transcript = StringVar()

variant_entry = Entry(queryframe, width=20, textvariable=variant)
sample_entry = Entry(queryframe, width=20, textvariable=sample)
gene_entry = Entry(queryframe, width=20, textvariable=gene)
transcript_entry = Entry(queryframe, width=20, textvariable=transcript)

variant_entry.pack(side=LEFT)
#grid(column=1, row=2, sticky=(W, E))
sample_entry.pack(side=LEFT)
#grid(column=2, row=2, sticky=(W, E))
gene_entry.pack(side=LEFT)
#grid(column=3, row=2, sticky=(W, E))
transcript_entry.pack(side=LEFT)
#grid(column=4, row=2, sticky=(W, E))

variant_lab = Label(queryframe, text="Variant")
variant_lab.pack(side=LEFT)
#grid(column=1, row=1, sticky=W)
sample_lab = Label(queryframe, text="Sample")
sample_lab.pack()
#grid(column=2, row=1, sticky=W)
gene_lab = Label(queryframe, text="Gene")
gene_lab.pack()
#grid(column=3, row=1, sticky=W)
transcript_lab = Label(queryframe, text="Refseq Transcript")
transcript_lab.pack()
#grid(column=4, row=1, sticky=W)

select_but = Button(queryframe, text="Search")
select_but.pack()
#grid(column=5, row=2)

""" Login frame for application """
loginframe = Frame(root)
loginframe.pack(side=LEFT)
#loginframe.columnconfigure(0, weight=1)
#loginframe.rowconfigure(0, weight=1)

username = StringVar()
password = StringVar()

username_entry = Entry(loginframe, width=10, textvariable=username) 
# show="*" provides a mask for password entry
password_entry = Entry(loginframe, show="*", width=10, textvariable=password)

username_entry.grid(column=2, row=1, sticky=(W, E))
password_entry.grid(column=2, row=2, sticky=(W, E))

login_but = Button(loginframe, text="Login", command=access)
login_but.grid(column=2, row=4, sticky=S)

username_lab = Label(loginframe, text="Username")
username_lab.grid(column=1, row=1, sticky=W)

password_lab = Label(loginframe, text="Password")
password_lab.grid(column=1, row=2, sticky=W)

""" Input and output file frame"""
fileframe = Frame(root)
fileframe.pack(side=LEFT)
#fileframe.columnconfigure(0, weight=1)
#fileframe.rowconfigure(0, weight=1)

insf_but = Button(fileframe, text="Input file")
insf_but.grid(column=1, row=2)

outf_but = Button(fileframe, text="Output file")
outf_but.grid(column=1, row=3)

exit_but = Button(root, text="Exit", command=exit)
exit_but.pack(side=BOTTOM)

for child in loginframe.winfo_children(): child.grid_configure(padx=5, pady=5)
for child in queryframe.winfo_children(): child.grid_configure(padx=5, pady=5)
for child in fileframe.winfo_children(): child.grid_configure(padx=5, pady=5)

username_entry.focus()

root.bind('<Return>', access)
root.bind('<Return>', exit)

root.mainloop()