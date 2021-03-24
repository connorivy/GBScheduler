from tkinter import Tk, Canvas, Frame, BOTH, Button, filedialog
from Classes import RevGB
import os

class PlanView(Frame):

    def __init__(self, parent, controller):

        super().__init__()
        Frame.__init__(self, parent)
        self.controller = controller
        self.canvas = Canvas(self)

        pad = 3
        self.screenwidth = self.winfo_screenwidth()-pad
        self.screenheight = self.winfo_screenheight()-pad
        self.usable_screenwidth = float(self.screenwidth * .8)
        self.usable_screenheight = float(self.screenheight * .8)
        self.screenwidth_padding = float(self.screenwidth * .1)
        self.screenheight_padding = float(self.screenheight * .1)

        self.draw_all_gbs()
        self.add_browse_btn()
        self.canvas.pack(fill=BOTH, expand=1)

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
            frame = self.controller.get_page('ReinfDiagram')
            frame.setup_when_clicked()

            self.controller.show_frame("ReinfDiagram")

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