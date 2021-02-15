import math
import more_itertools as mit
import copy
import time

from Classes import RebarElement
from create_spans import define_spans
from create_spans import define_long_rebar
from create_spans import finalize_spans
from update_rebar import assign_from_bar_schedule


def add_min_reinf(beam_run_info):
    # i dont love this function, it just assigns the minimum amount of #6 bars as the minimum area
    # i want to make it more dynamic and assign the minimum amount of whichever bars are being used
    for rebar_req in beam_run_info.rebar_req:
        current_span = beam_run_info.spans[rebar_req[3]]

        rebar_req[1] = max(rebar_req[1], current_span.min_num_bars * .44)
        rebar_req[2] = max(rebar_req[2], current_span.min_num_bars * .44)

def reinf_for_max_area(beam_run_info, user_input):
    rebar_req = beam_run_info.rebar_req
    max_area, grouped_indices = get_max_area_indices(rebar_req)

    if max_area:
        for group in grouped_indices:
            bar_size , num_bars = get_best_rebar_sizes(beam_run_info, rebar_req[group[0]][3], max_area)
            dl = development_len(bar_size, user_input)

            start_loc = max(rebar_req[group[0]][0] - dl, 0)
            end_loc = min(rebar_req[group[-1]][0] + dl, beam_run_info.all_spans_len)
            new_bar = RebarElement(a_required=max_area, start_loc=start_loc, end_loc=end_loc, bar_size=bar_size, num_bars=num_bars)

            # try_extend_neighbor_bars(new_bar, beam_run_info)
            print(start_loc, end_loc)
            beam_run_info.top_rebar.append(new_bar)

    # for index in range(len(beam_run_info.rebar_req)):
    # for current_span in beam_run_info.spans:
    #     # returns 2d list [[max_left_top location, max_top_left area],[max_left_top location, max_top_left area], [[max_center_top]], [[max_right_top]]
    #     left_max_area, center_max_area, right_max_area = get_max_area(current_span)
    #     # print('max areas', left_max_area, center_max_area, right_max_area)

    #     # assign rebar in order
    #     # returns 3d list
    #     max_areas_and_locations = order_max_areas(left_max_area, center_max_area, right_max_area)
    #     # print('sorted max areas', max_areas)

    #     max_area = max_areas_and_locations[0][0][1]

    #     if max_area == 0:
    #         continue
    #     else:
    #         bar_size , num_bars = get_best_rebar_sizes(current_span, max_area)
    #         dl = development_len(bar_size, user_input) / current_span.length

    #         start_loc = current_span.len_prev_spans + current_span.length * round_down(max(max_areas_and_locations[0][0][0] - dl, 0))
    #         end_loc = current_span.len_prev_spans + current_span.length * round_up(min(max_areas_and_locations[0][-1][0] + dl, 1))
    #         new_bar = RebarElement(a_required=max_area, start_loc=start_loc, end_loc=end_loc, bar_size=bar_size, num_bars=num_bars)

    #         try_extend_neighbor_bars(new_bar, beam_run_info)
    #         beam_run_info.top_rebar.append(new_bar)

def get_max_area_indices(rebar_req):
    top_rebar_req = [row[1] for row in rebar_req]
    max_area = max(top_rebar_req)
    all_indices = [i for i, j in enumerate(top_rebar_req) if j == max_area]
    grouped_indices = [list(group) for group in mit.consecutive_groups(all_indices)]

    return max_area, grouped_indices

# def get_max_area_indices1(rebar_req):
#     max_top_area = 0
#     indices = [[]]
#     for index in range(len(rebar_req)):
#         temp_max_area = copy.copy(max_top_area)
#         max_top_area = max(rebar_req[index][1], max_top_area)
#         if max_top_area != temp_max_area:
#             indices = [[index]]
#         elif max_top_area == temp_max_area:
#             if index - indices[-1][-1] < 5:
#                 indices[-1].append(index)
#             else:
#                 indices.append([index])
#     return indices



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

def development_len(bar_size, user_input):
    bar_diameter = float(bar_size / 8)

    # per ACI 318-14 table 25.4.2.2
    if bar_size <= 6:
        constant = 20
    else:
        constant = 25

    # I need to ask clovis where this 1.3 comes from
    ld = user_input.yield_strength * user_input.psi_t * user_input.psi_e / (constant*user_input.lam*math.sqrt(user_input.fc)) * bar_diameter * (1.3/12)
    
    # print('development length', ld)
    return ld

def order_max_areas(left, center, right):
    # left center and right are 2d lists
    # put left center and right in order of greatest area required to least area required
    max_areas = []
    for x in range(3):
        if left[0][1] >= center[0][1] and left[0][1] >= right[0][1]:
            max_areas.append(left)
            left = [[0,-5]]
        elif center[0][1] >= left[0][1] and center[0][1] >= right[0][1]:
            max_areas.append(center)
            center = [[0,-3]]
        else:
            max_areas.append(right)
            right = [[0,-1]]

    return max_areas


def get_best_rebar_sizes(beam_run_info, span_num, area):
    min_num_bars = beam_run_info.spans[span_num].min_num_bars
    min_extra_rebar_area = 100

    for bar_num in range(6,12):
        bar_area = float(math.pi * float(bar_num / 8)**2 / 4 )
        num_bars = max(math.ceil(area / bar_area), min_num_bars)
        # print('info', x, area, bar_num, num_bars)

        extra_rebar_area = num_bars * bar_area - area

        # print('xetra rebar area', extra_rebar_area)
        if extra_rebar_area < min_extra_rebar_area:
            # print('ASSIGN BEST SIZE')
            best_size = bar_num
            num_best_bars = num_bars
            min_extra_rebar_area = extra_rebar_area

    return best_size, num_best_bars

def round_up(num):
    return float(math.ceil(num*20) / 20)

def round_down(num):
    return float(math.floor(num*20) / 20)

def try_extend_neighbor_bars(new_bar, beam_run_info):
    # print('try_extend_neighbor_bars')
    beam_run_info.top_rebar.sort(key=lambda x: x.start_loc)
    # for x in beam_run_info.top_rebar:
    #     print('start_loc',x.start_loc)