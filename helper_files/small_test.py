from tkinter import *
from tkinter import ttk

frame = Frame()

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

style = ttk.Style()
style.theme_use("default")
style.map("Treeview")
