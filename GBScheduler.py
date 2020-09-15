from openpyxl import Workbook
import openpyxl
from striprtf.striprtf import rtf_to_text

class Span:
    def __init__(self, number, length, width, depth):
        self.number = number
        self.length = length
        self.width = width
        self.depth = depth
        self.shear_reinf_criteria = []

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
    shear_reinf_search = Search('12.1 Shear Calculation Envelope','Note: "Ratio" is calculated using paired shear (V) and moment (M) design values resulting in the lowest concrete capacity. For ACI and CSA codes, the lowest value of V*d/M is used.')

    row_count = ws.max_row
    # row_count = 30
    spans = []

    for row in ws.iter_rows(min_col=1, max_col=1, max_row = row_count):
        for cell in row:
            if not span_search.defined:
                new_span = look_for_grade_beam_data(cell, span_search, add_span)
                # print('new span', new_span, span_search.looking, span_search.defined)
                if new_span:
                    spans.append(new_span)

            if not shear_reinf_search.defined:
                new_span = look_for_grade_beam_data(cell, span_search, add_span)
                # print('new span', new_span, span_search.looking, span_search.defined)
                if new_span:
                    spans.append(new_span)
    
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

def add_shear_reinf_criteria(cell,spans):
    if 'SPAN' in str(cell.value):
        current_span = int(cell.value[-1])
    elif str(cell.value).replace('.','',1).isdigit():
        spans[current_span-1].shear_reinf_criteria.append(float(cell.offset(0,1)),float(cell.offset(0,6)))

def main():
    file = "report.xlsx"
    wb = openpyxl.load_workbook(file)
    ws = wb.active

    get_input_geometry(ws)

main()

