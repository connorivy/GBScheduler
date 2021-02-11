from openpyxl import Workbook
import xlrd
import openpyxl
from tkinter import Tk, Canvas, Frame, BOTH, Button
import inspect

from Classes import ParamatersDefinedByUser
from Classes import RebarElement
from create_spans import define_spans
from create_spans import define_long_rebar
from create_spans import finalize_spans
from gui import GUI
from intial_long_rebar_design import add_min_reinf, reinf_for_max_area, update_req_areas
# from update_rebar import assign_from_bar_schedule

def lineno():
    """Returns the current line number in our program."""
    return inspect.currentframe().f_back.f_lineno
    
def main():
    file = "helper_files/report - DONT USE.xls"
    wb = xlrd.open_workbook(file)

    user_input = ParamatersDefinedByUser(4000, 60000, 1, 1, 1)
    spans = define_spans(wb)
    define_long_rebar(wb, spans)
    finalize_spans(spans)
    
    
    add_min_reinf(spans)
    reinf_for_max_area(spans,user_input)
    # assign_from_bar_schedule()
    update_req_areas(spans)

    root = Tk()
    gui = GUI(root, spans)
    root.mainloop()

    # for x in spans:
    #     x.get_span_info()

main()


