import tkinter as tk
from tkinter import Tk, Canvas, Frame, BOTH, Button, filedialog
import xlrd
import copy
import os
from PlanView import PlanView
from ReinfDiagram import ReinfDiagram

from Classes import BeamRunInfo, RevGB
from create_spans import define_spans, define_long_rebar, is_num
from intial_long_rebar_design import add_min_reinf, reinf_for_max_area
from update_rebar import assign_from_bar_schedule, update_req_areas


TITLE_FONT = ("Helvetica", 18, "bold")

class GUI(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.shared_data = {
            'directory'     : '',
            'current_file'  : ''
        }

        pad = 3
        self.screenwidth = self.winfo_screenwidth()-pad
        self.screenheight = self.winfo_screenheight()-pad
        self.usable_screenwidth = float(self.screenwidth * .8)
        self.usable_screenheight = float(self.screenheight * .8)
        self.screenwidth_padding = float(self.screenwidth * .1)
        self.screenheight_padding = float(self.screenheight * .1)

        geom = "{0}x{1}+0+0".format(self.screenwidth, self.screenheight)

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F,geometry in zip((PlanView, ReinfDiagram, PageTwo), (geom, geom, geom)):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            # store the frame and the geometry for this frame
            self.frames[page_name] = (frame, geometry)

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("PlanView")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        if page_name not in self.frames:
            self.frames[page_name] 
        frame, geometry = self.frames[page_name]
        # change geometry of the window
        self.update_idletasks()
        self.geometry(geometry)
        frame.tkraise()

    def get_page(self, page_name):
        frame, geometry = self.frames[page_name]
        return frame


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 2", font=TITLE_FONT)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                            command=lambda: controller.show_frame("PlanView"))
        button.pack()


if __name__ == "__main__":
    # root = tk.Tk()
    app = GUI()
    app.mainloop()