# from tkinter import *

# class App:
#     def __init__(self, root):
#         self.entry = []
#         self.sv = []
#         self.root = root
#         self.canvas = Canvas(self.root, background="#ffffff", borderwidth=0)
#         self.frame = Frame(self.canvas, background="#ffffff")
#         self.scrolly = Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
#         self.scrollx = Scrollbar(self.root, orient="horizontal", command=self.canvas.xview)
#         self.canvas.configure(yscrollcommand=self.scrolly.set)#, xscrollcommand=self.scrollx.set)
#         self.canvas.create_window((4,4), window=self.frame, anchor="nw", tags="self.frame")
#         self.scrolly.pack(side="left", fill="y")
#         self.canvas.pack(side="top", fill="both", expand=True)
#         self.scrollx.pack(side="bottom", fill="x")
#         self.frame.bind("<Configure>", self.onFrameConfigure)
#         for i in range(15):
#             self.entry.append([])
#             self.sv.append([])
#             for c in range(30):
#                 self.sv[i].append(StringVar())
#                 self.sv[i][c].trace("w", lambda name, index, mode, sv=self.sv[i][c], i=i, c=c: self.callback(sv, i, c))
#                 self.entry[i].append(Entry(self.frame, textvariable=self.sv[i][c]).grid(row=c, column=i))
#     def onFrameConfigure(self, event):
#         self.canvas.configure(scrollregion=self.canvas.bbox("all"))
#     def callback(self, sv, column, row):
#         print("Column: "+str(column)+", Row: "+str(row)+" = "+sv.get())

# root = Tk()
# App(root)
# root.mainloop()


from tkinter import *
from tkinter import ttk

ws = Tk()
ws.title("PythonGuides")


frame = Frame(ws)
frame.pack(pady=20)

tv = ttk.Treeview(frame, columns=(1,2,3,4,5,6,7,8,9,10,11), height=8, show='tree')
tv.pack(side=LEFT)

sb = Scrollbar(frame, orient=VERTICAL)
sb.pack(side=RIGHT, fill=Y)

tv.config(yscrollcommand=sb.set)
sb.config(command=tv.yview)

def update_item():
    selected = tv.focus()
    temp = tv.item(selected, 'values')
    sal_up = float(temp[2]) + float(temp[2]) * 0.05
    tv.item(selected, values=(temp[0], temp[1], sal_up))

tv.column("#0",minwidth=0,width=50)
tv.insert(parent='', index=0, iid=0, values=("vineet", "e11", 1000000.00))
tv.insert(parent='', index=1, iid=1, values=("anil", "e12", 120000.00))
tv.insert(parent='', index=2, iid=2, values=("ankit", "e13", 41000.00))
tv.insert(parent='', index=3, iid=3, values=("Shanti", "e14", 22000.00))
tv.insert(parent='', index=4, iid=4, values=("vineet", "e11", 1000000.00))
tv.insert(parent='', index=5, iid=5, values=("anil", "e12", 120000.00))
tv.insert(parent='', index=6, iid=6, values=("ankit", "e13", 41000.00))
tv.insert(parent='', index=7, iid=7, values=("Shanti", "e14", 22000.00))
tv.insert(parent='', index=8, iid=8, values=("vineet", "e11", 1000000.00))
tv.insert(parent='', index=9, iid=9, values=("anil", "e12", 120000.00))
tv.insert(parent='', index=10, iid=10, values=("ankit", "e13", 41000.00))
tv.insert(parent='', index=11, iid=11, values=("Shanti", "e14", 22000.00))

Button(
    ws, 
    text='Increment Salary', 
    command=update_item, 
    padx=20, 
    pady=10, 
    bg='#081947', 
    fg='#fff', 
    font=('Times BOLD', 12)
    ).pack(pady=10)

style = ttk.Style()
style.theme_use("default")
style.map("Treeview")

ws.mainloop()



# import tkinter as tk


# class TestFrame(tk.Frame):
#     def __init__(self):
#         super().__init__()
#         list_of_options = ["first option", "second option", "third option", "forth option"]
#         first_option = tk.StringVar(self)
#         first_option.set(list_of_options[0])

#         tk.Label(self, text="Test Label 1").grid(row=0, column=0)
#         tk.Entry(self, bd=5).grid(row=0, column=1)
#         tk.Label(self, text="Test Label 2").grid(row=0, column=2)
#         tk.Entry(self, bd=5).grid(row=0, column=3)
#         tk.Label(self, text="Test check button 1").grid(row=2, column=0)
#         tk.Checkbutton(self, bd=5).grid(row=2, column=1)
#         tk.Label(self, text="Test check button 2").grid(row=2, column=2)
#         tk.Checkbutton(self, bd=5).grid(row=2, column=3)
#         tk.Label(self, text="Test drop down 1").grid(row=3, column=0)
#         tk.OptionMenu(self, first_option, *list_of_options).grid(row=3, column=1)


# class TestMainApplication(tk.Tk):
#     def __init__(self):
#         super().__init__()
#         self.title("Test Application")

#         for r in range(3):
#             self.rowconfigure(r, weight=1)
#         for c in range(8):
#             self.columnconfigure(c, weight=1)

#         self.testFrame1 = TestFrame()
#         self.testFrame2 = TestFrame()
#         self.testFrame3 = TestFrame()
#         self.testFrame4 = TestFrame()
#         self.testFrame1.grid(row=0, column=0, rowspan=3, columnspan=3, sticky='nsew')
#         self.testFrame2.grid(row=3, column=0, rowspan=3, columnspan=3, sticky='nsew')
#         self.testFrame3.grid(row=0, column=3, rowspan=2, columnspan=3, sticky='nsew')
#         self.testFrame3.grid(row=2, column=3, rowspan=4, columnspan=3, sticky='nsew')


# TestMainApplication().mainloop()



# from tkinter import *
# from pandastable import Table, TableModel

# class TestApp(Frame):
#         """Basic test frame for the table"""
#         def __init__(self, parent=None):
#             self.parent = parent
#             Frame.__init__(self)
#             self.main = self.master
#             self.main.geometry('600x400+200+100')
#             self.main.title('Table app')
#             f = Frame(self.main)
#             f.pack(fill=BOTH,expand=1)
#             df = TableModel.getSampleData()
#             self.table = pt = Table(f, dataframe=df,
#                                     showtoolbar=True, showstatusbar=True)
#             pt.show()
#             return

# app = TestApp()
# #launch the app
# app.mainloop()


# import tkinter as tk
# from tkinter import ttk
# from tkinter import scrolledtext
 
 
# def exit_qk():
#     obj.quit()
#     obj.destroy()
#     exit()
 
 
# # obj of Tkinter
# obj = tk.Tk()
# obj.geometry("500x200+50+50")
# obj.resizable(0, 0) # switch off resizable
 
 
# # create menu bar
# menu_bar = tk.Menu(obj)
# obj.config(menu=menu_bar)
# # add item to menu bar
# file_menu = tk.Menu(menu_bar, tearoff=0) # create file menu
# # add file-menu to menu bar with label
# menu_bar.add_cascade(label="File", menu=file_menu)
# # add commands to File menu
# file_menu.add_command(label="New") # add new to file menu
# file_menu.add_command(label="Open")
# file_menu.add_command(label="Save")
# file_menu.add_separator()
# file_menu.add_command(label="Exit", command=exit_qk)
 
# help_menu = tk.Menu(menu_bar, tearoff=0) # create help menu
# # add help-menu to menu bar with label
# menu_bar.add_cascade(label="Help", menu=help_menu)
# # add commands to File menu
# help_menu.add_command(label="Help") # add new to help menu
# help_menu.add_separator()
# help_menu.add_command(label="Credits") # add new to help menu
# help_menu.add_command(label="About")
 
# obj.mainloop()
