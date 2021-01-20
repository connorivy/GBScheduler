import tkinter as tk
from screeninfo import get_monitors

def create_window():
    root = tk.Tk()
    # label = tk.Label(text="Python rocks!")
    # label.pack()
    root.geometry()

    root.mainloop()
    print(get_curr_screen_geometry)

def get_curr_screen_geometry():
    for m in get_monitors():
        
        print(str(m))

get_curr_screen_geometry()