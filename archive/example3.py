from Tkinter import *
import ttk

class Example(ttk.Frame):
    def __init__(self, root):

        ttk.Frame.__init__(self, root)
        self.canvas = Canvas(root, borderwidth=0)
        self.frame = ttk.Frame(self.canvas)
        self.vsb = ttk.Scrollbar(root, orient=VERTICAL, command=self.canvas.yview)
        self.hsb = ttk.Scrollbar(root, orient=HORIZONTAL, command=self.canvas.xview)

        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.canvas.configure(xscrollcommand=self.hsb.set)

        self.vsb.pack(side=RIGHT, fill=Y)
        self.hsb.pack(side=BOTTOM, fill=X)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=1)
        self.canvas.create_window((4,4), window=self.frame, anchor=NW, 
                                  tags="self.frame")

        self.frame.bind("<Configure>", self.OnFrameConfigure)

        #self.populate()

    def populate(self):
        '''Put in some fake data'''
        for row in range(100):
            ttk.Label(self.frame, text="%s" % row, width=3, borderwidth=1, 
                     relief=SOLID).grid(row=row, column=row)
            t="this is the second colum for row %s" %row
            ttk.Label(self.frame, text=t).grid(row=row, column=row)

    def OnFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox(ALL))

if __name__ == "__main__":
    root=Tk()
    Example(root).pack(side=TOP, fill=BOTH, expand=1)
    root.mainloop()