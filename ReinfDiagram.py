from tkinter import Tk, Canvas, Frame, BOTH, Button, filedialog
from Classes import BeamRunInfo, ParametersDefinedByUser
from create_spans import define_spans, define_long_rebar, is_num
from intial_long_rebar_design import add_min_reinf, reinf_for_max_area
from update_rebar import assign_from_bar_schedule, update_req_areas

import xlrd
import copy

class ReinfDiagram(Frame):

    def __init__(self, parent, controller):
        super().__init__()
        Frame.__init__(self, parent)

        pad = 3
        self.screenwidth = self.winfo_screenwidth()-pad
        self.screenheight = self.winfo_screenheight()-pad
        self.usable_screenwidth = float(self.screenwidth * .8)
        self.usable_screenheight = float(self.screenheight * .8)
        self.screenwidth_padding = float(self.screenwidth * .1)
        self.screenheight_padding = float(self.screenheight * .1)
        self.controller = controller
        self.canvas = Canvas(self)


    def setup_when_clicked(self):
        file = self.controller.shared_data['directory'] + '/' + self.controller.shared_data['current_file'] + '/' + 'report.xls'
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

            self.create_back_btn(beam_run_info)
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
            print(current_span.left_side_on_screen, top, current_span.right_side_on_screen, bot)
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

    def create_back_btn(self, beam_run_info):
        btn = Button(self, text = 'Back', command=lambda: self.back_to_plan_view(beam_run_info))
        # button = tk.Button(self, text="Go to the start page",
        #                     command=lambda: self.controller.show_frame("PlanView"))
        btn.place(relheight = 0.05, relwidth = 0.1, relx = 0.02, rely = 0.01)

    def back_to_plan_view(self, beam_run_info):
        print('leave page')
        self.canvas.delete("all")

        beam_run_info.top_rebar = []
        beam_run_info.rebar_req = copy.deepcopy(beam_run_info.original_rebar_req)

        self.controller.show_frame("PlanView")