from Classes import SingleSpan
from Classes import RebarElement
import copy

def define_spans(wb):
    # open the '(2)' tab in the excel sheet and extract the data for each span
    ws = wb.sheet_by_name('(2)')

    # loop over the second column. Once you find 'Span' then start looking for non-empy cells
    # note you cant just look for numbers because cantalievers are given by 'C'

    spans = []
    start_flag = 'span'
    end_flag = '2.7 Support Width and Column Data'
    create_spans = False

    for row in range(ws.nrows):
        # look in the first column bc the 0th column is blank
        cell = ws.cell(row,1)
        value = str(cell.value)

        # if cell value == start falg then start looking for nums 
        if value.lower() == start_flag.lower():
            create_spans = True
        # if cell value == end flag then stop looking
        if value.lower() == end_flag.lower():
            break

        if create_spans:
            # if the value is not empty, just spaces, or the start flag
            if value != '' and not value.isspace() and value.lower() != start_flag.lower():
                # if the value is not a number then its a cantilever
                if not is_num(value):
                    if spans == []:
                        value = 'CL'
                    else:
                        value = 'CR'
                # returns span object with the following attributes
                # span number (or CR / CL if cantilever), length, width, depth
                spans.append(SingleSpan(value, float(ws.cell(row,3).value), float(ws.cell(row,4).value), float(ws.cell(row,5).value)))

    return spans

def define_long_rebar(wb, spans):
    # open the '(29)' tab in the excel sheet and extract the data for each span
    ws = wb.sheet_by_name('(29)')

    num_consec_spaces = 0
    current_span = -1
    for row in range(ws.nrows):
        # look in the first column bc the 0th column is blank
        cell = ws.cell(row,1)
        value = str(cell.value)

        # start with span number -1 (which doesn't exists) and everytime you find two consecutive cells that are empty, go to the next span
        if value == '' or value.isspace():
            num_consec_spaces += 1
            if num_consec_spaces == 2:
                current_span += 1
            # jump ahead to next iteration of the loop
            continue
        else:
            num_consec_spaces = 0

        if is_num(value):
            spans[current_span].top_rebar_req.append([float(value),float(ws.cell(row,7).value)])
            spans[current_span].bot_rebar_req.append([float(value),float(ws.cell(row,8).value)])

def finalize_spans(spans):
    for current_span in spans:
        # make a deep copy of the original top and bottom rebar so they never change
        current_span.original_top_rebar_req = copy.deepcopy(current_span.top_rebar_req)
        current_span.original_bot_rebar_req = copy.deepcopy(current_span.bot_rebar_req)
        current_span.get_min_num_bars()

def is_num(s):
    try:
        float(s)
        return True
    except ValueError:
        return False