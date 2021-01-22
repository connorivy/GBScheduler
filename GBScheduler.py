from openpyxl import Workbook
import xlrd
import openpyxl
from tkinter import Tk, Canvas, Frame, BOTH
import inspect
import math

from Classes import ParamatersDefinedByUser
from Classes import RebarElement
from create_spans import define_spans
from create_spans import define_long_rebar
from create_spans import finalize_spans
from gui import GUI

def lineno():
    """Returns the current line number in our program."""
    return inspect.currentframe().f_back.f_lineno

def add_min_reinf(spans):
    # i dont love this function, it just assigns the minimum amount of #6 bars as the minimum area
    # i want to make it more dynamic and assign the minimum amount of whichever bars are being used
    for current_span in spans:
        # print(current_span.top_rebar_req)
        current_span.get_min_num_bars()
        min_num_bars = current_span.min_num_bars
        for pair in current_span.top_rebar_req:
            area = pair[1]
            pair[1] = max(area, min_num_bars * .44)
        # print(current_span.top_rebar_req)

def reinf_for_max_area(spans, user_input):
    for current_span in spans:
        # returns 2d list [[max_left_top location, max_top_left area],[max_left_top location, max_top_left area], [[max_center_top]], [[max_right_top]]
        left_max_area, center_max_area, right_max_area = get_max_area(current_span)
        # print('max areas', left_max_area, center_max_area, right_max_area)

        # assign rebar in order
        # returns 3d list
        max_areas_and_locations = order_max_areas(left_max_area, center_max_area, right_max_area)
        # print('sorted max areas', max_areas)

        max_area = max_areas_and_locations[0][0][1]

        if max_area == 0:
            continue
        else:
            bar_size , num_bars = get_best_rebar_sizes(current_span, max_area)
            length = current_span.length
            dl = development_len(bar_size, user_input) / length

            start_loc = round_down(max(max_areas_and_locations[0][0][0] - dl, 0))
            end_loc = round_up(min(max_areas_and_locations[0][-1][0] + dl, 1))
            current_span.top_rebar_elements.append(RebarElement(a_required=max_area, start_loc=start_loc, end_loc=end_loc, bar_size=bar_size, num_bars=num_bars))
            current_span.top_rebar_elements[-1].get_area()

def update_req_areas(spans):
    for current_span in spans:
        print(current_span.top_rebar_req)
        for rebar_element in current_span.top_rebar_elements:
            if not rebar_element.rebar_subtracted:
                for pair in current_span.top_rebar_req:
                    if rebar_element.start_loc <= pair[0] and rebar_element.end_loc >= pair[0]:
                        pair[1] = max(pair[1] - rebar_element.a_provided, 0)
                    rebar_element.rebar_subtracted = True
        print(current_span.top_rebar_req, '\n')

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


def get_best_rebar_sizes(current_span, area):
    min_num_bars = current_span.min_num_bars
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

def round_up(num):
    return float(math.ceil(num*20) / 20)

def round_down(num):
    return float(math.floor(num*20) / 20)

    
def main():
    file = "helper_files/report - DONT USE.xls"
    wb = xlrd.open_workbook(file)

    user_input = ParamatersDefinedByUser(4000, 60000, 1, 1, 1)
    spans = define_spans(wb)
    # define_long_rebar(wb, spans)
    # finalize_spans(spans)

    # add_min_reinf(spans)
    # reinf_for_max_area(spans,user_input)
    # update_req_areas(spans)

    root = Tk()
    gui = GUI(root, spans)
    root.mainloop()

    # for x in spans:
    #     x.get_span_info()

main()


