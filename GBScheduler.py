from openpyxl import Workbook
import xlrd
import openpyxl
from tkinter import Tk, Canvas, Frame, BOTH, Button
import inspect

from Classes import ParametersDefinedByUser, BeamRunInfo
from Classes import RebarElement
from create_spans import define_spans
from create_spans import define_long_rebar
from create_spans import finalize_spans
from gui import GUI
from intial_long_rebar_design import add_min_reinf, reinf_for_max_area
from update_rebar import assign_from_bar_schedule, update_req_areas

def lineno():
    """Returns the current line number in our program."""
    return inspect.currentframe().f_back.f_lineno
    
def main():
    file = "helper_files/report - DONT USE.xls"
    wb = xlrd.open_workbook(file)

    beam_run_info = BeamRunInfo()
    user_input = ParametersDefinedByUser(4000, 60000, 1, 1, 1)

    beam_run_info.spans, beam_run_info.max_beam_depth, beam_run_info.all_spans_len = define_spans(wb)
    # finalize_spans(beam_run_info)

    define_long_rebar(wb, beam_run_info)  
    # beam_run_info.get_rebar_req_info()

    add_min_reinf(beam_run_info)
    reinf_for_max_area(beam_run_info,user_input)
    assign_from_bar_schedule(beam_run_info)
    update_req_areas(beam_run_info)

    root = Tk()
    gui = GUI(root, beam_run_info, user_input)
    root.mainloop()

    # for x in spans:
    #     x.get_span_info()

main()


