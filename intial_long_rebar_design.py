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
    spans = beam_run_info.spans
    group = grouped_indices[0]

    if max_area:
        # for group in grouped_indices:
        start_loc_span = rebar_req[group[0]][3]
        end_loc_span = rebar_req[group[0]][3]
        # set min num bars = to max min num bar value between the spans of the start and end location
        min_num_bars = max(spans[start_loc_span].get_min_num_bars(), spans[end_loc_span].get_min_num_bars())
        bar_size , num_bars = get_best_rebar_sizes(min_num_bars, max_area)
        dl = development_len(bar_size, user_input)

        start_loc = max(rebar_req[group[0]][0] - dl, 0)
        end_loc = min(rebar_req[group[-1]][0] + dl, beam_run_info.all_spans_len)
        new_bar = RebarElement(a_required=max_area, start_loc=start_loc, end_loc=end_loc, bar_size=bar_size, num_bars=num_bars, min_num_bars=min_num_bars)

        if not extend_neighbor_bars(new_bar, beam_run_info):
            beam_run_info.top_rebar.append(new_bar)

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


def get_best_rebar_sizes(min_num_bars, area):
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

def extend_neighbor_bars(new_bar, beam_run_info):
    # print('extend_neighbor_bars')
    copy_top_rebar_elements = copy.copy(beam_run_info.top_rebar)
    copy_top_rebar_elements.append(new_bar)
    copy_top_rebar_elements.sort(key=lambda x: x.start_loc)
    index_start = copy_top_rebar_elements.index(new_bar)

    surrounding_bars = []
    vol_diff = []
    if index_start:
        surrounding_bars.append(copy_top_rebar_elements[index_start-1])
    if index_start != len(copy_top_rebar_elements)-1:
        surrounding_bars.append(copy_top_rebar_elements[index_start+1])

    copy_top_rebar_elements.sort(key=lambda x: x.end_loc)
    index_end = copy_top_rebar_elements.index(new_bar)

    if index_end:
        if not copy_top_rebar_elements[index_start-1] in surrounding_bars:
            surrounding_bars.append(copy_top_rebar_elements[index_start-1])
    if index_end != len(copy_top_rebar_elements)-1:
        if not copy_top_rebar_elements[index_start+1] in surrounding_bars:
            surrounding_bars.append(copy_top_rebar_elements[index_start+1])

    for bar in surrounding_bars:
        if bar.a_from_smaller:
            continue
        og_volume = bar.volume + new_bar.volume

        if bar.a_provided + bar.a_from_smaller > new_bar.a_provided:
            print('new bar smaller')
            smaller_bar = copy.copy(new_bar)
            larger_bar = copy.copy(bar)
        else:
            print('new bar larger')
            smaller_bar = copy.copy(bar)
            larger_bar = copy.copy(new_bar)

        smaller_bar.start_loc = min(smaller_bar.start_loc, larger_bar.start_loc)
        smaller_bar.end_loc = max(smaller_bar.end_loc, larger_bar.end_loc)

        larger_bar.a_required -= smaller_bar.a_provided
        larger_bar.a_from_smaller = smaller_bar.a_provided
        larger_bar.bar_size , larger_bar.num_bars = get_best_rebar_sizes(larger_bar.min_num_bars - smaller_bar.num_bars, larger_bar.a_required)

        
        new_volume = smaller_bar.get_volume() + larger_bar.get_volume()

        vol_diff = og_volume-new_volume
        if vol_diff > 0:
            # bar = larger_bar
            # new_bar = smaller_bar
            beam_run_info.top_rebar.remove(bar)
            beam_run_info.top_rebar.append(larger_bar)
            beam_run_info.top_rebar.append(smaller_bar)
            print('vol diff', vol_diff, 'in3')
            return True
    return False


    # for x in beam_run_info.top_rebar:
    #     print('start_loc',x.start_loc)