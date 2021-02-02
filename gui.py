from tkinter import Tk, Canvas, Frame, BOTH
from create_spans import is_num
from Classes import VirtualSingleSpan

class GUI(Frame):

    def __init__(self, master, spans):
        super().__init__()
        self.initUI(master, spans)

    def initUI(self,master,spans):
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
        virt_spans = self.draw_beam(canvas,spans)
        # self.draw_rebar(canvas,spans,virt_spans)
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
        virt_spans = []
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
            left_side = length_along_screen
            top_side = self.screenheight * .6
            right_side = left_side + current_span.virt_length
            # bot_side = self.screenheight * current_span.virt_depth
            bot_side = self.screenheight * virt_depth
            # get ready for next span by changing the length across screen to the right side
            length_along_screen = right_side

            if is_num(current_span.number):
                canvas.create_line(left_side,bot_side,left_side - self.screenheight * .02, bot_side + self.screenheight * .03, width=4)
                canvas.create_line(left_side,bot_side,left_side + self.screenheight * .02, bot_side + self.screenheight * .03, width=4)

                canvas.create_line(right_side,bot_side,right_side - self.screenheight * .02, bot_side + self.screenheight * .03, width=4)
                canvas.create_line(right_side,bot_side,right_side + self.screenheight * .02, bot_side + self.screenheight * .03, width=4)

            # draw frame for graph
            canvas.create_rectangle(left_side, top_side, right_side, bot_side, outline="#000000")
            # draw centerline
            mid_height = (top_side + bot_side) / 2
            canvas.create_line(left_side, mid_height, right_side, mid_height)

            # draw little lines representing rebar required
            for pair in current_span.original_top_rebar_req:
                canvas.create_line(left_side + pair[0] * current_span.virt_length, mid_height - (bot_side-top_side) / 2 * pair[1] / max_rebar_area, left_side + pair[0] * current_span.virt_length, mid_height)
            for pair in current_span.original_bot_rebar_req:
                canvas.create_line(left_side + pair[0] * current_span.virt_length, mid_height + (bot_side-top_side) / 2 * pair[1] / max_rebar_area, left_side + pair[0] * current_span.virt_length, mid_height)



        return virt_spans

    # def draw_rebar(self, canvas, spans, virt_spans):
    #     for num_current_span in len(spans):
    #         top_rebar_elements = spans[num_current_span].top_rebar_elements
    #         for element in top_rebar_elements:



