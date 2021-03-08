from tkinter import Tk, Canvas, Frame, BOTH, Button, filedialog
from create_spans import is_num
from Classes import VolDiff, RevGB
import copy

from intial_long_rebar_design import add_min_reinf, reinf_for_max_area
from update_rebar import update_req_areas

class GUI(Frame):

    def __init__(self, master, beam_run_info,user_input):
        super().__init__()
        self.initUI(master,beam_run_info,user_input)

    def initUI(self,master,beam_run_info,user_input):
        self.master=master
        pad=3
        self._geom='200x200+0+0'
        self.screenwidth = master.winfo_screenwidth()-pad
        self.screenheight = master.winfo_screenheight()-pad
        self.usable_screenwidth = float(self.screenwidth * .8)
        self.usable_screenheight = float(self.screenheight * .8)
        self.screenwidth_padding = float(self.screenwidth * .1)
        self.screenheight_padding = float(self.screenheight * .1)
        master.geometry("{0}x{1}+0+0".format(self.screenwidth, self.screenheight))
        master.bind('<Escape>',self.toggle_geom)
        self.master.title("beam scheduler")
        self.pack(fill=BOTH, expand=1)
        canvas = Canvas(self)

        self.draw_all_gbs(canvas)
        self.add_browse_btn(canvas)

        # self.add_update_btn(canvas,beam_run_info,user_input)
        # self.add_reset_btn(canvas,beam_run_info,user_input)
        # self.draw_reinf_diagram(canvas,beam_run_info)

        canvas.pack(fill=BOTH, expand=1)

    def toggle_geom(self,event):
        geom=self.master.winfo_geometry()
        print(geom,self._geom)
        self.master.geometry(self._geom)
        self._geom=geom

    def draw_reinf_diagram(self, canvas, beam_run_info):
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
                canvas.create_line(current_span.left_side_on_screen,bot,current_span.left_side_on_screen - self.screenheight * .02, bot + self.screenheight * .03, width=4)
                canvas.create_line(current_span.left_side_on_screen,bot,current_span.left_side_on_screen + self.screenheight * .02, bot + self.screenheight * .03, width=4)

                canvas.create_line(current_span.right_side_on_screen,bot,current_span.right_side_on_screen - self.screenheight * .02, bot + self.screenheight * .03, width=4)
                canvas.create_line(current_span.right_side_on_screen,bot,current_span.right_side_on_screen + self.screenheight * .02, bot + self.screenheight * .03, width=4)

            # draw frame for graph
            canvas.create_rectangle(current_span.left_side_on_screen, top, current_span.right_side_on_screen, bot, outline="#000000")
            # draw centerline
            canvas.create_line(current_span.left_side_on_screen, mid, current_span.right_side_on_screen, mid)

        # draw little lines representing rebar required
        for rebar_req in beam_run_info.original_rebar_req:
            tick_left = self.screenwidth * .1 + spans_length_on_screen * rebar_req[0] / beam_run_info.all_spans_len
            tick_top = mid - (mid - top) * rebar_req[1] / beam_run_info.max_rebar_area
            tick_bot = mid + (mid - top) * rebar_req[2] / beam_run_info.max_rebar_area
            canvas.create_line(tick_left, tick_top, tick_left, tick_bot)

        self.draw_rebar(canvas, beam_run_info, mid)       

    def draw_rebar(self, canvas, beam_run_info, mid):
        length_along_screen = self.screenwidth * .1
        spans_length_on_screen = .8 * self.screenwidth
        half_diagram_height = self.screenheight * .075

        top_rebar_elements = beam_run_info.top_rebar
        top_rebar_elements.sort(key=lambda x: x.a_provided)

        for element in top_rebar_elements:
            x1_dim = length_along_screen + element.start_loc / beam_run_info.all_spans_len * spans_length_on_screen
            x2_dim = length_along_screen + element.end_loc / beam_run_info.all_spans_len * spans_length_on_screen
            y_dim = mid - half_diagram_height * (element.a_provided + element.a_from_smaller)/ beam_run_info.max_rebar_area
            line = canvas.create_line(x1_dim, y_dim, x2_dim, y_dim, width = 4, fill="Black", activefill="Red")
            
            canvas.tag_bind(line, '<ButtonPress-1>', lambda event, element = element: self.on_click(event, element))
            canvas.pack()

            element.drawn = True
            
    def draw_all_gbs(self, canvas):
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

        for gb in rev_gbs:
            print(self.screenwidth_padding, (gb.start_x - min_x) * scale, self.screenwidth_padding + (gb.start_x - min_x) * scale)
            x1_dim = float((gb.start_x - min_x) * scale + self.screenwidth_padding)
            x2_dim = float((gb.end_x - min_x) * scale + self.screenwidth_padding)
            y1_dim = float(self.screenheight - ((gb.start_y - min_y) * scale) - self.screenheight_padding)
            y2_dim = float(self.screenheight - ((gb.end_y - min_y) * scale) - self.screenheight_padding)

            line = canvas.create_line(x1_dim, y1_dim, x2_dim, y2_dim, width = 4, fill="Black", activefill="Red")

            canvas.tag_bind(line, '<ButtonPress-1>', lambda event, gb = gb: self.click_on_plan(event, gb))
            canvas.pack()


    def on_click(self, event, element):
        print('\n\n\n')
        element.get_rebar_info()

    def click_on_plan(self, event, gb):
        print('%f %f' %(gb.start_x, gb.start_y))

    def add_update_btn(self, canvas, beam_run_info, user_input):
        self.update_btn = Button(self, text="UPDATE", command = lambda:self.update(canvas,beam_run_info,user_input))
        self.update_btn.place(relheight = 0.05, relwidth = 0.1, relx = 0.89, rely = 0.01)
        # self.update_btn.pack()

    def add_browse_btn(self, canvas):
        self.browse_button = Button(self, text = "BROWSE", command = lambda:self.fileDialog())
        self.browse_button.place(relheight = 0.05, relwidth = 0.1, relx = 0.89, rely = 0.01)

    def fileDialog(self):
        self.filename = filedialog.askdirectory(initialdir =  "/", title = "Where are you ADAPT runs?")
        print(self.filename)

    def add_reset_btn(self, canvas, beam_run_info, user_input):
        self.update_btn = Button(self, text="RESET", command = lambda:self.reset(canvas,beam_run_info,user_input))
        self.update_btn.place(relheight = 0.05, relwidth = 0.1, relx = 0.89, rely = 0.07)
        # self.update_btn.pack()

    def update(self,canvas,beam_run_info,user_input):
        print('update')
        canvas.delete("all")

        reinf_for_max_area(beam_run_info,user_input)
        update_req_areas(beam_run_info)

        self.draw_reinf_diagram(canvas,beam_run_info)

    def reset(self,canvas,beam_run_info,user_input):
        print('reset')
        canvas.delete("all")

        beam_run_info.top_rebar = []
        beam_run_info.rebar_req = copy.deepcopy(beam_run_info.original_rebar_req)

        add_min_reinf(beam_run_info)
        reinf_for_max_area(beam_run_info,user_input)
        update_req_areas(beam_run_info)

        self.draw_reinf_diagram(canvas,beam_run_info)




