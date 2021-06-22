import math
import more_itertools as mit
import copy
import time

from Classes import RebarElement
from create_spans import define_spans
from create_spans import define_long_rebar
from update_rebar import assign_from_bar_schedule


def add_min_reinf(beam_run_info):
    # i dont love this function, it just assigns the minimum amount of #6 bars as the minimum area
    # i want to make it more dynamic and assign the minimum amount of whichever bars are being used
    for rebar_req in beam_run_info.rebar_req:
        current_span = beam_run_info.spans[rebar_req[3]]

        rebar_req[1] = max(rebar_req[1], current_span.min_num_bars * .44)
        rebar_req[2] = max(rebar_req[2], current_span.min_num_bars * .44)

def reinf_for_max_area(beam_run_info, user_input):
    # rebar_req - [[absolute_location, a_top_rebar req at that location, area_bot_rebar req at that location, span number that location belongs to]]
    rebar_req = beam_run_info.rebar_req

    # this returns the maximum area followed by groups of consecutive indexes in which the maximum area occurrs in top_rebar_req
    # 1.68 , [[19,20,21],[41,42,43],[62,63]]
    max_area, grouped_indices = get_max_area_indices(rebar_req)
    spans = beam_run_info.spans
    group = grouped_indices[0]

    if max_area:
        # for group in grouped_indices:
        start_loc_span = rebar_req[group[0]][3]
        end_loc_span = rebar_req[group[-1]][3]

        # set min num bars = to max (min num bar value between the spans of the start and end location)
        min_num_bars = max(spans[start_loc_span].min_num_bars, spans[end_loc_span].min_num_bars)
        bar_size , num_bars = get_best_rebar_sizes(min_num_bars, max_area)
        dl = development_len(bar_size, user_input)

        start_loc = max(rebar_req[group[0]][0] - dl, 0)
        end_loc = min(rebar_req[group[-1]][0] + dl, beam_run_info.all_spans_len)
        new_bar = RebarElement(a_required=max_area, start_loc=start_loc, end_loc=end_loc, bar_size=bar_size, num_bars=num_bars, min_num_bars=min_num_bars)
        
        extend_neighbor_bars(new_bar, beam_run_info)

def get_max_area_indices(rebar_req):
    top_rebar_req = [row[1] for row in rebar_req]
    max_area = max(top_rebar_req)
    all_indices = [i for i, j in enumerate(top_rebar_req) if j == max_area]
    grouped_indices = [list(group) for group in mit.consecutive_groups(all_indices)]

    # this returns the maximum area followed by groups of consecutive indexes in which the maximum area occurrs in top_rebar_req
    # 1.68 , [[19,20,21],[41,42,43],[62,63]]
    
    return max_area, grouped_indices


def development_len(bar_size, user_input):
    bar_diameter = float(bar_size / 8)

    # per ACI 318-14 table 25.4.2.2
    if bar_size <= 6:
        constant = 20
    else:
        constant = 25

    # I need to ask clovis where this 1.3 comes from
    # second 1.3 is fresh conc factor
    ld = user_input.fy * user_input.psi_t * user_input.psi_e / (constant*user_input.lam*math.sqrt(user_input.fc)) * bar_diameter * (1/12) * 1.3 * 1.3
    
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
    # copy_top_rebar_elements.append(new_bar)
    # copy_top_rebar_elements.sort(key=lambda x: x.start_loc)
    # index_start = copy_top_rebar_elements.index(new_bar)

    # surrounding_bars = []
    # vol_diff = []

    for existing_bar in copy_top_rebar_elements:
        og_volume = existing_bar.get_volume() + new_bar.get_volume()
        # if existing_bar doesn't overlap the new beam then continue or if the bar already has a bar beneath it
        if existing_bar.end_loc < new_bar.start_loc or existing_bar.start_loc > new_bar.end_loc or existing_bar.a_from_smaller:
            continue
        elif existing_bar.start_loc < new_bar.start_loc and existing_bar.end_loc > new_bar.end_loc:
            print("This shouldn't happen. New bar inside the start and end of existing bar")
        else:
            if existing_bar.a_provided == new_bar.a_provided:
                # smaller_bar = copy.copy(new_bar)

                new_bar.start_loc = min(existing_bar.start_loc, new_bar.start_loc)
                new_bar.end_loc = max(existing_bar.end_loc, new_bar.end_loc)

                beam_run_info.top_rebar.remove(existing_bar)
                break

            if existing_bar.a_provided > new_bar.a_provided:
                # print(existing_bar.start_loc, existing_bar.end_loc)
                smaller_bar = copy.copy(new_bar)
                larger_bar = copy.copy(existing_bar)
            else:
                print("TRIED ADDING A LARGER THAN EXISTED - THIS SHOULDNT HAPPEN - DONT TRUST RESULTS")

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
                beam_run_info.top_rebar.remove(existing_bar)
                beam_run_info.top_rebar.append(larger_bar)
                new_bar = copy.copy(smaller_bar)
                
    beam_run_info.top_rebar.append(new_bar)
