

# from tkinter import *
# from tkinter import ttk

# ws = Tk()
# ws.title("PythonGuides")


# frame = Frame(ws)
# frame.pack(pady=20)

# tv = ttk.Treeview(frame, columns=(1,2,3,4,5,6,7,8,9,10,11), height=8, show='tree')
# tv.pack(side=LEFT)

# sb = Scrollbar(frame, orient=VERTICAL)
# sb.pack(side=RIGHT, fill=Y)

# tv.config(yscrollcommand=sb.set)
# sb.config(command=tv.yview)

# def update_item():
#     selected = tv.focus()
#     temp = tv.item(selected, 'values')
#     sal_up = float(temp[2]) + float(temp[2]) * 0.05
#     tv.item(selected, values=(temp[0], temp[1], sal_up))

# tv.column("#0",minwidth=0,width=50)
# tv.insert(parent='', index=0, iid=0, values=("vineet", "e11", 1000000.00))
# tv.insert(parent='', index=1, iid=1, values=("anil", "e12", 120000.00))
# tv.insert(parent='', index=2, iid=2, values=("ankit", "e13", 41000.00))
# tv.insert(parent='', index=3, iid=3, values=("Shanti", "e14", 22000.00))
# tv.insert(parent='', index=4, iid=4, values=("vineet", "e11", 1000000.00))
# tv.insert(parent='', index=5, iid=5, values=("anil", "e12", 120000.00))
# tv.insert(parent='', index=6, iid=6, values=("ankit", "e13", 41000.00))
# tv.insert(parent='', index=7, iid=7, values=("Shanti", "e14", 22000.00))
# tv.insert(parent='', index=8, iid=8, values=("vineet", "e11", 1000000.00))
# tv.insert(parent='', index=9, iid=9, values=("anil", "e12", 120000.00))
# tv.insert(parent='', index=10, iid=10, values=("ankit", "e13", 41000.00))
# tv.insert(parent='', index=11, iid=11, values=("Shanti", "e14", 22000.00))

# Button(
#     ws, 
#     text='Increment Salary', 
#     command=update_item, 
#     padx=20, 
#     pady=10, 
#     bg='#081947', 
#     fg='#fff', 
#     font=('Times BOLD', 12)
#     ).pack(pady=10)

# style = ttk.Style()
# style.theme_use("default")
# style.map("Treeview")

# ws.mainloop()


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

import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo

def popup_bonus():
    win = tk.Toplevel()
    win.wm_title("Window")

    # Make topLevelWindow remain on top until destroyed, or attribute changes.
    win.attributes('-topmost', 'true')

    l = tk.Label(win, text="Input")
    l.grid(row=0, column=0)

    b = ttk.Button(win, text="Okay", command=win.destroy)
    b.grid(row=1, column=0)

def popup_showinfo():
    showinfo("Window", "Hello World!")

class Application(ttk.Frame):

    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        self.pack()

        self.button_bonus = ttk.Button(self, text="Bonuses", command=popup_bonus)
        self.button_bonus.pack()

        self.button_showinfo = ttk.Button(self, text="Show Info", command=popup_showinfo)
        self.button_showinfo.pack()

root = tk.Tk()

app = Application(root)

root.mainloop()