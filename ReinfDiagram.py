from tkinter import Tk, Canvas, Frame, BOTH, Button, filedialog, Label, FLAT, LEFT, ttk, Scrollbar, VERTICAL, RIGHT, Y
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

        pad = 3
        self.screenwidth = self.winfo_screenwidth()-pad
        self.screenheight = self.winfo_screenheight()-pad
        # self.usable_screenwidth =       float(self.screenwidth * .8)
        # self.usable_screenheight =      float(self.screenheight * .92)
        # self.screenwidth_padding =      float(self.screenwidth * .05)
        # self.screenheight_padding =     float(self.screenheight * .05)

        self.toolbar_x0 = 0
        self.toolbar_y0 = 0
        self.toolbar_width = 1
        self.toolbar_height = .08

        self.diagram_x0 = .05
        self.diagram_y0 = .6
        self.diagram_width = .8
        self.diagram_height = .15

        self.top_of_sched_x0 = .05
        self.top_of_sched_y0 = self.toolbar_height + .01
        self.top_of_sched_width = .8
        self.top_of_sched_height = .15

        self.table_x0 = .05
        self.table_y0 = self.top_of_sched_y0 + self.top_of_sched_height
        self.table_width = .8
        self.table_height = .3

        self.controller = controller
        self.canvas = Canvas(self)


    def setup_when_clicked(self):
        file = self.controller.shared_data['directory'] + '/' + self.controller.shared_data['current_file'] + '/' + 'report.xls'
        print(file)
        if self.controller.shared_data['directory']:
            wb = xlrd.open_workbook(file)
            beam_run_info = BeamRunInfo()
            
            beam_run_info.spans, beam_run_info.all_spans_len = define_spans(wb)

            # create user input and use it to define stuff (specifically min num bars)
            user_input = ParametersDefinedByUser(fc = 4000, fy = 60000)
            for span in beam_run_info.spans:
                span.get_min_num_bars(user_input)

            define_long_rebar(wb, beam_run_info)  
            add_min_reinf(beam_run_info)
            reinf_for_max_area(beam_run_info,user_input)
            assign_from_bar_schedule(beam_run_info)
            update_req_areas(beam_run_info)

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

        spans_length_on_screen = self.diagram_width * self.screenwidth
        length_along_screen = self.diagram_x0 * self.screenwidth

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

            # # draw frame for graph
            # print(current_span.left_side_on_screen, top, current_span.right_side_on_screen, bot)
            self.canvas.create_rectangle(current_span.left_side_on_screen, top, current_span.right_side_on_screen, bot, outline="#000000")
            # draw centerline
            self.canvas.create_line(current_span.left_side_on_screen, mid, current_span.right_side_on_screen, mid)

        # draw little lines representing rebar required
        for rebar_req in beam_run_info.original_rebar_req:
            tick_left = self.diagram_x0 * self.screenwidth + spans_length_on_screen * rebar_req[0] / beam_run_info.all_spans_len
            tick_top = mid - (mid - top) * rebar_req[1] / beam_run_info.max_rebar_area
            tick_bot = mid + (mid - top) * rebar_req[2] / beam_run_info.max_rebar_area
            self.canvas.create_line(tick_left, tick_top, tick_left, tick_bot)

        self.draw_rebar(beam_run_info, mid)       

    def draw_rebar(self, beam_run_info, mid):
        length_along_screen = self.diagram_x0 * self.screenwidth
        spans_length_on_screen = self.diagram_width * self.screenwidth
        half_diagram_height = self.diagram_height * self.screenheight * .5

        top_rebar_elements = beam_run_info.top_rebar
        top_rebar_elements.sort(key=lambda x: x.a_provided)

        for element in top_rebar_elements:
            x1_dim = length_along_screen + element.start_loc / beam_run_info.all_spans_len * spans_length_on_screen
            x2_dim = length_along_screen + element.end_loc / beam_run_info.all_spans_len * spans_length_on_screen
            y_dim = mid - half_diagram_height * (element.a_provided + element.a_from_smaller)/ beam_run_info.max_rebar_area
            line = self.canvas.create_line(x1_dim, y_dim, x2_dim, y_dim, width = 4, fill="Black", activefill="Red")
            
            self.canvas.tag_bind(line, '<ButtonPress-1>', lambda event, element = element: self.on_click(event, element))
            self.canvas.place()

            element.drawn = True

    def on_click(self, event, element):
        print('\n\n\n')
        element.get_rebar_info()

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
        update_req_areas(beam_run_info)

        self.draw_reinf_diagram(beam_run_info)

    def reset(self,beam_run_info,user_input):
        self.canvas.delete("all")

        beam_run_info.top_rebar = []
        beam_run_info.rebar_req = copy.deepcopy(beam_run_info.original_rebar_req)

        add_min_reinf(beam_run_info)
        reinf_for_max_area(beam_run_info,user_input)
        update_req_areas(beam_run_info)

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
        command= lambda: lambda:self.reset(beam_run_info,user_input))
        b3.place(relheight = .9, relwidth = 0.05, relx = .115, rely = 0.05)

        b4 = Button(
        self.toolbar,
        relief=FLAT,
        compound = LEFT,
        text="Schedule",
        command= lambda: lambda:self.add_rebar_to_global_schedule(beam_run_info))
        b4.place(relheight = .9, relwidth = 0.05, relx = .17, rely = 0.05)

    def draw_top_of_sched(self):
        x0 = self.top_of_sched_x0 * self.screenwidth
        y0 = self.top_of_sched_y0 * self.screenheight
        width = self.top_of_sched_width * self.screenwidth
        height = self.top_of_sched_height * self.screenheight

        col_width = width / 16


        # border starting with left vertical and going clockwise
        self.canvas.create_line(x0, y0, x0, y0 + height)
        self.canvas.create_line(x0, y0, x0 + width, y0)
        self.canvas.create_line(x0 + width, y0, x0 + width, y0 + height)
        self.canvas.create_line(x0, y0 + height, x0 + width, y0 + height)
        # middle line
        self.canvas.create_line(x0, y0 + height/2, x0 + width, y0 + height/2)
        # first 3 dividing lines
        self.canvas.create_line(x0 + 1 * col_width, y0 + height/2, x0 + 1 * col_width, y0 + height)
        self.canvas.create_line(x0 + 2 * col_width, y0 + height/2, x0 + 2 * col_width, y0 + height)
        self.canvas.create_line(x0 + 3 * col_width, y0 + height/2, x0 + 3 * col_width, y0 + height)
        # 3/4 down horizontal line
        self.canvas.create_line(x0 + 3 * col_width, y0 + 3 * height / 4, x0 + 15 * col_width, y0 + 3 * height / 4)
        # next three (half sized) dividing lines
        self.canvas.create_line(x0 + 5 * col_width, y0 + 3 * height / 4, x0 + 5 * col_width, y0 + height)
        self.canvas.create_line(x0 + 7 * col_width, y0 + 3 * height / 4, x0 + 7 * col_width, y0 + height)
        self.canvas.create_line(x0 + 9 * col_width, y0 + 3 * height / 4, x0 + 9 * col_width, y0 + height)
        # next half sized line
        self.canvas.create_line(x0 + 11 * col_width, y0 + height / 2, x0 + 11 * col_width, y0 + height)
        # last 2 quarter length lines
        self.canvas.create_line(x0 + 12 * col_width, y0 + 3 * height / 4, x0 + 12 * col_width, y0 + height)
        self.canvas.create_line(x0 + 13 * col_width, y0 + 3 * height / 4, x0 + 13 * col_width, y0 + height)
        # last half sized line
        self.canvas.create_line(x0 + 15 * col_width, y0 + 3 * height / 4, x0 + 15 * col_width, y0 + height)

from pandastable import Table, TableModel
import pandas
import openpyxl

class PageTwo(Frame):

    def __init__(self, parent, controller, width, height, x, y):
        super().__init__()
        Frame.__init__(self, parent)
        self.controller = controller
        
        f = Frame(self.master)
        f.place(relwidth = width, relheight = height, relx = x, rely = y)

        tv = ttk.Treeview(f, columns=(1,2,3,4,5,6,7,8,9,10,11), show='tree')
        tv.pack(side=LEFT)

        sb = Scrollbar(f, orient=VERTICAL)
        sb.pack(side=RIGHT, fill=Y)

        tv.config(yscrollcommand=sb.set)
        sb.config(command=tv.yview)


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

    def update_item(tv):
            selected = tv.focus()
            temp = tv.item(selected, 'values')
            sal_up = float(temp[2]) + float(temp[2]) * 0.05
            tv.item(selected, values=(temp[0], temp[1], sal_up))



# class PageTwo(Frame):
#     """Basic test frame for the table"""
#     def __init__(self, parent=None):
#         self.parent = parent
#         Frame.__init__(self)
#         self.main = self.master
#         self.main.geometry("{0}x{1}+0+0".format(self.screenwidth, self.screenheight))
#         self.main.title('Table app')
#         f = Frame(self.main)
#         f.pack(fill=BOTH,expand=1)
#         df = TableModel.getSampleData()
#         self.table = pt = Table(f, dataframe=df,
#                                 showtoolbar=True, showstatusbar=True)
#         pt.show()
#         return