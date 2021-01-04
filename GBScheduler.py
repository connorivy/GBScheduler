from openpyxl import Workbook
import openpyxl
from Classes import ParamatersDefinedByUser
from create_spans import get_input_geometry
import inspect
import math

def lineno():
    """Returns the current line number in our program."""
    return inspect.currentframe().f_back.f_lineno

def optimize_gbs(spans, user_input):
    for current_span in spans:
        # design top bars
        rebar_required = current_span.top_rebar_req

        # returns [max_left_top, max_center_top, max_right_top]
        max_areas = get_areas(current_span)

        # define max sizes and the optimal bar size and number of bars
        current_span.lt_rebar.a_required = max_areas[0]
        current_span.ct_rebar.a_required = max_areas[1]
        current_span.rt_rebar.a_required = max_areas[2]
        current_span.get_best_rebar_sizes()

        lt_max_area_locations = []
        rt_max_area_locations = []
        ct_max_area_locations = []

        for index in range(len(rebar_required.selected_area)):
            normalized_location = rebar_required.point_loc[index]
            area = rebar_required.selected_area[index]

            if normalized_location < .33:
                if area == max_areas[0]:
                    lt_max_area_locations.append(normalized_location)
            elif normalized_location > .66:
                if area == max_areas[2]:
                    rt_max_area_locations.append(normalized_location)
            else:
                if area == max_areas[1]:
                    ct_max_area_locations.append(normalized_location)

        length = current_span.length
        if lt_max_area_locations:
            dl = current_span.lt_rebar.development_len(user_input)
            current_span.lt_rebar.start_loc = max(lt_max_area_locations[0]*length - dl, 0)
            current_span.lt_rebar.end_loc = min(lt_max_area_locations[-1]*length + dl, length)

        if ct_max_area_locations:
            dl = current_span.ct_rebar.development_len(user_input)
            current_span.ct_rebar.start_loc = max(ct_max_area_locations[0]*length - dl, 0)
            current_span.ct_rebar.end_loc = min(ct_max_area_locations[0]*length + dl, length)

        if rt_max_area_locations:
            dl = current_span.rt_rebar.development_len(user_input)
            current_span.rt_rebar.start_loc = max(rt_max_area_locations[0]*length - dl, 0)
            current_span.rt_rebar.end_loc = min(rt_max_area_locations[-1]*length + dl, length)

        print('\nSpan Number ', current_span.number)
        print('  left top')
        current_span.lt_rebar.get_rebar_info()
        print('\n  center top')
        current_span.ct_rebar.get_rebar_info()
        print('\n  right top')
        current_span.rt_rebar.get_rebar_info()

def get_areas(current_span):
    max_left_top = 0
    max_right_top = 0
    max_center_top = 0

    min_left_top = 100
    min_right_top = 100
    min_center_top = 100

    rebar_required = current_span.top_rebar_req

    # get the area of rebar required for each third of the beam
    for data_point in range(len(rebar_required.point_loc)):
        if rebar_required.point_loc[data_point] < .33:
            max_left_top = max(rebar_required.selected_area[data_point], max_left_top)
            min_left_top = min(rebar_required.selected_area[data_point], min_left_top)
        elif rebar_required.point_loc[data_point] > .66:
            max_right_top = max(rebar_required.selected_area[data_point], max_right_top)
            min_right_top = min(rebar_required.selected_area[data_point], min_right_top)
        else:
            max_center_top = max(rebar_required.selected_area[data_point], max_center_top)
            min_center_top = min(rebar_required.selected_area[data_point], min_center_top)

    return [max_left_top, max_center_top, max_right_top]

def development_length(bar_size, user_input):
    bar_diameter = float(bar_size / 8)

    # per ACI 318-14 table 25.4.2.2
    if bar_size <= 6:
        constant = 20
    else:
        constant = 25

    # clovis multiplied development length by 1.3 and I'm not sure why.
    ld = user_input.yield_strength * user_input.psi_t * user_input.psi_e / (constant*user_input.lam*math.sqrt(user_input.fc)) * bar_diameter * (1.3/12)
    
    # print('development length', ld)
    return ld

    
def main():
    file = "report.xlsx"
    wb = openpyxl.load_workbook(file)
    ws = wb.active

    user_input = ParamatersDefinedByUser(4000, 60000, 1, 1, 1)
    spans = get_input_geometry(ws)
    optimize_gbs(spans, user_input)

main()


