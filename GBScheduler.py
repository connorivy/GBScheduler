from openpyxl import Workbook
import openpyxl
from striprtf.striprtf import rtf_to_text

class Span:
    def __init__(self, number, length, width, depth):
        self.number = number
        self.length = length
        self.width = width
        self.depth = depth

class Search:
    def __init__(self):
        self.looking = False
        self.defined = False

# this func
def word_to_excel():
    rtf = "report.rtf"
    text = rtf_to_text(rtf) 
    print(text)


def get_input_geometry(ws):
    span_search = Search()

    row_count = ws.max_row
    row_count = 30
    spans = []

    for row in ws.iter_rows(min_col=1, max_col=1, max_row = row_count):
        for cell in row:
            if not span_search.defined:
                # print('spans not defined')
                new_span = look_for_grade_beam_data(cell, span_search, "2.1 Principal Span Data of Uniform Spans","2.7 Support Width and Column Data", add_span)
                print('new span', new_span, span_search.looking, span_search.defined)
                if new_span:
                    spans.append(new_span)
    
    print(spans)
            

def look_for_grade_beam_data(cell, search_obj, start_flag, end_flag, func):
    if cell.value == start_flag:
        print('\n\n\n look = true \n\n\n')
        search_obj.looking = True

    elif cell.value == end_flag:
        print('\n\n\n look = false \n\n\n')
        search_obj.looking = False
        search_obj.defined = True

    if search_obj.looking:
        return func(cell)

def add_span(cell):
    if str(cell.value).replace('.','',1).isdigit():
        return Span(str(cell.value), str(cell.offset(0,2)), str(cell.offset(0,3)), str(cell.offset(0,3)))
    else:
        return 0


def main():
    file = "report.xlsx"
    wb = openpyxl.load_workbook(file, read_only=True)
    ws = wb.active

    get_input_geometry(ws)

main()

