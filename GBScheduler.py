from openpyxl import Workbook
import xlrd
import openpyxl
from Classes import ParamatersDefinedByUser
from create_spans import define_spans
from create_spans import define_long_rebar
import inspect
import math

def lineno():
    """Returns the current line number in our program."""
    return inspect.currentframe().f_back.f_lineno

def optimize_gbs(spans, user_input):
    for current_span in spans:
        # design top bars
        top_rebar_required = current_span.top_rebar_req
        # print(current_span.top_rebar_req.get_rebar_req_info())

        # returns [max_left_top, max_center_top, max_right_top]
        max_areas = get_areas(current_span)
        # print(max_areas)

        # define max sizes and the optimal bar size and number of bars
        current_span.lt_rebar.a_required = max_areas[0]
        current_span.ct_rebar.a_required = max_areas[1]
        current_span.rt_rebar.a_required = max_areas[2]
        current_span.get_best_rebar_sizes()

        # get all locations along each third of the beam in which the max area will be found
        lt_max_area_locations = []
        rt_max_area_locations = []
        ct_max_area_locations = []
        for index in range(len(top_rebar_required)):
            normalized_location = top_rebar_required[index][0]
            area = top_rebar_required[index][1]

            if normalized_location < .33:
                if area == max_areas[0]:
                    lt_max_area_locations.append(normalized_location)
            elif normalized_location > .66:
                if area == max_areas[2]:
                    rt_max_area_locations.append(normalized_location)
            else:
                if area == max_areas[1]:
                    ct_max_area_locations.append(normalized_location)

        # assign the length of the reinforcement to go from the last instance of the max area location plus the developement length
        # also normalize that length so it can be subtracted from the overall list of areas
        length = current_span.length
        if lt_max_area_locations:
            dl = current_span.lt_rebar.development_len(user_input) / length
            current_span.lt_rebar.start_loc = round_down(max(lt_max_area_locations[0] - dl, 0))
            current_span.lt_rebar.end_loc = round_up(min(lt_max_area_locations[-1] + dl, 1))

        if ct_max_area_locations:
            dl = current_span.ct_rebar.development_len(user_input) / length
            current_span.ct_rebar.start_loc = round_down(max(ct_max_area_locations[0] - dl, 0))
            current_span.ct_rebar.end_loc = round_up(min(ct_max_area_locations[0] + dl, 1))

        if rt_max_area_locations:
            dl = current_span.rt_rebar.development_len(user_input) / length
            current_span.rt_rebar.start_loc = round_down(max(rt_max_area_locations[0] - dl, 0))
            current_span.rt_rebar.end_loc = round_up(min(rt_max_area_locations[-1] + dl, 1))

        print('\nSpan Number ', current_span.number)
        print('  left top')
        current_span.lt_rebar.get_rebar_info()
        print('\n  center top')
        current_span.ct_rebar.get_rebar_info()
        print('\n  right top')
        current_span.rt_rebar.get_rebar_info()

        # adjust_req_rebar(current_span)

###############################################################################################################################################################
# I left off working on this. I'm thinking about changing the lists into a dictionary bc I definitely should have done that in the first place
# but I'm trying to subtract the rebar areas that my code gives from those that ADAPT gives
###############################################################################################################################################################

# def adjust_req_rebar(current_span, rebar_element):
#     # lengths = [.02, .05, .1, .15, .2, .25, .3, .35, .4, .45, .5, .55, .6, .65, .7, .75, .8, .85, .9, .95, .98]

#     if rebar_element.start_loc == 0 and current_span.top_rebar_req.point_loc[0] < .05:
#         current_span.top_rebar_req.point_loc[0]

#     for dist in range(0,len(span.top_rebar_req.point_loc)):
#         print('point location = ', span.top_rebar_req.point_loc[dist])
#         print('selected_area = ', span.top_rebar_req.selected_area[dist])

#         span.top_rebar_req.point_loc[dist]

def get_areas(current_span):
    max_left_top = 0
    max_right_top = 0
    max_center_top = 0

    min_left_top = 100
    min_right_top = 100
    min_center_top = 100

    top_rebar_required = current_span.top_rebar_req

    # get the area of rebar required for each third of the beam
    for data_point in range(len(top_rebar_required)):
        if top_rebar_required[data_point][0] < .33:
            max_left_top = max(top_rebar_required[data_point][1], max_left_top)
            min_left_top = min(top_rebar_required[data_point][1], min_left_top)
        elif top_rebar_required[data_point][0] > .66:
            max_right_top = max(top_rebar_required[data_point][1], max_right_top)
            min_right_top = min(top_rebar_required[data_point][1], min_right_top)
        else:
            max_center_top = max(top_rebar_required[data_point][1], max_center_top)
            min_center_top = min(top_rebar_required[data_point][1], min_center_top)

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

def round_up(num):
    return float(math.ceil(num*20) / 20)

def round_down(num):
    return float(math.floor(num*20) / 20)

    
def main():
    file = "helper_files/report - DONT USE.xls"
    wb = xlrd.open_workbook(file)

    user_input = ParamatersDefinedByUser(4000, 60000, 1, 1, 1)
    spans = define_spans(wb)
    define_long_rebar(wb, spans)

    # for x in spans:
    #     x.get_span_info()

    optimize_gbs(spans, user_input)

main()


