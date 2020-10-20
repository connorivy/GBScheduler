from openpyxl import Workbook
import openpyxl
import inspect
import math

def lineno():
    """Returns the current line number in our program."""
    return inspect.currentframe().f_back.f_lineno

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
        self.top_rebar = None
        self.bot_rebar = None
        self.stirrups = None

    def get_span_info(self):
        print('\n\nspan number:           ', self.number)
        print('********************************************************************')
        print('span length:           ', self.length)
        print('span width:            ', self.width)
        print('span depth:            ', self.depth)
        print('\ntop rebar:')
        if self.top_rebar == None:
            print('  -')
        else:
            self.top_rebar.get_rebar_info()

        print('\nbottom rebar:')
        if self.bot_rebar == None:
            print('  -')
        else:
            self.bot_rebar.get_rebar_info()
        
    # def effective_depth():
    #     return self.depth -
    
    # def max_shear_spacing():

class Rebar:
    def __init__(self, selected, point_loc, bar_size=0, yield_strength=60000):
        self.point_loc = [point_loc]
        self.selected = [selected]
        self.a_req = 0
        self.start_loc = 0
        self.end_loc = 0
        self.bar_size = bar_size
        self.yield_strength = yield_strength

    def get_rebar_info(self):
        print('  location, area selected')
        for x in range(len(self.point_loc)):
            print('    ', self.point_loc[x], ', ', self.selected[x])

        print('  area required:       ', self.a_req)
        print('  start location:      ', self.start_loc)
        print('  end location:        ', self.end_loc)
        print('  bar size:            ', self.bar_size)

    def development_length(self):
        # per ACI 318-14 table 25.4.2.4
        psi_t = 1
        psi_e = 1
        lam = 1

        # not from ACI
        fc = 4000
        self.bar_diameter = .875

        # per ACI 318-14 table 25.4.2.2
        ld = self.yield_strength * psi_t * psi_e / (20*lam*math.sqrt(fc)) * self.bar_diameter * (1.3/12)
        print('development length in feet', ld)
        return ld

class Stirrups:
    def __init__(self, a_req, start_loc, end_loc):
        self.a_req = a_req
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
                new_span = look_for_grade_beam_data(cell, long_reinf_search, add_long_reinf_criteria, spans)
                if new_span:
                    spans.append(new_span)

            # if not shear_reinf_search.defined:
            #     new_span = look_for_grade_beam_data(cell, span_search, add_span)
            #     if new_span:
            #         spans.append(new_span)
    for x in spans:
        x.get_span_info()
            

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
        return Span(int(cell.value), float(cell.offset(0,2).value), float(cell.offset(0,3).value), float(cell.offset(0,4).value))
    else:
        return 0


# this function was used for the summarized rebar chart and it works but I learned that the summarized rebar isnt detailed enough
# def add_long_reinf_criteria(cell,spans):
#     if str(cell.value).replace('.','',1).isdigit():
#         current_span = spans[int(cell.value)-1]
    
#     if str(cell.offset(0,1).value) == 'TOP':
        
#         if abs(float(cell.offset(0,2).value)) < .1:
#             current_span.top_rebar = Rebar(float(cell.offset(0,4).value),float(cell.offset(0,2).value),float(cell.offset(0,3).value))
#         elif abs(current_span.length - float(cell.offset(0,3).value)) < .1:
#             current_span.rt_rebar = Rebar(float(cell.offset(0,4).value),float(cell.offset(0,2).value),float(cell.offset(0,3).value))
#         else:
#             current_span.ct_rebar = Rebar(float(cell.offset(0,4).value),float(cell.offset(0,2).value),float(cell.offset(0,3).value))

#     elif str(cell.offset(0,1).value) == 'BOT':
#         # returns rebar object with the following attributes
#         # location (top, bottom), a_req, start_loc, end_loc,
#         current_span.bot_rebar = Rebar(float(cell.offset(0,4).value),float(cell.offset(0,2).value),float(cell.offset(0,3).value))


def add_long_reinf_criteria(cell,spans,search_obj):
    print('cell value', cell.value)
    if 'SPAN' in str(cell.value):
        num = [int(i) for i in str(cell.value).split() if i.isdigit()]
        print('list of nums', num)
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
            if search_obj.current_span.bot_rebar == None:
                # point location, selected area
                search_obj.current_span.bot_rebar = Rebar(round(float(cell.value)*search_obj.current_span.length,1),round(float(cell.offset(0,7).value),2))
            else:
                search_obj.current_span.bot_rebar.point_loc.append(round(float(cell.value)*search_obj.current_span.length,1))
                search_obj.current_span.bot_rebar.selected.append(round(float(cell.offset(0,7).value),2))
        # define top rebar if area not 0
        if not str(cell.offset(0,6).value) == '0' and not cell.offset(0,6).value == None:
            # test if cb rebar is defined
            if search_obj.current_span.top_rebar == None:
                # point location, selected area
                search_obj.current_span.top_rebar = Rebar(round(float(cell.value)*search_obj.current_span.length,1),round(float(cell.offset(0,6).value),2))
            else:
                search_obj.current_span.top_rebar.point_loc.append(round(float(cell.value)*search_obj.current_span.length,1))
                search_obj.current_span.top_rebar.selected.append(round(float(cell.offset(0,6).value),2))

def optimize_gbs(spans):
    print('hey')
    
def main():
    file = "report.xlsx"
    wb = openpyxl.load_workbook(file)
    ws = wb.active

    get_input_geometry(ws)

main()


