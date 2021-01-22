from tkinter import Tk, Canvas, Frame, BOTH
from create_spans import is_num

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
        for current_span in spans:
            spans_length_irl += current_span.length
            deepest_beam = max(deepest_beam, current_span.depth)

        for current_span in spans:
            current_span.virt_length = current_span.length * spans_length_on_screen / spans_length_irl
            current_span.virt_depth = .55 + .07 * current_span.depth / deepest_beam
            left_side = length_along_screen
            top_side = self.screenheight * .55
            right_side = left_side + current_span.virt_length
            bot_side = self.screenheight * current_span.virt_depth

            if is_num(current_span.number):
                canvas.create_line(left_side,bot_side,left_side - self.screenheight * .02, bot_side + self.screenheight * .03, width=4)
                canvas.create_line(left_side,bot_side,left_side + self.screenheight * .02, bot_side + self.screenheight * .03, width=4)

                canvas.create_line(right_side,bot_side,right_side - self.screenheight * .02, bot_side + self.screenheight * .03, width=4)
                canvas.create_line(right_side,bot_side,right_side + self.screenheight * .02, bot_side + self.screenheight * .03, width=4)

            canvas.create_rectangle(left_side, top_side, right_side, bot_side, outline="#000000", fill="#000000")
            length_along_screen = right_side


def main():
    root = Tk()
    gui = GUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()