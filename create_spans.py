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
    len_prev_spans = 0
    max_beam_depth = 0

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
                spans.append(SingleSpan(value, float(ws.cell(row,3).value), float(ws.cell(row,4).value), float(ws.cell(row,5).value),len_prev_spans))
                len_prev_spans += float(ws.cell(row,3).value)
                max_beam_depth = max(max_beam_depth, float(ws.cell(row,5).value))

    return spans, max_beam_depth, len_prev_spans

def define_long_rebar(wb, beam_run_info):
    # open the '(29)' tab in the excel sheet and extract the data for each span
    ws = wb.sheet_by_name('(29)')

    num_consec_spaces = 0
    current_span_num = -1
    max_rebar_area = 0
    for row in range(ws.nrows):
        # look in the first column bc the 0th column is blank
        cell = ws.cell(row,1)
        value = str(cell.value)

        # start with span number -1 (which doesn't exists) and everytime you find two consecutive cells that are empty, go to the next span
        if value == '' or value.isspace():
            num_consec_spaces += 1
            if num_consec_spaces == 2:
                current_span_num += 1
            # jump ahead to next iteration of the loop
            continue
        else:
            num_consec_spaces = 0

        if is_num(value):
            current_span = beam_run_info.spans[current_span_num]
            loc = current_span.len_prev_spans + current_span.length * float(value)
            # use the minimum number of number 6 bars as a minimum area
            beam_run_info.rebar_req.append([loc, float(ws.cell(row,7).value), float(ws.cell(row,8).value), current_span_num])
            top = max(float(ws.cell(row,7).value), current_span.min_num_bars * .44)
            bot = max(float(ws.cell(row,8).value), current_span.min_num_bars * .44)
            beam_run_info.max_rebar_area = max(beam_run_info.max_rebar_area, top, bot)
            # beam_run_info.rebar_req.append([loc, top, bot, current_span_num])

    # make a deep copy of the original top and bottom rebar so they never change
    beam_run_info.original_rebar_req = copy.deepcopy(beam_run_info.rebar_req)

def finalize_spans(beam_run_info):
    len_prev_spans = 0
    max_beam_depth = 0
    for current_span in beam_run_info.spans:
        max_beam_depth = max(max_beam_depth, current_span.depth)
        current_span.len_prev_spans = len_prev_spans
        len_prev_spans += current_span.length
        current_span.get_min_num_bars()

    beam_run_info.max_beam_depth = max_beam_depth
    beam_run_info.all_spans_len = len_prev_spans

    # make a deep copy of the original top and bottom rebar so they never change
    beam_run_info.original_rebar_req = copy.deepcopy(beam_run_info.rebar_req)
    print(beam_run_info.rebar_req)
    print('\n\n\n\n', beam_run_info.original_rebar_req)

def is_num(s):
    try:
        float(s)
        return True
    except ValueError:
        return False