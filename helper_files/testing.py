from tkinter import *

ws = Tk()
ws.title('PythonGuides')
ws.geometry('500x400')
ws.config(bg='grey')

canvas = Canvas(
    ws,
    height=300,
    width=400,
    bg="#fff",
    )

canvas.pack()

canvas.create_rectangle(
    30, 20, 200, 100,
    fill="red", 
    tags="rect",
    )

canvas.create_oval(
    150, 150, 50, 50,
    fill="blue",
    tag="circ"
    )

canvas.create_rectangle(
    150, 50, 250, 150,
    fill="grey",
    tag="squa"
    )

canvas.create_text(
    180, 250,
    font= "Times 20",
    text="Squre,Circle & Rectangle \n inside the canvas",
    tag='txt'
    )

btn1 = Button(
    ws,
    text='del_rect',
    font="Times 12",
    command=lambda:canvas.delete("rect")
    )
 
btn1.pack(side=LEFT, fill=X, expand=True)

btn2 = Button(
    ws,
    text='del_squ',
    font="Times 12",
    command=lambda:canvas.delete("squa")
    )
 
btn2.pack(side=LEFT, fill=X, expand=True)

btn3 = Button(
    ws,
    text='del_circ',
    font="Times 12",
    command=lambda:canvas.delete("circ")
    )
 
btn3.pack(side=LEFT, fill=X, expand=True)

btn4 = Button(
    ws,
    text='del_all',
    font="Times 12",
    command=lambda:canvas.delete("all")
    )
 
btn4.pack(side=LEFT, fill=X, expand=True)


ws.mainloop()