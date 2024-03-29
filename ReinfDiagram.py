from tkinter import Canvas, Frame, BOTH, Button, FLAT, LEFT, StringVar, TOP, ttk, Scrollbar, VERTICAL, CENTER, font, Toplevel, Label, ttk, Entry, END
from tkinter.constants import DISABLED
from Classes import BeamRunInfo, ParametersDefinedByUser
from create_spans import define_spans, define_long_rebar, is_num
from intial_long_rebar_design import add_min_reinf, reinf_for_max_area
from update_rebar import assign_from_bar_schedule, update_req_areas
from schedule_rebar import schedule_rebar
from write_to_excel import write_to_excel

import xlrd
import copy

class ReinfDiagram(Frame):

    def __init__(self, parent, controller):
        super().__init__()
        Frame.__init__(self, parent)

        pad = 0
        self.controller = controller
        self.controller.screenwidth = self.winfo_screenwidth()-pad
        self.screenheight = self.winfo_screenheight()-pad
        # self.usable_screenwidth =       float(self.controller.screenwidth * .8)
        # self.usable_screenheight =      float(self.screenheight * .92)
        # self.controller.screenwidth_padding =      float(self.controller.screenwidth * .05)
        # self.screenheight_padding =     float(self.screenheight * .05)

        self.toolbar_x0 = 0
        self.toolbar_y0 = 0
        self.toolbar_width = 1
        self.toolbar_height = .08

        self.diagram_x0 = .05
        self.diagram_y0 = .7
        self.diagram_width = .8
        self.diagram_height = .15

        self.top_of_sched_x0 = .05
        self.top_of_sched_y0 = self.toolbar_height + .01
        self.controller.top_of_sched_width = .8
        self.top_of_sched_height = .20

        self.table_x0 = .05
        self.table_y0 = self.top_of_sched_y0 + self.top_of_sched_height + .02
        self.table_width = .8 + .015
        self.table_height = .3

        self.controller = controller
        self.canvas = Canvas(self)


    def setup_when_clicked(self):
        # print(self.controller.all_beam_runs.keys())
        file = self.controller.shared_data['current_file']
        beam_run_info = self.controller.all_beam_runs[file]
        beam_run_info.get_top_rebar_info()
        user_input = self.controller.user_input
        # print(file)

        self.draw_reinf_diag_toolbar(beam_run_info, user_input)

        table_params = [self.table_width, self.table_height, self.table_x0, self.table_y0]
        
        self.draw_top_of_sched()
        self.table = PageTwo(self, self.controller, table_params[0], table_params[1], table_params[2], table_params[3])
        # self.table.place(relwidth = self.usable_screenwidth, relheight = 0.5 * self.usable_screenheight, relx = 0.1, rely = 0.2)
        # self.create_back_btn(beam_run_info)
        # self.add_update_btn(beam_run_info,user_input)
        # self.add_reset_btn(beam_run_info,user_input)
        # self.add_sched_btn(beam_run_info)
        self.draw_reinf_diagram(beam_run_info)

        # self.table = PageTwo(self, self.controller)
        # self.table.place(relwidth = 0.8, relheight = 0.5, relx = 0.1, rely = 0.2)

        self.canvas.place(relwidth = 1, relheight = 1, relx = 0, rely = 0)

    def draw_reinf_diagram(self, beam_run_info):

        spans_length_on_screen = self.diagram_width * self.controller.screenwidth
        length_along_screen = self.diagram_x0 * self.controller.screenwidth

        top = self.diagram_y0 * self.screenheight
        bot = top + self.diagram_height * self.screenheight
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

            # add GB label
            helv20 = font.Font(size=20)
            self.canvas.create_text(current_span.left_side_on_screen + .5 * current_span.virt_length, bot + .02 * self.screenheight, text = 'GB' + str(current_span.sched_num), justify = CENTER, font = helv20)

            # # draw frame for graph
            # print(current_span.left_side_on_screen, top, current_span.right_side_on_screen, bot)
            self.canvas.create_rectangle(current_span.left_side_on_screen, top, current_span.right_side_on_screen, bot, outline="#000000")
            # draw centerline
            self.canvas.create_line(current_span.left_side_on_screen, mid, current_span.right_side_on_screen, mid)

        # draw little lines representing rebar required
        for rebar_req in beam_run_info.original_rebar_req:
            tick_left = self.diagram_x0 * self.controller.screenwidth + spans_length_on_screen * rebar_req[0] / beam_run_info.all_spans_len
            tick_top = mid - (mid - top) * rebar_req[1] / beam_run_info.max_rebar_area
            tick_bot = mid + (mid - top) * rebar_req[2] / beam_run_info.max_rebar_area
            self.canvas.create_line(tick_left, tick_top, tick_left, tick_bot)

        self.draw_rebar(beam_run_info, mid)       

    def draw_rebar(self, beam_run_info, mid):
        length_along_screen = self.diagram_x0 * self.controller.screenwidth
        spans_length_on_screen = self.diagram_width * self.controller.screenwidth
        half_diagram_height = self.diagram_height * self.screenheight * .5

        top_rebar_elements = beam_run_info.top_rebar
        bot_rebar_elements = beam_run_info.bot_rebar

        top_rebar_elements.sort(key=lambda x: x.a_provided)
        bot_rebar_elements.sort(key=lambda x: x.a_provided)

        for element in top_rebar_elements:
            x1_dim = length_along_screen + element.start_loc / beam_run_info.all_spans_len * spans_length_on_screen
            x2_dim = length_along_screen + element.end_loc / beam_run_info.all_spans_len * spans_length_on_screen
            y_dim = mid - half_diagram_height * (element.a_provided + element.a_from_smaller)/ beam_run_info.max_rebar_area
            line = self.canvas.create_line(x1_dim, y_dim, x2_dim, y_dim, width = 4, fill="Black", activefill="Red")
            
            self.canvas.tag_bind(line, '<ButtonPress-1>', lambda event, element = element: self.disp_rebar_info(event, element))
            self.canvas.place()

            element.drawn = True

        for element in bot_rebar_elements:
            x1_dim = length_along_screen + element.start_loc / beam_run_info.all_spans_len * spans_length_on_screen
            x2_dim = length_along_screen + element.end_loc / beam_run_info.all_spans_len * spans_length_on_screen
            y_dim = mid + half_diagram_height * (element.a_provided + element.a_from_smaller)/ beam_run_info.max_rebar_area
            line = self.canvas.create_line(x1_dim, y_dim, x2_dim, y_dim, width = 4, fill="Black", activefill="Red")
            
            self.canvas.tag_bind(line, '<ButtonPress-1>', lambda event, element = element: self.disp_rebar_info(event, element))
            self.canvas.place()

            element.drawn = True

    def disp_rebar_info(self, event, element):
        win = Toplevel()
        win.wm_title("Rebar Info")

        # Make topLevelWindow remain on top until destroyed, or attribute changes.
        win.attributes('-topmost', 'true')

        l1 = ttk.Label(win, text="Size").grid(row=0, column=0)
        bar_size = StringVar(win, value = element.bar_size)
        e1 = Entry(win, textvariable = bar_size, state='normal').grid(row=0, column=1)

        l2 = Label(win, text="Quantity").grid(row=1, column=0)
        num_bars = StringVar(win, value = element.num_bars)
        e2 = Entry(win, textvariable = num_bars , state='normal').grid(row=1, column=1)


        l3 = Label(win, text="Start Location").grid(row=2, column=0)
        start_loc = StringVar(win, value = element.start_loc)
        e3 = Entry(win, textvariable=start_loc, state='normal').grid(row=2, column=1)

        l4 = Label(win, text="End Location").grid(row=3, column=0)
        end_loc = StringVar(win, value = element.end_loc)
        e4 = Entry(win, textvariable=end_loc, state='normal').grid(row=3, column=1)

        b = ttk.Button(win, text="Save", command=win.destroy)
        b.grid(row=4, column=0)

    # def add_reset_btn(self, beam_run_info, user_input):
    #     self.update_btn = Button(self, text="RESET", command = lambda:self.reset(beam_run_info,user_input))
    #     self.update_btn.place(relheight = 0.05, relwidth = 0.1, relx = 0.89, rely = 0.07)
    #     # self.update_btn.pack()

    # def add_update_btn(self, beam_run_info, user_input):
    #     self.update_btn = Button(self, text="UPDATE", command = lambda:self.update_reinf_diagram(beam_run_info,user_input))
    #     self.update_btn.place(relheight = 0.05, relwidth = 0.1, relx = 0.89, rely = 0.01)
    #     # self.update_btn.pack()

    def update_reinf_diagram(self,beam_run_info,user_input):
        self.canvas.delete("all")

        reinf_for_max_area(beam_run_info,user_input)
        beam_run_info.top_rebar_designed = update_req_areas(beam_run_info)

        self.draw_reinf_diagram(beam_run_info)

    def reset(self,beam_run_info,user_input):
        self.canvas.delete("all")

        beam_run_info.top_rebar = []
        beam_run_info.rebar_req = copy.deepcopy(beam_run_info.original_rebar_req)

        add_min_reinf(beam_run_info)
        reinf_for_max_area(beam_run_info,user_input)
        beam_run_info.top_rebar_designed = update_req_areas(beam_run_info)

        self.draw_reinf_diagram(beam_run_info)

    # def create_back_btn(self, beam_run_info):
    #     btn = Button(self, text = 'Back', command=lambda: self.back_to_plan_view(beam_run_info))
    #     # button = tk.Button(self, text="Go to the start page",
    #     #                     command=lambda: self.controller.show_frame("PlanView"))
    #     btn.place(relheight = 0.05, relwidth = 0.1, relx = 0.02, rely = 0.01)

    def back_to_plan_view(self, beam_run_info):
        self.canvas.delete("all")

        beam_run_info.top_rebar = []
        beam_run_info.rebar_req = copy.deepcopy(beam_run_info.original_rebar_req)

        self.controller.show_frame("PlanView")

    # def add_sched_btn(self, beam_run_info):
    #     btn = Button(self, text = 'SCHEDULE REBAR', command=lambda: self.add_rebar_to_global_schedule(beam_run_info))
    #     btn.place(relheight = 0.05, relwidth = 0.1, relx = 0.89, rely = 0.13)

    def add_rebar_to_global_schedule(self,beam_run_info):
        values = schedule_rebar(beam_run_info)
        self.controller.show_frame("PageTwo")
        write_to_excel(values)

    def draw_reinf_diag_toolbar(self, beam_run_info, user_input):
        self.toolbar = Frame(self, bg = 'dark gray')
        self.toolbar.place(relheight = self.toolbar_height, relwidth = self.toolbar_width, relx = 0, rely = 0)

        b1 = Button(
        self.toolbar,
        relief=FLAT,
        compound = LEFT,
        text="Back",
        command= lambda: self.back_to_plan_view(beam_run_info))
        b1.place(relheight = .9, relwidth = 0.05, relx = .005, rely = 0.05)

        b2 = Button(
        self.toolbar,
        relief=FLAT,
        compound = LEFT,
        text="Update",
        command= lambda: self.update_reinf_diagram(beam_run_info,user_input))
        b2.place(relheight = .9, relwidth = 0.05, relx = .06, rely = 0.05)

        b3 = Button(
        self.toolbar,
        relief=FLAT,
        compound = LEFT,
        text="Reset",
        command= lambda: self.reset(beam_run_info,user_input))
        b3.place(relheight = .9, relwidth = 0.05, relx = .115, rely = 0.05)

        b4 = Button(
        self.toolbar,
        relief=FLAT,
        compound = LEFT,
        text="Schedule",
        command= lambda: self.add_rebar_to_global_schedule(beam_run_info))
        b4.place(relheight = .9, relwidth = 0.05, relx = .17, rely = 0.05)

    def draw_top_of_sched(self):
        x0 = self.top_of_sched_x0 * self.controller.screenwidth
        y0 = self.top_of_sched_y0 * self.screenheight
        width = self.controller.top_of_sched_width * self.controller.screenwidth
        height = self.top_of_sched_height * self.screenheight

        col_width = width / 16
        top_len = .4 * height
        bot_len = height - top_len

        helv36 = font.Font(size=36, weight='bold')
        helv20 = font.Font(size=20)


        # border starting with left vertical and going clockwise
        self.canvas.create_line(x0, y0, x0, y0 + height)
        self.canvas.create_line(x0, y0, x0 + width, y0)
        self.canvas.create_line(x0 + width, y0, x0 + width, y0 + height)
        self.canvas.create_line(x0, y0 + height, x0 + width, y0 + height)
        # middle line
        self.canvas.create_line(x0, y0 + top_len, x0 + width, y0 + top_len)
        # first 3 dividing lines
        self.canvas.create_line(x0 + 1 * col_width, y0 + top_len, x0 + 1 * col_width, y0 + height)
        self.canvas.create_line(x0 + 2 * col_width, y0 + top_len, x0 + 2 * col_width, y0 + height)
        self.canvas.create_line(x0 + 3 * col_width, y0 + top_len, x0 + 3 * col_width, y0 + height)
        # 3/4 down horizontal line
        self.canvas.create_line(x0 + 3 * col_width, y0 + top_len + bot_len / 2, x0 + 15 * col_width, y0 + top_len + bot_len / 2)
        # next three (half sized) dividing lines
        self.canvas.create_line(x0 + 5 * col_width, y0 + top_len + bot_len / 2, x0 + 5 * col_width, y0 + height)
        self.canvas.create_line(x0 + 7 * col_width, y0 + top_len + bot_len / 2, x0 + 7 * col_width, y0 + height)
        self.canvas.create_line(x0 + 9 * col_width, y0 + top_len + bot_len / 2, x0 + 9 * col_width, y0 + height)
        # next half sized line
        self.canvas.create_line(x0 + 11 * col_width, y0 + top_len, x0 + 11 * col_width, y0 + height)
        # last 2 quarter length lines
        self.canvas.create_line(x0 + 12 * col_width, y0 + top_len + bot_len / 2, x0 + 12 * col_width, y0 + height)
        self.canvas.create_line(x0 + 13 * col_width, y0 + top_len + bot_len / 2, x0 + 13 * col_width, y0 + height)
        # last half sized line
        self.canvas.create_line(x0 + 15 * col_width, y0 + top_len, x0 + 15 * col_width, y0 + height)

        self.canvas.create_text(x0 + width/2, y0 + top_len / 2, text = "CONCRETE GRADE BEAM SCHEDULE", justify = CENTER, font=helv36)
        self.canvas.create_text(x0 + 7 * col_width, y0 + top_len + bot_len / 4, text = "MILD REINFORCING", justify = CENTER, font=helv20)
        self.canvas.create_text(x0 + 13 * col_width, y0 + top_len + bot_len / 4, text = "STIRRUPS", justify = CENTER, font=helv20)
        self.canvas.create_text(x0 + col_width / 2, y0 + top_len + bot_len / 2, text = "MARK", justify = CENTER)
        self.canvas.create_text(x0 + 1 * col_width + col_width / 2, y0 + top_len + bot_len / 2, text = "WIDTH\n(IN.)", justify = CENTER)
        self.canvas.create_text(x0 + 2 * col_width + col_width / 2, y0 + top_len + bot_len / 2, text = "DEPTH\n(IN.)", justify = CENTER)
        self.canvas.create_text(x0 + 15 * col_width + col_width / 2, y0 + top_len + bot_len / 2, text = "SPECIAL\nNOTES", justify = CENTER)
        self.canvas.create_text(x0 + 4 * col_width, y0 + top_len + bot_len * 3/4, text = "LEFT END\nTOP BARS", justify = CENTER)
        self.canvas.create_text(x0 + 6 * col_width, y0 + top_len + bot_len * 3/4, text = "CENTER\nBOTTOM BARS", justify = CENTER)
        self.canvas.create_text(x0 + 8 * col_width, y0 + top_len + bot_len * 3/4, text = "CENTER\nTOP BARS", justify = CENTER)
        self.canvas.create_text(x0 + 10 * col_width, y0 + top_len + bot_len * 3/4, text = "RIGHT END\nTOP BARS", justify = CENTER)
        self.canvas.create_text(x0 + 11 * col_width + col_width / 2, y0 + top_len + bot_len * 3/4, text = "SIZE", justify = CENTER)
        self.canvas.create_text(x0 + 12 * col_width + col_width / 2, y0 + top_len + bot_len * 3/4, text = "TYPE", justify = CENTER)
        self.canvas.create_text(x0 + 14 * col_width, y0 + top_len + bot_len * 3/4, text = "SPACING\nEACH END", justify = CENTER)

class PageTwo(Frame):

    def __init__(self, parent, controller, width, height, x, y):
        super().__init__()
        Frame.__init__(self, parent)
        self.controller = controller

        col_width = int((self.controller.top_of_sched_width * self.controller.screenwidth) / 16)
        cols = [1,2,3,4,5,6,7,8,9,10,11]
        
        f = Frame(self.master, bg = 'pink')
        f.place(relwidth = width, relheight = height, relx = x, rely = y)

        tv = ttk.Treeview(f, columns=cols, show="tree")
        tv.place(relwidth = 1, relheight = 1, relx = 0, rely = 0)

        sb = Scrollbar(f, orient=VERTICAL)
        sb.place(relwidth = .015, relheight = 1, relx = .985, rely = 0)

        tv.config(yscrollcommand=sb.set)
        sb.config(command=tv.yview)

        for i in cols:
            tv.heading(column=f'{i}',text=f'{i}',anchor='w')
            if 3 < i < 8 or i == 10:
                tv.column(column=f'{i}', width=2*col_width, stretch=False, anchor='center')
            else:
                tv.column(column=f'{i}', width=col_width, stretch=False, anchor='center')

        tv.column('#0', stretch=False, minwidth=0, width=0)

        for key, item in self.controller.schedule_entries.items():
            item.insert(0,key)
            if key % 2:
                tv.insert(parent='', index=key, values=item, tags=['oddrow'])
            else:
                tv.insert(parent='', index=key, values=item)
                
        tv.tag_configure('oddrow', background = 'gray')
        # tv.tag_configure('oddrow', background = 'dark gray')

        style = ttk.Style()
        style.theme_use("default")
        style.map("Treeview")



# class PageTwo(Frame):
#     """Basic test frame for the table"""
#     def __init__(self, parent=None):
#         self.parent = parent
#         Frame.__init__(self)
#         self.main = self.master
#         self.main.geometry("{0}x{1}+0+0".format(self.controller.screenwidth, self.screenheight))
#         self.main.title('Table app')
#         f = Frame(self.main)
#         f.pack(fill=BOTH,expand=1)
#         df = TableModel.getSampleData()
#         self.table = pt = Table(f, dataframe=df,
#                                 showtoolbar=True, showstatusbar=True)
#         pt.show()
#         return