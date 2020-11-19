from openpyxl import Workbook
import openpyxl
import inspect
import math

def lineno():
    """Returns the current line number in our program."""
    return inspect.currentframe().f_back.f_lineno

class ParamatersDefinedByUser:
    def __init__(self, fc, yield_strength, psi_t, psi_e, lam):
        self.fc = fc
        self.yield_strength = yield_strength

        # per ACI 318-14 table 25.4.2.4
        self.psi_t = psi_t
        self.psi_e = psi_e
        self.lam = lam

class RebarElement:
    def __init__(self, a_required=0, start_loc=100, end_loc=0, start2_loc=0, end2_loc=0, bar_size=0):
        self.a_required = a_required     
        self.bar_size = bar_size
        self.start_loc = start_loc
        self.end_loc = end_loc
        self.start2_loc = start2_loc
        self.end2_loc = end2_loc

    def get_area(self):
        self.bar_diameter = float(self.bar_size / 8)
        self.a_provided = float(math.pi * self.bar_diameter**2 / 4 )

    def get_rebar_info(self):
        self.get_area
        print('  area required:       ', self.a_required)
        # print('  area provided:       ', self.a_provided)
        print('  bar size:            ', self.bar_size)
        print('  start location:      ', self.start_loc)
        print('  end location:        ', self.end_loc)

class Span:
    def __init__(self, number, length, width, depth, fc=4000, cover_bot=3, cover_top=1.5, cover_side=2):
        self.number = number
        self.length = length
        self.width = width
        self.depth = depth
        self.fc = fc
        self.cover_bot = cover_bot
        self.cover_top = cover_top
        self.cover_side = cover_side
        self.top_rebar_req = None
        self.bot_rebar_req = None
        self.lt_rebar = RebarElement()
        self.cb_rebar = RebarElement()
        self.ct_rebar = RebarElement()
        self.rt_rebar = RebarElement()
        self.stirrups = None

    def get_span_info(self):
        print('\n\nspan number:           ', self.number)
        print('********************************************************************')
        print('span length:           ', self.length)
        print('span width:            ', self.width)
        print('span depth:            ', self.depth)
        print('\ntop rebar:')
        if self.top_rebar_req == None:
            print('  -')
        else:
            self.top_rebar_req.get_rebar_req_info()

        print('\nbottom rebar:')
        if self.bot_rebar_req == None:
            print('  -')
        else:
            self.bot_rebar_req.get_rebar_req_info()
        
    # def effective_depth():
    #     return self.depth -
    
    # def max_shear_spacing():

class RebarRequirements:
    def __init__(self, point_loc, selected_area, bar_size=0, yield_strength=60000):
        self.point_loc = [point_loc]
        self.selected_area = [selected_area]
        self.a_required = 0
        self.start_loc = 0
        self.end_loc = 0
        self.bar_size = bar_size
        self.yield_strength = yield_strength

    def get_rebar_req_info(self):
        print('  location, selected_area')
        for x in range(len(self.point_loc)):
            print('    ', self.point_loc[x], ', ', self.selected_area[x])

        # print('  area required:       ', self.a_required)
        # print('  start location:      ', self.start_loc)
        # print('  end location:        ', self.end_loc)
        # print('  bar size:            ', self.bar_size)

class Stirrups:
    def __init__(self, a_required, start_loc, end_loc):
        self.a_required = a_required
        self.start_loc = start_loc
        self.end_loc = end_loc

class Search:
    def __init__(self, start_flag, end_flag):
        self.looking = False
        self.defined = False
        self.start_flag = start_flag
        self.end_flag = end_flag


def get_input_geometry(ws):
    span_search = Search("2.1 Principal Span Data of Uniform Spans","2.7 Support Width and Column Data")
    long_reinf_search = Search('29 - DETAILED REBAR', 'Note: Reinforcement requirements for Initial condition are included in Service block. Reinforcement requirements for UBC combination, if selected, are included in Analysis block.')
    shear_reinf_search = Search('12.1 Shear Calculation Envelope','Note: "Ratio" is calculated using paired shear (V) and moment (M) design values resulting in the lowest concrete capacity. For ACI and CSA codes, the lowest value of V*d/M is used.')

    row_count = ws.max_row
    spans = []

    for row in ws.iter_rows(min_col=1, max_col=1, max_row = row_count):
        for cell in row:
            if not span_search.defined:
                new_span = look_for_grade_beam_data(cell, span_search, add_span, spans)
                if new_span:
                    spans.append(new_span)

            if not long_reinf_search.defined:
                # print('looking of rebar')
                look_for_grade_beam_data(cell, long_reinf_search, add_long_reinf_criteria, spans)

    for x in spans:
        x.get_span_info()

    return spans
            

def look_for_grade_beam_data(cell, search_obj, func, spans):
    if cell.value == search_obj.start_flag:
        search_obj.looking = True
        return

    elif cell.value == search_obj.end_flag:
        search_obj.looking = False
        search_obj.defined = True
        return


    if search_obj.looking:
        return func(cell,spans,search_obj)

def add_span(cell,spans,search_obj):
    if str(cell.value).replace('.','',1).isdigit():
        # returns span object with the following attributes
        # number, length, width, depth
        return Span(float(cell.value), float(cell.offset(0,2).value), float(cell.offset(0,3).value), float(cell.offset(0,4).value))
    else:
        return 0

def add_long_reinf_criteria(cell,spans,search_obj):
    if 'SPAN' in str(cell.value):
        num = [int(i) for i in str(cell.value).split() if i.isdigit()]
        if len(num) == 1:
            # store current span in the long_reinf_search object to remember next time this function is called
            search_obj.current_span = spans[num[0]-1]
        elif len(num) == 0:
            print('Error trying to find detailed rebar, cannot identify span. No numbers present')
        else:
            print('Error trying to find detailed rebar, cannot identify span. Multiple numbers present')
    

    if str(cell.value).replace('.','',1).isdigit():
        # define bottom rebar if areaq not 0
        if not str(cell.offset(0,7).value) == '0' and not cell.offset(0,7).value == None: 
            # test if cb rebar is defined
            if search_obj.current_span.bot_rebar_req == None:
                # point location, selected area
                search_obj.current_span.bot_rebar_req = RebarRequirements(round(float(cell.value),2),round(float(cell.offset(0,7).value),2))
            else:
                search_obj.current_span.bot_rebar_req.point_loc.append(round(float(cell.value),2))
                search_obj.current_span.bot_rebar_req.selected_area.append(round(float(cell.offset(0,7).value),2))
        # define top rebar if area not 0
        if not str(cell.offset(0,6).value) == '0' and not cell.offset(0,6).value == None:
            # test if cb rebar is defined
            if search_obj.current_span.top_rebar_req == None:
                # point location, selected area
                search_obj.current_span.top_rebar_req = RebarRequirements(round(float(cell.value),2),round(float(cell.offset(0,6).value),2))
            else:
                search_obj.current_span.top_rebar_req.point_loc.append(round(float(cell.value),2))
                search_obj.current_span.top_rebar_req.selected_area.append(round(float(cell.offset(0,6).value),2))

def optimize_gbs(spans, user_input):
    for current_span in spans:
        # design top bars
        # max_area, min_area = get_areas(current_span)

        rebar_required = current_span.top_rebar_req
        max_area, min_area = max(rebar_required.selected_area), min(rebar_required.selected_area)

        beam_width_no_cover = current_span.width - 2 * current_span.cover_side
        min_num_bars = math.ceil(beam_width_no_cover / 18) + 1

        max_best_size = get_best_size(max_area, min_num_bars)
        min_best_size = get_best_size(min_area, min_num_bars)

        print(max_best_size, min_best_size)


        m = max(rebar_required.selected_area)
        max_indexes = [i for i, j in enumerate(rebar_required.selected_area) if j == m]
        print(max_indexes)

        for index in max_indexes:
            normalized_location = rebar_required.point_loc[index]
            area = rebar_required.selected_area[index]
            start_location = current_span.length * normalized_location
            print(normalized_location)

            if normalized_location < .33:
                ###################################################################################################################################
                # replace the hardcoded 10
                dl = development_length(10, user_input)
                ###################################################################################################################################
                if area > current_span.lt_rebar.a_required:
                    current_span.lt_rebar.a_required = area
                if start_location < current_span.lt_rebar.start_loc:
                    current_span.lt_rebar.start_loc = start_location
                    if current_span.lt_rebar.end_loc == 0:
                        current_span.lt_rebar.end_loc = start_location + dl
                elif start_location > current_span.lt_rebar.start_loc:
                    current_span.lt_rebar.end_loc = start_location + dl

            if normalized_location < .33:
                ###################################################################################################################################
                # replace the hardcoded 10
                dl = development_length(10, user_input)
                ###################################################################################################################################
                if area > current_span.lt_rebar.a_required:
                    current_span.lt_rebar.a_required = area
                if start_location < current_span.lt_rebar.start_loc:
                    current_span.lt_rebar.start_loc = start_location
                    if current_span.lt_rebar.end_loc == 0:
                        current_span.lt_rebar.end_loc = start_location + dl
                elif start_location > current_span.lt_rebar.start_loc:
                    current_span.lt_rebar.end_loc = start_location + dl

        print('rebar info for span ', current_span.number)
        current_span.lt_rebar.get_rebar_info()
        current_span.rt_rebar.get_rebar_info()

        # for bar_size in range(6,10):
        #     dl = development_length(bar_size, user_input)

        #     rebar_required = current_span.top_rebar_req

        #     # get the area of rebar required for each third of the beam
        #     for data_point in range(len(rebar_required.point_loc)):
        





        # # go back through the rebar requirements find the location when a steel =
        # for data_point in range(len(rebar_required.point_loc)):
        #     print()

    # #######################################################################################################
    # I left off working on the above formula to get the most effecient bar size
    # right now it just gets the one with the smallest remainder which I'm not sure is best
    # I'm thinking I'll have it design the whole line of GBs to see which bar uses the least amount of steel

    # for bar_size in range(6,10):
    #     dl = development_length(bar_size, user_input)

    #     for current_span in spans:
    #         # design top rebar
    #         max_left_top = 0
    #         max_right_top = 0
    #         max_center_top = 0
    #         rebar_required = current_span.top_rebar_req
    #         # get the area of rebar required for each side of the midpoint of the beam
    #         for data_point in range(len(rebar_required.point_loc)):
    #             if rebar_required.point_loc[data_point] < .33:
    #                 max_left_top = max(rebar_required.selected_area[data_point], max_left_top)
    #             elif rebar_required.point_loc[data_point] > .66:
    #                 max_right_top = max(rebar_required.selected_area[data_point], max_right_top)
    #             else:
    #                 max_center_top = max(rebar_required.selected_area[data_point], max_center_top)

    #     if max_left_top > max_center_top or max_right_top > max_center_top:


    #         print(max_left_top, max_right_top, max_center_top)


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
    print('development length', ld)
    return ld

    
def main():
    file = "report.xlsx"
    wb = openpyxl.load_workbook(file)
    ws = wb.active

    user_input = ParamatersDefinedByUser(4000, 60000, 1, 1, 1)
    spans = get_input_geometry(ws)
    optimize_gbs(spans, user_input)

main()


