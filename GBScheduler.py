from openpyxl import Workbook
import openpyxl
from striprtf.striprtf import rtf_to_text

class Span:
    def __init__(self, number, length, width, depth, cover_bot=3, cover_top=1.5, cover_side=2, stirrup_size=3, top_bar_size=0,bot_bar_size=0):
        self.number = number
        self.length = length
        self.width = width
        self.depth = depth
        self.cover_bot = cover_bot
        self.cover_top = cover_top
        self.cover_side = cover_side
        self.stirrup_size = stirrup_size
        self.top_bar_size = top_bar_size
        self.bot_bar_size = bot_bar_size
        self.shear_reinf = []

    # def effective_depth():
    #     return self.depth -
    
    # def max_shear_spacing():

class Rebar:
    def __init__(self, location, a_req, start_loc, end_loc):
        self.location = location
        self.a_req = a_req
        self.start_loc = start_loc
        self.end_loc = end_loc

class Search:
    def __init__(self, start_flag, end_flag):
        self.looking = False
        self.defined = False
        self.start_flag = start_flag
        self.end_flag = end_flag

# this func
def word_to_excel():
    rtf = "report.rtf"
    text = rtf_to_text(rtf) 
    print(text)


def get_input_geometry(ws):
    span_search = Search("2.1 Principal Span Data of Uniform Spans","2.7 Support Width and Column Data")
    long_reinf_search = Search('10.1.1 Total Strip Required Rebar', '10.2 Provided Rebar')
    shear_reinf_search = Search('12.1 Shear Calculation Envelope','Note: "Ratio" is calculated using paired shear (V) and moment (M) design values resulting in the lowest concrete capacity. For ACI and CSA codes, the lowest value of V*d/M is used.')

    row_count = ws.max_row
    # row_count = 30
    spans = []

    for row in ws.iter_rows(min_col=1, max_col=1, max_row = row_count):
        for cell in row:
            if not span_search.defined:
                new_span = look_for_grade_beam_data(cell, span_search, add_span)
                if new_span:
                    spans.append(new_span)

            if not long_reinf_search.defined:
                new_span = look_for_grade_beam_data(cell, span_search, add_span)
                if new_span:
                    spans.append(new_span)

            # if not shear_reinf_search.defined:
            #     new_span = look_for_grade_beam_data(cell, span_search, add_span)
            #     if new_span:
            #         spans.append(new_span)
    
    print(spans)
            

def look_for_grade_beam_data(cell, search_obj, func):
    if cell.value == search_obj.start_flag:
        print('\n\n\n look = true \n\n\n')
        search_obj.looking = True
        return

    elif cell.value == search_obj.end_flag:
        print('\n\n\n look = false \n\n\n')
        search_obj.looking = False
        search_obj.defined = True
        return

    if search_obj.looking:
        return func(cell)

def add_span(cell):
    if str(cell.value).replace('.','',1).isdigit():
        return Span(str(cell.value), str(cell.offset(0,2)), str(cell.offset(0,3)), str(cell.offset(0,3)))
    else:
        return 0

def add_long_reinf_criteria(cell,spans):
    if str(cell.value).replace('.','',1).isdigit():
        current_span = spans[int(cell.value[-1])-1]
    
    if str(cell.offset(0,1)) == 'TOP' or str(cell.offset(0,1)) == 'BOT':
        current_span.rebar.append(Rebar(str(cell.offset(0,1).value),float(cell.offset(0,4).value),float(cell.offset(0,2).value),float(cell.offset(0,3).value)))
        
# def add_shear_reinf_criteria(cell,spans):
#     if 'SPAN' in str(cell.value):
#         current_span = int(cell.value[-1])
#     elif str(cell.value).replace('.','',1).isdigit():
#         spans[current_span-1].shear_reinf_criteria.append(float(cell.offset(0,1)),float(cell.offset(0,6)))

def main():
    file = "report.xlsx"
    wb = openpyxl.load_workbook(file)
    ws = wb.active

    get_input_geometry(ws)

main()

