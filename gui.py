from tkinter import Tk, Canvas, Frame, BOTH, Button
from create_spans import is_num
import copy

from intial_long_rebar_design import add_min_reinf, reinf_for_max_area
from update_rebar import update_req_areas

class GUI(Frame):

    def __init__(self, master, spans,user_input):
        super().__init__()
        self.initUI(master, spans,user_input)

    def initUI(self,master,spans, user_input):
        self.master=master
        pad=3
        self._geom='200x200+0+0'
        self.screenwidth = master.winfo_screenwidth()-pad
        self.screenheight = master.winfo_screenheight()-pad
        master.geometry("{0}x{1}+0+0".format(self.screenwidth, self.screenheight))
        master.bind('<Escape>',self.toggle_geom)

        self.master.title("beam scheduler")
        self.pack(fill=BOTH, expand=1)
        canvas = Canvas(self)

        self.add_update_btn(canvas,spans,user_input)
        self.add_reset_btn(canvas,spans,user_input)
        self.draw_beam(canvas,spans)

        canvas.pack(fill=BOTH, expand=1)

    def toggle_geom(self,event):
        geom=self.master.winfo_geometry()
        print(geom,self._geom)
        self.master.geometry(self._geom)
        self._geom=geom

    def draw_beam(self, canvas, spans):
        spans_length_irl = 0
        spans_length_on_screen = .8 * self.screenwidth
        length_along_screen = self.screenwidth * .1
        deepest_beam = 0
        max_rebar_area = 0
        for current_span in spans:
            spans_length_irl += current_span.length
            deepest_beam = max(deepest_beam, current_span.depth)

            for pair in current_span.original_top_rebar_req:
                max_rebar_area = max(max_rebar_area, pair[1])
            for pair in current_span.original_bot_rebar_req:
                max_rebar_area = max(max_rebar_area, pair[1])

        for current_span in spans:
            current_span.virt_length = current_span.length * spans_length_on_screen / spans_length_irl
            # current_span.virt_depth = .6 + .15 * current_span.depth / deepest_beam
            virt_depth = .6 + .15
            current_span.left_side_on_screen = length_along_screen
            current_span.top_side_on_screen = self.screenheight * .6
            current_span.right_side_on_screen = current_span.left_side_on_screen + current_span.virt_length
            # current_span.bot_side_on_screen = self.screenheight * current_span.virt_depth
            current_span.bot_side_on_screen = self.screenheight * virt_depth
            # get ready for next span by changing the length across screen to the right side
            length_along_screen = current_span.right_side_on_screen

            if is_num(current_span.number):
                # draw beam supports
                canvas.create_line(current_span.left_side_on_screen,current_span.bot_side_on_screen,current_span.left_side_on_screen - self.screenheight * .02, current_span.bot_side_on_screen + self.screenheight * .03, width=4)
                canvas.create_line(current_span.left_side_on_screen,current_span.bot_side_on_screen,current_span.left_side_on_screen + self.screenheight * .02, current_span.bot_side_on_screen + self.screenheight * .03, width=4)

                canvas.create_line(current_span.right_side_on_screen,current_span.bot_side_on_screen,current_span.right_side_on_screen - self.screenheight * .02, current_span.bot_side_on_screen + self.screenheight * .03, width=4)
                canvas.create_line(current_span.right_side_on_screen,current_span.bot_side_on_screen,current_span.right_side_on_screen + self.screenheight * .02, current_span.bot_side_on_screen + self.screenheight * .03, width=4)

            # draw frame for graph
            canvas.create_rectangle(current_span.left_side_on_screen, current_span.top_side_on_screen, current_span.right_side_on_screen, current_span.bot_side_on_screen, outline="#000000")
            # draw centerline
            current_span.mid_height = (current_span.top_side_on_screen + current_span.bot_side_on_screen) / 2
            current_span.beam_height = (current_span.bot_side_on_screen - current_span.top_side_on_screen) / 2
            canvas.create_line(current_span.left_side_on_screen, current_span.mid_height, current_span.right_side_on_screen, current_span.mid_height)

            # draw little lines representing rebar required
            for pair in current_span.original_top_rebar_req:
                canvas.create_line(current_span.left_side_on_screen + pair[0] * current_span.virt_length, current_span.mid_height - current_span.beam_height * pair[1] / max_rebar_area, current_span.left_side_on_screen + pair[0] * current_span.virt_length, current_span.mid_height)
            for pair in current_span.original_bot_rebar_req:
                canvas.create_line(current_span.left_side_on_screen + pair[0] * current_span.virt_length, current_span.mid_height + current_span.beam_height * pair[1] / max_rebar_area, current_span.left_side_on_screen + pair[0] * current_span.virt_length, current_span.mid_height)   

            self.draw_rebar(canvas, current_span, max_rebar_area)       

    def draw_rebar(self, canvas, cs, max_rebar_area):
        top_rebar_elements = cs.top_rebar_elements
        for element in top_rebar_elements:
            x1_dim = cs.left_side_on_screen + element.start_loc * cs.virt_length
            x2_dim = cs.left_side_on_screen + element.end_loc * cs.virt_length
            y_dim = cs.mid_height - cs.beam_height * element.a_provided / max_rebar_area
            canvas.create_line(x1_dim, y_dim, x2_dim, y_dim, width = 3)

    def add_update_btn(self, canvas, spans, user_input):
        self.update_btn = Button(self, text="UPDATE", command = lambda:self.update(canvas,spans,user_input))
        self.update_btn.place(relheight = 0.05, relwidth = 0.1, relx = 0.89, rely = 0.01)
        # self.update_btn.pack()

    def add_reset_btn(self, canvas, spans, user_input):
        self.update_btn = Button(self, text="RESET", command = lambda:self.reset(canvas,spans,user_input))
        self.update_btn.place(relheight = 0.05, relwidth = 0.1, relx = 0.89, rely = 0.07)
        # self.update_btn.pack()

    def update(self,canvas,spans,user_input):
        canvas.delete("all")

        reinf_for_max_area(spans,user_input)
        update_req_areas(spans)

        self.draw_beam(canvas,spans)

    def reset(self,canvas,spans,user_input):
        canvas.delete("all")

        for x in spans:
            x.top_rebar_elements = []
            x.top_rebar_req = copy.deepcopy(x.original_top_rebar_req)

        add_min_reinf(spans)
        self.draw_beam(canvas,spans)




