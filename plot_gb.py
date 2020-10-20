import tkinter as tk

def draw_beam():
    window = tk.Tk()
    window.mainloop()

def get_curr_screen_geometry():
    """
    Workaround to get the size of the current screen in a multi-screen setup.

    Returns:
        geometry (str): The standard Tk geometry string.
            [width]x[height]+[left]+[top]
    """
    root = tk.Tk()
    root.update_idletasks()
    root.attributes('-fullscreen', True)
    root.state('iconic')
    geometry = root.winfo_geometry()
    # root.destroy()
    print(geometry)
    return geometry

get_curr_screen_geometry()
# draw_beam()