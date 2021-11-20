from tkinter import *
from tkinter import filedialog
import pandas as pand
import cx_Oracle as pyo
from tkinter import Tk, Button,Label,Scrollbar,Listbox,StringVar,Entry,W,E,N,S,END
from tkinter import ttk
from tkinter import messagebox
dbcon='System/newpassword@localhost'
con = pyo.connect(dbcon)
cursor = con.cursor()

cursor.execute("create table netflix ( show_id	varchar2(800),type varchar2(800),	title varchar2(800),	director varchar2(800),	cast varchar2(800),	country	varchar2(800),date_added	varchar2(800),release_year	varchar2(800),rating	varchar2(800),duration	varchar2(800),listed_in	varchar2(800),description varchar2(800))")
def insertd(l):
    sql = ("INSERT INTO netflix(SHOW_ID,TYPE,TITLE, DIRECTOR, CAST, COUNTRY, DATE_ADDED, RELEASE_YEAR, RATING, DURATION, LISTED_IN, DESCRIPTION) VALUES (:SHOW_ID,:TYPE,:TITLE, :DIRECTOR, :CAST, :COUNTRY, :DATE_ADDED, :RELEASE_YEAR, :RATING, :DURATION, :LISTED_IN, :DESCRIPTION)")
    cursor.executemany(sql,l)
    con.commit()

def browseFiles():
    global filename
    filename = filedialog.askopenfilename(initialdir="/",
                                          title="Select CSV a File",
                                          filetypes=(("Csv files",
                                                      "*.csv"),
                                                     ("all files",
                                                      "*.*")))
    label_file_explorer.configure(text="File Opened: " + filename)
    df = pand.read_csv(filename).astype(str)
    xx = [tuple(x) for x in df.values]
    insertd(xx)


class Netflixdb:
    def __init__(self):
        self.con = pyo.connect(dbcon)
        self.cursor = con.cursor()
        print("You have connected to the  database")
        print(con)

    def __del__(self):
        self.con.close()

    def view(self):
        self.cursor.execute("SELECT * FROM netflix")
        rows = self.cursor.fetchall()
        return rows

    def delete(self, id):
        delquery ='DELETE FROM netflix WHERE show_id = :id'
        self.cursor.execute(delquery, [id])
        self.con.commit()
        messagebox.showinfo(title="Netflix Database",message="Netflix Show Deleted!!")
db = Netflixdb()
def get_selected_row(event):
    global selected_tuple
    index = list_bx.curselection()[0]
    selected_tuple = list_bx.get(index)

def view_records():
    list_bx.delete(0, 'end')
    for row in db.view():
        list_bx.insert('end', row)

def delete_records():
    db.delete(selected_tuple[0])
    print(selected_tuple[0])
    con.commit()

def clear_screen():
    list_bx.delete(0,'end')

root = Tk()  # Creates application window

root.title("Netflix Database App") # Adds a title to application window
root.configure(background="light blue")  # Add background color to application window
root.geometry("850x500")  # Sets a size for application window
root.resizable(width=False,height=False) # Prevents the application window from resizing



# Add  a listbox  to display data from database
list_bx = Listbox(root,height=14,width=70,font="helvetica 13",bg="light blue")
list_bx.grid(row=3,column=1, columnspan=14,sticky=W + E,pady=40,padx=15)
list_bx.bind('<<ListboxSelect>>',get_selected_row)

# Add scrollbar to enable scrolling
scroll_bar = Scrollbar(root)
scroll_bar.grid(row=1,column=8, rowspan=14,sticky=W )

list_bx.configure(yscrollcommand=scroll_bar.set) # Enables vertical scrolling
scroll_bar.configure(command=list_bx.yview)

scroll_bary = Scrollbar(root, orient=HORIZONTAL)
scroll_bary.grid(row=4,column=1, columnspan=5 , sticky=N)

list_bx.configure(xscrollcommand=scroll_bary.set) # Enables hor scrolling
scroll_bary.configure(command=list_bx.xview)


delete_btn = Button(root, text="Delete Record",bg="red",fg="white",font="helvetica 10 bold",command=delete_records)
delete_btn.grid(row=10, column=5)

view_btn = Button(root, text="View all records",bg="black",fg="white",font="helvetica 10 bold",command=view_records)
view_btn.grid(row=10, column=1)#, sticky=tk.N)

clear_btn = Button(root, text="Clear Screen",bg="maroon",fg="white",font="helvetica 10 bold",command=clear_screen)
clear_btn.grid(row=10, column=2)#, sticky=tk.W)


label_file_explorer = Label(root,
                            text="Choose Netflix Data",
                            width=70, height=1,
                            fg="blue")

button_explore = Button(root,
                        text="Browse Files",
                        command=browseFiles)
label_file_explorer.grid(column=2, row=1)
button_explore.grid(column=2, row=2)
root.mainloop()  # Runs the application until exit


