# from tkinter import *

# ws = Tk()
# ws.title('PythonGuides')
# ws.geometry('500x400')
# ws.config(bg='grey')

# canvas = Canvas(
#     ws,
#     height=300,
#     width=400,
#     bg="#fff",
#     )

# canvas.pack()

# canvas.create_rectangle(
#     30, 20, 200, 100,
#     fill="red", 
#     tags="rect",
#     )

# canvas.create_oval(
#     150, 150, 50, 50,
#     fill="blue",
#     tag="circ"
#     )

# canvas.create_rectangle(
#     150, 50, 250, 150,
#     fill="grey",
#     tag="squa"
#     )

# canvas.create_text(
#     180, 250,
#     font= "Times 20",
#     text="Squre,Circle & Rectangle \n inside the canvas",
#     tag='txt'
#     )

# btn1 = Button(
#     ws,
#     text='del_rect',
#     font="Times 12",
#     command=lambda:canvas.delete("rect")
#     )
 
# btn1.pack(side=LEFT, fill=X, expand=True)

# btn2 = Button(
#     ws,
#     text='del_squ',
#     font="Times 12",
#     command=lambda:canvas.delete("squa")
#     )
 
# btn2.pack(side=LEFT, fill=X, expand=True)

# btn3 = Button(
#     ws,
#     text='del_circ',
#     font="Times 12",
#     command=lambda:canvas.delete("circ")
#     )
 
# btn3.pack(side=LEFT, fill=X, expand=True)

# btn4 = Button(
#     ws,
#     text='del_all',
#     font="Times 12",
#     command=lambda:canvas.delete("all")
#     )
 
# btn4.pack(side=LEFT, fill=X, expand=True)


# ws.mainloop()














# from tkinter import * 

# def onObjectClick(event):                  
#     print('Clicked', event.x, event.y, event.widget)
#     print(event.widget.find_closest(event.x, event.y)) 

# root = Tk()
# canv = Canvas(root, width=100, height=100)
# obj1 = canv.create_text(50, 30, text='Click me one')
# obj2 = canv.create_text(50, 70, text='Click me two')

# canv.tag_bind(obj1, '<Double-1>', onObjectClick)        
# canv.tag_bind(obj2, '<Double-1>', onObjectClick)        
# canv.pack()
# root.mainloop()















# import tkinter 
# from tkinter import *

# root = Tk() 

# L = Label(root, text ="Right-click to display menu", 
# 		width = 40, height = 20) 
# L.pack() 

# m = Menu(root, tearoff = 0) 
# m.add_command(label ="Cut") 
# m.add_command(label ="Copy") 
# m.add_command(label ="Paste") 
# m.add_command(label ="Reload") 
# m.add_separator() 
# m.add_command(label ="Rename") 

# def do_popup(event): 
# 	try: 
# 		m.tk_popup(event.x_root, event.y_root) 
# 	finally: 
# 		m.grab_release() 

# L.bind("<Button-3>", do_popup) 

# mainloop() 














# Import all files from
# tkinter and overwrite
# all the tkinter files
# by tkinter.ttk
from tkinter import *
from tkinter.ttk import *

# creates tkinter window or root window
root = Tk()
root.geometry('200x100')

# function to be called when mouse enters in a frame
def enter(event):
	print('Button-2 pressed at x = % d, y = % d'%(event.x, event.y))

# function to be called when when mouse exits the frame
def exit_(event):
	print('Button-3 pressed at x = % d, y = % d'%(event.x, event.y))

# frame with fixed geomerty
frame1 = Frame(root, height = 100, width = 200)

# these lines are showing the
# working of bind function
# it is universal widget method
frame1.bind('<Enter>', enter)
frame1.bind('<Leave>', exit_)

frame1.pack()

mainloop()
