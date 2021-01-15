from Classes import Span
from Classes import RebarElement
from Classes import RebarRequirements
from Classes import Search

def get_input_geometry(ws):
    span_search = Search("2.1 Principal Span Data of Uniform Spans","2.7 Support Width and Column Data")
    long_reinf_search = Search('29 - DETAILED REBAR', 'Note: Reinforcement requirements for Initial condition are included in Service block. Reinforcement requirements for UBC combination, if selected, are included in Analysis block.')
    # shear_reinf_search = Search('12.1 Shear Calculation Envelope','Note: "Ratio" is calculated using paired shear (V) and moment (M) design values resulting in the lowest concrete capacity. For ACI and CSA codes, the lowest value of V*d/M is used.')

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

    # for x in spans:
    #     x.get_span_info()

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
        if str(cell.value).lower() == start_flag.lower():
            create_spans = True
        # if cell value == end flag then stop looking
        if str(cell.value).lower() == end_flag.lower():
            break

        if create_spans:
            # if the value is not empty, just spaces, or the start flag
            if value != '' and not value.isspace() and value.lower() != start_flag.lower():
                print('we made it through', value)
                # if the value is not a number then its a cantilever
                if not is_num(value):
                    if spans == []:
                        value = 'CL'
                    else:
                        value = 'CR'
                # returns span object with the following attributes
                # span number (or CR / CL if cantilever), length, width, depth
                spans.append(Span(value, float(ws.cell(row,3).value), float(ws.cell(row,4).value), float(ws.cell(row,5).value)))

    for x in spans:
        x.get_span_info()

    return spans

def get_input_geometry(wb):
    spans = []

def is_num(s):
    try:
        float(s)
        return True
    except ValueError:
        return False