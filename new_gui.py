import tkinter as tk   # python3
from tkinter import Tk, Canvas, Frame, BOTH, Button, filedialog
from Classes import RevGB
import os
#import Tkinter as tk   # python

TITLE_FONT = ("Helvetica", 18, "bold")

class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

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
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F,geometry in zip((StartPage, PageOne, PageTwo), (geom, geom, geom)):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            # store the frame and the geometry for this frame
            self.frames[page_name] = (frame, geometry)

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame, geometry = self.frames[page_name]
        # change geometry of the window
        self.update_idletasks()
        self.geometry(geometry)
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):

        super().__init__()
        tk.Frame.__init__(self, parent)
        self.controller = controller
        # label = tk.Label(self, text="This is the start page", font=TITLE_FONT)
        # label.pack(side="top", fill="x", pady=10)

        # button1 = tk.Button(self, text="Go to Page One",
        # 					command=lambda: controller.show_frame("PageOne"))
        # button2 = tk.Button(self, text="Go to Page Two",
        # 					command=lambda: controller.show_frame("PageTwo"))
        # button1.pack()
        # button2.pack()



        canvas = tk.Canvas(self)

        pad = 3
        self.screenwidth = self.winfo_screenwidth()-pad
        self.screenheight = self.winfo_screenheight()-pad
        self.usable_screenwidth = float(self.screenwidth * .8)
        self.usable_screenheight = float(self.screenheight * .8)
        self.screenwidth_padding = float(self.screenwidth * .1)
        self.screenheight_padding = float(self.screenheight * .1)

        self.draw_all_gbs(canvas)
        self.add_browse_btn(canvas)

        # self.add_update_btn(canvas,beam_run_info,user_input)
        # self.add_reset_btn(canvas,beam_run_info,user_input)
        # self.draw_reinf_diagram(canvas,beam_run_info)

        canvas.pack(fill=tk.BOTH, expand=1)

    def draw_all_gbs(self, canvas):
        path = 'C:/Users/civy/Documents/GitHub/GBScheduler/helper_files/revit_output.txt'
        revit_output = open(path, 'r')
        lines = revit_output.readlines()
        revit_output.close()

        rev_gbs = []
        max_x = -10000000.0
        min_x = 10000000.0
        max_y = -1000000.0
        min_y = 10000000.0

        for line in range(len(lines)):
            rev_gbs.append(RevGB(line, lines[line]))
            
            max_x = max(max_x, rev_gbs[-1].start_x, rev_gbs[-1].end_x)
            min_x = min(min_x, rev_gbs[-1].start_x, rev_gbs[-1].end_x)
            max_y = max(max_y, rev_gbs[-1].start_y, rev_gbs[-1].end_y)
            min_y = min(min_y, rev_gbs[-1].start_y, rev_gbs[-1].end_y)

        scale = min(self.usable_screenwidth / (max_x-min_x), self.usable_screenheight / (max_y - min_y))

        self.gb_lines = []
        for gb in rev_gbs:
            x1_dim = float((gb.start_x - min_x) * scale + self.screenwidth_padding)
            x2_dim = float((gb.end_x - min_x) * scale + self.screenwidth_padding)
            y1_dim = float(self.screenheight - ((gb.start_y - min_y) * scale) - self.screenheight_padding)
            y2_dim = float(self.screenheight - ((gb.end_y - min_y) * scale) - self.screenheight_padding)

        
            gb_line = canvas.create_line(x1_dim, y1_dim, x2_dim, y2_dim, width = 4, fill="Black", activefill="Red", state="disabled")
            print(gb_line)
            self.gb_lines.append(gb_line)

            canvas.tag_bind(gb_line, '<ButtonPress-1>', lambda event, gb = gb, line = line: self.add_to_active_run(event, gb, line))
            canvas.pack()

    def add_browse_btn(self, canvas):
        self.browse_button = Button(self, text = "BROWSE", command = lambda:self.fileDialog(canvas))
        self.browse_button.place(relheight = 0.05, relwidth = 0.1, relx = 0.89, rely = 0.01)

    def add_to_active_run(self, event, gb, line):
        active_flag = 'None'
        for flag in self.run_btn_flags.keys():
            if self.run_btn_flags[flag]:
                active_flag = flag
                break
        if active_flag == 'None':
            print('A line was clicked without an active flag. This shouldnt happen')
        else:
            line.configure(fill='red', tags=flag)
        print('%f %f' %(gb.start_x, gb.start_y))

    def fileDialog(self, canvas):
        self.filename = filedialog.askdirectory(initialdir =  "/", title = "Where are you ADAPT runs?")
        run_names = next(os.walk(self.filename))[1]
        self.beam_run_info_all = {}
        for run in run_names:
            print('hey')
            # self.beam_run_info_all[run] = create_beam_run_obj(self.filename + '/' + run + '/report.xls')

        self.run_btns = {}
        self.run_btn_flags = {}
        self.assign_beams_to_run_flag = False
        for run in range(len(run_names)):
            self.run_btns[run_names[run]] = Button(self, text = run_names[run], command=lambda: self.run_btn_pushed(self.run_btns[run_names[run]]))
            self.run_btns[run_names[run]].place(relheight = 0.05, relwidth = 0.1, relx = 0.89, rely = 0.07 + .06*run)
            self.run_btn_flags[run_names[run]] = False

        btn = Button(self, text = 'Assign Beams to Run', command=lambda: self.assign_beams_to_run(btn))
        btn.place(relheight = 0.05, relwidth = 0.1, relx = 0.78, rely = 0.01)


    def assign_beams_to_run(self, btn):
        self.assign_beams_to_run_flag = not self.assign_beams_to_run_flag
        if self.assign_beams_to_run_flag:
            btn.configure(bg = "red")
        else:
            btn.configure(bg = "SystemButtonFace")
            for key, button in self.run_btns.items():
                button.configure(bg = "SystemButtonFace")
                print(self.gb_lines)
            for line in self.gb_lines:
                print(line)
                line.configure(fill='black')
            for key, flag in self.run_btn_flags.items():
                flag = False

    def run_btn_pushed(self, btn):
        self.run_btn_flags[btn['text']] == True
        if self.assign_beams_to_run_flag:
            btn.configure(bg = "red")
            for line in self.gb_lines:
                if line.tags() == btn['text']:
                    line.configure(fill='red')
        else:
            self.controller.show_frame("PageOne")


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 1", font=TITLE_FONT)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                            command=lambda: controller.show_frame("StartPage"))
        button.pack()


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 2", font=TITLE_FONT)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                            command=lambda: controller.show_frame("StartPage"))
        button.pack()


if __name__ == "__main__":
    # root = tk.Tk()
    app = SampleApp()
    app.mainloop()