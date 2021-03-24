import tkinter as tk   # python3
from tkinter import Tk, Canvas, Frame, BOTH, Button, filedialog
import xlrd
import copy
import os

from Classes import ParametersDefinedByUser, BeamRunInfo, RevGB
from create_spans import define_spans, define_long_rebar, is_num
from intial_long_rebar_design import add_min_reinf, reinf_for_max_area
from update_rebar import assign_from_bar_schedule, update_req_areas


TITLE_FONT = ("Helvetica", 18, "bold")

class SampleApp(tk.Tk):

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
        for F,geometry in zip((StartPage, PageOne, PageTwo), (geom, geom, geom)):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            # store the frame and the geometry for this frame
            self.frames[page_name] = (frame, geometry)

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        print('show_frame')
        '''Show a frame for the given page name'''
        if page_name not in self.frames:
            self.frames[page_name] 
        frame, geometry = self.frames[page_name]
        # change geometry of the window
        self.update_idletasks()
        self.geometry(geometry)
        frame.tkraise()

    def update_frame(self, page_name):
        frame, geometry = self.frames[page_name]
        frame.__init__(parent=self.container, controller=self)

    def get_page(self, page_name):
        frame, geometry = self.frames[page_name]
        return frame

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



        self.canvas = tk.Canvas(self)

        pad = 3
        self.screenwidth = self.winfo_screenwidth()-pad
        self.screenheight = self.winfo_screenheight()-pad
        self.usable_screenwidth = float(self.screenwidth * .8)
        self.usable_screenheight = float(self.screenheight * .8)
        self.screenwidth_padding = float(self.screenwidth * .1)
        self.screenheight_padding = float(self.screenheight * .1)

        self.draw_all_gbs()
        self.add_browse_btn()

        # self.add_update_btn(canvas,beam_run_info,user_input)
        # self.add_reset_btn(canvas,beam_run_info,user_input)
        # self.draw_reinf_diagram(canvas,beam_run_info)

        self.canvas.pack(fill=tk.BOTH, expand=1)

    def draw_all_gbs(self):
        path = 'helper_files/revit_output.txt'
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

    
            gb_line = self.canvas.create_line(x1_dim, y1_dim, x2_dim, y2_dim, width = 4, fill="Black", activefill="Red", state="disabled")
            self.gb_lines.append(gb_line)

            self.canvas.tag_bind(gb_line, '<ButtonPress-1>', lambda event, gb = gb, gb_line = gb_line: self.add_to_active_run(event, gb, gb_line))
            self.canvas.pack()

    def add_browse_btn(self):
        self.browse_button = Button(self, text = "BROWSE", command = lambda:self.fileDialog())
        self.browse_button.place(relheight = 0.05, relwidth = 0.1, relx = 0.89, rely = 0.01)

    def add_to_active_run(self, event, gb, gb_line):
        active_flag = 'None'
        for flag in self.run_btn_flags.keys():
            if self.run_btn_flags[flag]:
                active_flag = flag
                break
        if active_flag == 'None':
            print('A line was clicked without an active flag. This shouldnt happen')
        else:
            self.canvas.itemconfig(gb_line, fill='blue', tags=flag)
        print('%f %f' %(gb.start_x, gb.start_y))

    def fileDialog(self):
        # get the directory of all the gb runs
        self.filename = filedialog.askdirectory(initialdir =  "/", title = "Where are you ADAPT runs?")
        # save the directory of the runs in the controller
        self.controller.shared_data['directory'] = self.filename
        # get name of all folders in directory
        run_names = next(os.walk(self.filename))[1]
        self.beam_run_info_all = {}
        for run in run_names:
            print('hey')
            # self.beam_run_info_all[run] = create_beam_run_obj(self.filename + '/' + run + '/report.xls')

        self.run_btns = {}
        self.run_btn_flags = {}
        self.assign_beams_to_run_flag = False
        for run in range(len(run_names)):
            self.run_btns[run_names[run]] = Button(self, text = run_names[run], command=lambda run_name = run_names[run]: self.run_btn_pushed(self.run_btns[run_name]))
            self.run_btns[run_names[run]].place(relheight = 0.05, relwidth = 0.1, relx = 0.89, rely = 0.07 + .06*run)
            self.run_btn_flags[run_names[run]] = False

        btn = Button(self, text = 'Assign Beams to Run', command=lambda: self.assign_beams_to_run(btn))
        btn.place(relheight = 0.05, relwidth = 0.1, relx = 0.785, rely = 0.01)


    def assign_beams_to_run(self, btn):
        self.assign_beams_to_run_flag = not self.assign_beams_to_run_flag
        if self.assign_beams_to_run_flag:
            btn.configure(bg = "red")
        
        else:
            self.reset_gb_plan()

            # change assign beams btn color back
            btn.configure(bg = "SystemButtonFace")

            # disable all lines
            for line in self.gb_lines:
                self.canvas.itemconfig(line, state='disabled')

    def run_btn_pushed(self, btn):
        # if that button is already flagged, reset everything and turn off the flag
        if self.run_btn_flags[btn['text']]:
            self.reset_gb_plan()
            self.run_btn_flags[btn['text']] = False

        # if assign beams to run flag is true, flag this btn, change color of all beams belonging to this run
        elif self.assign_beams_to_run_flag:
            self.reset_gb_plan()
            # enable lines
            for line in self.gb_lines:
                self.canvas.itemconfig(line, state='normal')

            self.run_btn_flags[btn['text']] = True
            btn.configure(bg = "blue")
            for line in self.gb_lines:
                tags = self.canvas.gettags(line)
                if tags:
                    if tags[0] == btn['text']:
                        self.canvas.itemconfig(line, fill='blue')
        else:
            self.controller.shared_data['current_file'] = btn['text']
            frame = self.controller.get_page('PageOne')
            frame.setup_when_clicked()

            self.controller.show_frame("PageOne")

    def reset_gb_plan(self):
        # change lines back to black
        for line in self.gb_lines:
            self.canvas.itemconfig(line, fill='black')

        # change beam run colors back
        for key, button in self.run_btns.items():
            button.configure(bg = "SystemButtonFace")

        # turn all run btn flags to false
        for key in self.run_btn_flags.keys():
            self.run_btn_flags[key] = False

        # disable lines
        for line in self.gb_lines:
                self.canvas.itemconfig(line, state='disabled')

class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__()
        tk.Frame.__init__(self, parent)

        pad = 3
        self.screenwidth = self.winfo_screenwidth()-pad
        self.screenheight = self.winfo_screenheight()-pad
        self.usable_screenwidth = float(self.screenwidth * .8)
        self.usable_screenheight = float(self.screenheight * .8)
        self.screenwidth_padding = float(self.screenwidth * .1)
        self.screenheight_padding = float(self.screenheight * .1)
        self.controller = controller

        # self.setup_when_clicked()


        label = tk.Label(self, text="This is page 1", font=TITLE_FONT)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                            command=lambda: controller.show_frame("StartPage"))
        button.pack()

    def setup_when_clicked(self):
        file = self.controller.shared_data['directory'] + '/' + self.controller.shared_data['current_file'] + '/' + 'report2.xls'
        print(file)
        if self.controller.shared_data['directory']:
            wb = xlrd.open_workbook(file)
            beam_run_info = BeamRunInfo()
            user_input = ParametersDefinedByUser(4000, 60000, 1, 1, 1)
            beam_run_info.spans, beam_run_info.max_beam_depth, beam_run_info.all_spans_len = define_spans(wb)
            define_long_rebar(wb, beam_run_info)  
            add_min_reinf(beam_run_info)
            reinf_for_max_area(beam_run_info,user_input)
            assign_from_bar_schedule(beam_run_info)
            update_req_areas(beam_run_info)

            self.canvas = Canvas(self)
            self.add_update_btn(beam_run_info,user_input)
            self.add_reset_btn(beam_run_info,user_input)
            self.draw_reinf_diagram(beam_run_info)

            self.canvas.pack(fill=BOTH, expand=1)

    def draw_reinf_diagram(self, beam_run_info):
        print('draw_reinf_diag')
        spans_length_on_screen = .8 * self.screenwidth
        length_along_screen = self.screenwidth * .1

        virt_depth = .15
        top = self.screenheight * .6
        bot = top + self.screenheight * virt_depth
        mid = (top + bot) / 2

        for current_span in beam_run_info.spans:
            current_span.virt_length = current_span.length * spans_length_on_screen / beam_run_info.all_spans_len

            current_span.left_side_on_screen = length_along_screen
            current_span.right_side_on_screen = current_span.left_side_on_screen + current_span.virt_length

            # get ready for next span by changing the length across screen to the right side
            length_along_screen = current_span.right_side_on_screen

            if is_num(current_span.number):
                # draw beam supports
                self.canvas.create_line(current_span.left_side_on_screen,bot,current_span.left_side_on_screen - self.screenheight * .02, bot + self.screenheight * .03, width=4)
                self.canvas.create_line(current_span.left_side_on_screen,bot,current_span.left_side_on_screen + self.screenheight * .02, bot + self.screenheight * .03, width=4)

                self.canvas.create_line(current_span.right_side_on_screen,bot,current_span.right_side_on_screen - self.screenheight * .02, bot + self.screenheight * .03, width=4)
                self.canvas.create_line(current_span.right_side_on_screen,bot,current_span.right_side_on_screen + self.screenheight * .02, bot + self.screenheight * .03, width=4)

            # draw frame for graph
            self.canvas.create_rectangle(current_span.left_side_on_screen, top, current_span.right_side_on_screen, bot, outline="#000000")
            # draw centerline
            self.canvas.create_line(current_span.left_side_on_screen, mid, current_span.right_side_on_screen, mid)

        # draw little lines representing rebar required
        for rebar_req in beam_run_info.original_rebar_req:
            tick_left = self.screenwidth * .1 + spans_length_on_screen * rebar_req[0] / beam_run_info.all_spans_len
            tick_top = mid - (mid - top) * rebar_req[1] / beam_run_info.max_rebar_area
            tick_bot = mid + (mid - top) * rebar_req[2] / beam_run_info.max_rebar_area
            self.canvas.create_line(tick_left, tick_top, tick_left, tick_bot)

        self.draw_rebar(beam_run_info, mid)       

    def draw_rebar(self, beam_run_info, mid):
        length_along_screen = self.screenwidth * .1
        spans_length_on_screen = .8 * self.screenwidth
        half_diagram_height = self.screenheight * .075

        top_rebar_elements = beam_run_info.top_rebar
        top_rebar_elements.sort(key=lambda x: x.a_provided)

        for element in top_rebar_elements:
            x1_dim = length_along_screen + element.start_loc / beam_run_info.all_spans_len * spans_length_on_screen
            x2_dim = length_along_screen + element.end_loc / beam_run_info.all_spans_len * spans_length_on_screen
            y_dim = mid - half_diagram_height * (element.a_provided + element.a_from_smaller)/ beam_run_info.max_rebar_area
            line = self.canvas.create_line(x1_dim, y_dim, x2_dim, y_dim, width = 4, fill="Black", activefill="Red")
            
            self.canvas.tag_bind(line, '<ButtonPress-1>', lambda event, element = element: self.on_click(event, element))
            self.canvas.pack()

            element.drawn = True

    def on_click(self, event, element):
        print('\n\n\n')
        element.get_rebar_info()

    def add_reset_btn(self, beam_run_info, user_input):
        self.update_btn = Button(self, text="RESET", command = lambda:self.reset(beam_run_info,user_input))
        self.update_btn.place(relheight = 0.05, relwidth = 0.1, relx = 0.89, rely = 0.07)
        # self.update_btn.pack()

    def add_update_btn(self, beam_run_info, user_input):
        self.update_btn = Button(self, text="UPDATE", command = lambda:self.update_reinf_diagram(beam_run_info,user_input))
        self.update_btn.place(relheight = 0.05, relwidth = 0.1, relx = 0.89, rely = 0.01)
        # self.update_btn.pack()

    def update_reinf_diagram(self,beam_run_info,user_input):
        print('update_reinf_diagram')
        self.canvas.delete("all")

        reinf_for_max_area(beam_run_info,user_input)
        update_req_areas(beam_run_info)

        self.draw_reinf_diagram(beam_run_info)

    def reset(self,beam_run_info,user_input):
        print('reset')
        self.canvas.delete("all")

        beam_run_info.top_rebar = []
        beam_run_info.rebar_req = copy.deepcopy(beam_run_info.original_rebar_req)

        add_min_reinf(beam_run_info)
        reinf_for_max_area(beam_run_info,user_input)
        update_req_areas(beam_run_info)

        self.draw_reinf_diagram(beam_run_info)


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