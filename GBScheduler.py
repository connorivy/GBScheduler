from openpyxl import Workbook
import xlrd
import openpyxl
from Classes import ParamatersDefinedByUser
from create_spans import define_spans
from create_spans import define_long_rebar
from create_spans import finalize_spans
import inspect
import math

def lineno():
    """Returns the current line number in our program."""
    return inspect.currentframe().f_back.f_lineno

def reinf_for_max_area(spans, user_input):
    for current_span in spans:
        # returns [[[max_left_top location, max_top_left area],[max_left_top location, max_top_left area], [[max_center_top]], [[max_right_top]]]
        left_max_area, center_max_area, right_max_area = get_max_area(current_span)
        print('max areas', left_max_area)

        # assign the length of the reinforcement to go from the first instance of max area - dl to last instance of the max area location plus the developement length
        # also normalize that length so it can be subtracted from the overall list of areas
        length = current_span.length
        if left_max_area[0][1]:
            dl = current_span.lt_rebar.development_len(user_input) / length
            current_span.lt_rebar.start_loc = round_down(max(lt_max_area_locations[0] - dl, 0))
            current_span.lt_rebar.end_loc = round_up(min(lt_max_area_locations[-1] + dl, 1))

        if ct_max_area_locations:
            dl = current_span.ct_rebar.development_len(user_input) / length
            current_span.ct_rebar.start_loc = round_down(max(ct_max_area_locations[0] - dl, 0))
            current_span.ct_rebar.end_loc = round_up(min(ct_max_area_locations[-1] + dl, 1))

        if rt_max_area_locations:
            dl = current_span.rt_rebar.development_len(user_input) / length
            current_span.rt_rebar.start_loc = round_down(max(rt_max_area_locations[0] - dl, 0))
            current_span.rt_rebar.end_loc = round_up(min(rt_max_area_locations[-1] + dl, 1))

################################################################################################################################################################################################
################################################################################################################################################################################################
# I left off working on the above code. My development length function needs to be updated because I'm no longer storing data where it is trying to reference it

def get_max_area(current_span):
    # design top bars
    # returns 3d list [[[location,area],[location,area]],[[location,area],[location,area]],[[location,area],[location,area]]]
    split = split_list_into_thirds(current_span.top_rebar_req)
    # print('split', split)

    left_max_area = [[0,0]]
    center_max_area = [[0,0]]
    right_max_area = [[0,0]]

    for segment in range(len(split)):
        # print('split[segment]', split[segment])
        for index in range(len(split[segment])):
            # print('split[segment][index]', split[segment][index])
            if split[segment][index][1] == 0:
                continue
            if segment == 0:
                if split[segment][index][1] > left_max_area[0][1]:
                    left_max_area = [split[segment][index]]
                elif split[segment][index][1] == left_max_area[0][1]:
                    left_max_area.append(split[segment][index])
            elif segment == 1:
                if split[segment][index][1] > center_max_area[0][1]:
                    center_max_area = [split[segment][index]]
                elif split[segment][index][1] == center_max_area[0][1]:
                    center_max_area.append(split[segment][index])
            else:
                if split[segment][index][1] > right_max_area[0][1]:
                    right_max_area = [split[segment][index]]
                elif split[segment][index][1] == right_max_area[0][1]:
                    right_max_area.append(split[segment][index])

    return left_max_area,center_max_area,right_max_area

def split_list_into_thirds(list2d):
    left = []
    center = []
    right = []
    for x in range(len(list2d)):
        if list2d[x][0] < .33:
            left.append(list2d[x])
        elif list2d[x][0] > .66:
            right.append(list2d[x])
        else:
            center.append(list2d[x])

    out = [left,center,right]
    # print(out)
    return out

    def development_len(self, user_input):
        bar_diameter = float(self.bar_size / 8)

        # per ACI 318-14 table 25.4.2.2
        if self.bar_size <= 6:
            constant = 20
        else:
            constant = 25
        ld = user_input.yield_strength * user_input.psi_t * user_input.psi_e / (constant*user_input.lam*math.sqrt(user_input.fc)) * bar_diameter * (1.3/12)
        
        # print('development length', ld)
        return ld

# def optimize_gbs(spans, user_input):
#     for current_span in spans:
#         # design top bars
#         top_rebar_required = current_span.top_rebar_req

#         # returns [max_left_top, max_center_top, max_right_top]
#         max_areas = get_areas(current_span)

#         # define max sizes and the optimal bar size and number of bars
#         current_span.lt_rebar.a_required = max_areas[0]
#         current_span.ct_rebar.a_required = max_areas[1]
#         current_span.rt_rebar.a_required = max_areas[2]
#         current_span.get_best_rebar_sizes()

#         # get all locations along each third of the beam in which the max area will be found
#         lt_max_area_locations = []
#         rt_max_area_locations = []
#         ct_max_area_locations = []
#         for index in range(len(top_rebar_required)):
#             normalized_location = top_rebar_required[index][0]
#             area = top_rebar_required[index][1]

#             if normalized_location < .33:
#                 if area == max_areas[0]:
#                     lt_max_area_locations.append(normalized_location)
#             elif normalized_location > .66:
#                 if area == max_areas[2]:
#                     rt_max_area_locations.append(normalized_location)
#             else:
#                 if area == max_areas[1]:
#                     ct_max_area_locations.append(normalized_location)

#         # assign the length of the reinforcement to go from the first instance of max area - dl to last instance of the max area location plus the developement length
#         # also normalize that length so it can be subtracted from the overall list of areas
#         length = current_span.length
#         if lt_max_area_locations:
#             dl = current_span.lt_rebar.development_len(user_input) / length
#             current_span.lt_rebar.start_loc = round_down(max(lt_max_area_locations[0] - dl, 0))
#             current_span.lt_rebar.end_loc = round_up(min(lt_max_area_locations[-1] + dl, 1))

#         if ct_max_area_locations:
#             dl = current_span.ct_rebar.development_len(user_input) / length
#             current_span.ct_rebar.start_loc = round_down(max(ct_max_area_locations[0] - dl, 0))
#             current_span.ct_rebar.end_loc = round_up(min(ct_max_area_locations[-1] + dl, 1))

#         if rt_max_area_locations:
#             dl = current_span.rt_rebar.development_len(user_input) / length
#             current_span.rt_rebar.start_loc = round_down(max(rt_max_area_locations[0] - dl, 0))
#             current_span.rt_rebar.end_loc = round_up(min(rt_max_area_locations[-1] + dl, 1))

#         print('\nSpan Number ', current_span.number)
#         print('  left top')
#         current_span.lt_rebar.get_rebar_info()
#         print('\n  center top')
#         current_span.ct_rebar.get_rebar_info()
#         print('\n  right top')
#         current_span.rt_rebar.get_rebar_info()

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
    finalize_spans(spans)

    # for x in spans:
    #     x.get_span_info()

    # optimize_gbs(spans, user_input)
    reinf_for_max_area(spans,user_input)

main()


