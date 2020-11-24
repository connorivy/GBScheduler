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
        # # design top bars
        # # max_area, min_area = get_areas(current_span)

        # rebar_required = current_span.top_rebar_req
        # max_area, min_area = max(rebar_required.selected_area), min(rebar_required.selected_area)

        # beam_width_no_cover = current_span.width - 2 * current_span.cover_side
        # min_num_bars = math.ceil(beam_width_no_cover / 18) + 1

        # max_best_size = get_best_size(max_area, min_num_bars)
        # min_best_size = get_best_size(min_area, min_num_bars)

        # print(max_best_size, min_best_size)

        rebar_required = current_span.top_rebar_req
        # returns [max_left_top, max_center_top, max_right_top]
        max_areas = get_areas(current_span)

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
        
        dl = development_length(11, user_input)

        if lt_max_area_locations:
            current_span.lt_rebar.a_required = max_areas[0]
            current_span.lt_rebar.start_loc = lt_max_area_locations[0]*current_span.length
            current_span.lt_rebar.end_loc = lt_max_area_locations[-1]*current_span.length + dl

        if ct_max_area_locations:
            current_span.ct_rebar.a_required = max_areas[1]
            current_span.ct_rebar.start_loc = ct_max_area_locations[0]*current_span.length - dl
            current_span.ct_rebar.start_loc = ct_max_area_locations[0]*current_span.length + dl

        if rt_max_area_locations:
            current_span.rt_rebar.a_required = max_areas[2]
            current_span.rt_rebar.start_loc = rt_max_area_locations[0]*current_span.length
            current_span.rt_rebar.end_loc = rt_max_area_locations[-1]*current_span.length + dl

        print('Span Number ', current_span.number)
        current_span.lt_rebar.get_rebar_info()
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


def get_best_size(area, min_num_bars):
    # set a value for the rebar remainder that will definitely be higher than all other remainder values 
    min_extra_rebar_area = 100
    # print('area', area)

    # loop through all bar sizes to find the most economic size
    for x in range(6,10):
        # print('bar size', x)
        bar_area = float(math.pi * float(x / 8)**2 / 4 )
        num_bars = math.ceil(area / bar_area)

        if num_bars < min_num_bars:
            num_bars = min_num_bars

        extra_rebar_area = num_bars * bar_area - area

        # print('xetra rebar area', extra_rebar_area)
        if extra_rebar_area < min_extra_rebar_area:
            # print('ASSIGN BEST SIZE')
            best_size = x
            min_extra_rebar_area = extra_rebar_area

    return best_size

def development_length(bar_size, user_input):
    bar_diameter = float(bar_size / 8)

    # per ACI 318-14 table 25.4.2.2
    if bar_size <= 6:
        constant = 20
    else:
        constant = 25
    ld = user_input.yield_strength * user_input.psi_t * user_input.psi_e / (constant*user_input.lam*math.sqrt(user_input.fc)) * bar_diameter * (1.3/12)

    rounded = math.ceil(ld*2) / 2.0
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


