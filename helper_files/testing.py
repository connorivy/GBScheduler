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

from tkinter import *
from tkinter import ttk
from tkinter import font
from demopanels import MsgPanel, SeeDismissPanel

class ToolbarDemo(ttk.Frame):
    
    def __init__(self, isapp=True, name='toolbardemo'):
        ttk.Frame.__init__(self, name=name)
        self.pack(expand=Y, fill=BOTH)
        self.master.title('Toolbar Demo')
        self.isapp = isapp
        self._create_widgets()
        
    def _create_widgets(self):
        # if self.isapp:    
        #     MsgPanel(self,
        #              ["This is a demonstration of how to do ",
        #               "a toolbar that is styled correctly and which ",
        #               "can be torn off. The buttons are configured ",
        #               "to be 'toolbar style' buttons by ",
        #               "telling them that they are to use the Toolbutton ",
        #               "style. At the left end of the toolbar is a ",
        #               "simple marker, on mouse over, the cursor changes to a ",
        #               "movement icon; drag that away from the ",
        #               "toolbar to tear off the whole toolbar into a ",
        #               "separate toplevel widget. When the dragged-off ",
        #               "toolbar is no longer needed, just close it like ",
        #               "any normal toplevel and it will reattach to the ",
        #               "window it was torn from."])       
        #     SeeDismissPanel(self)
        
        self._create_demo_panel()
        
    def _create_demo_panel(self):
        demoPanel = Frame(self)
        demoPanel.pack(side=TOP, fill=BOTH, expand=Y)
        
        sep = ttk.Separator(demoPanel, orient=HORIZONTAL)
        sep.grid(row=0, column=0, sticky='ew')
        
        # create the toolbar
        self.__tbDocked = True
        self.__tbFloating = None
        self.toolbar = self._add_toolbar(demoPanel)
        self.toolbar.grid(row=1, column=0, sticky='ew')
        
        # create a simple text area
        self.txt = Text(demoPanel, width=40, height=10)
        self.txt.grid(row=2, column=0, sticky='nsew')
        
        # position and set resize behaviour
        demoPanel.rowconfigure(2, weight=1)
        demoPanel.columnconfigure(0, weight=1)
        
    def _add_toolbar(self, parent):
        # add a toolbar (must be in a frame)
        toolbar = Frame(parent)
        
        if self.__tbDocked:
            # only create a tear off if the toolbar is being docked
            tearoff = Frame(toolbar, cursor='fleur', borderwidth=2, relief=RAISED)
            
            # use a label as a 'grip' to tearoff toolbar
            # rather than the vertical scrollbars used in the 
            # original Tcl demo
            self.__gripImg = BitmapImage(file='images\\circles.xbm')
            grip = ttk.Label(tearoff, image=self.__gripImg)
            grip.pack(side=LEFT, fill=Y)   
            tearoff.pack(side=LEFT)
            toolbar.__tearoff = tearoff
            
            # bind the 'tearoff grip' to capture dragging
            grip.bind('<ButtonPress-1>', self._start_tear)
            grip.bind('<ButtonRelease-1>', self._tear_off)
    
        # create the toolbar widgets
        contents = ttk.Frame(toolbar)
        
        btn = ttk.Button(contents, text='Button', style='Demo.Toolbutton',
                         command=lambda: self.txt.insert(END, 'Button pressed.\n'))
        btn.pack(side=LEFT)
        
        cb = ttk.Checkbutton(contents, text='Check', style='Demo.Toolbutton')
        cb['command'] = lambda c=cb: self._say_check(c)
        cb.pack(side=LEFT)
        
        menu = Menu(contents)
        mb = ttk.Menubutton(contents, text='Menu', menu=menu)
        menu.add_command(label='Just', command=lambda: self.txt.insert(END, 'Just\n'))
        menu.add_command(label='An', command=lambda: self.txt.insert(END, 'An\n'))
        menu.add_command(label='Example', command=lambda: self.txt.insert(END, 'Example\n'))
        mb.pack(side=LEFT)
        
        combo = ttk.Combobox(contents, value=sorted(font.families()),
                             state='readonly')      
        combo.bind('<<ComboboxSelected>>', lambda e, v=combo: self._change_font(e, v.get()))  
        combo.pack(side=LEFT)
        
        contents.pack(side=LEFT)
        
        return toolbar
    
    # =========================================================================
    # Bound methods to handle 'toolbar' tear-off
    # =========================================================================
    def _start_tear(self, evt):
        # save mouse press position
        self.__tearX = evt.x
        self.__tearY = evt.y
    
    def _tear_off(self, evt):
        if self.__tbDocked:
            # undock the toolbar
            self.__tbDocked = False
            self.toolbar.grid_remove() # saves orig grid position
            
            # and create another in a new toplevel window
            tp = Toplevel()
            tp.title('Demo Toolbar')
            
            # intercept new toolbar close so we can restore
            # the original toolbar in the app window
            tp.protocol('WM_DELETE_WINDOW', self._restore_toolbar)
            
            # position the new toolbar window
            # at the mouse released position
            dx = evt.x - self.__tearX
            dy = evt.y - self.__tearY
            x = self.toolbar.winfo_rootx() + dx
            y = self.toolbar.winfo_rooty() + dy
            tp.geometry('+{}+{}'.format(x,y))

            # show the window
            self.__tbFloating = self._add_toolbar(tp)
            self.__tbFloating.pack()
            
    def _restore_toolbar(self):
        # destroy the floating toolbar
        self.__tbFloating.master.destroy()
        self.__tbFloating = None
        
        # restore the original toolbar to its
        # original position in the app window
        self.__tbDocked = True
        self.toolbar.grid()

    # =========================================================================
    # Other commands and bound methods
    # =========================================================================
        
    def _say_check(self, check):
        # triggered when the checkbutton is selected/de-selected
        state = int(check.getvar(check['variable']))
        if state == 1: 
            state = 'On' 
        else: 
            state = 'Off'
        
        msg = "Check is {}.\n".format(state)
        self.txt.insert(END, msg)
        
    def _change_font(self, evt, font ):
        # triggered when there is a selection in the Font combobox
        newFont = font.split()  # handle multi-word font names
        newFont = ''.join(newFont)  
        
        self.txt.configure(font=newFont)
        self.txt.focus_set() # pushes font update in text area
        
if __name__ == '__main__':
    ToolbarDemo().mainloop()