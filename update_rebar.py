def update_req_areas(spans):
    for current_span in spans:
        # print(current_span.top_rebar_req)
        for rebar_element in current_span.top_rebar_elements:

            ###########################################
            assign_from_bar_schedule(rebar_element)
            ###########################################

            if not rebar_element.rebar_subtracted:
                for pair in current_span.top_rebar_req:
                    if rebar_element.start_loc <= pair[0] and rebar_element.end_loc >= pair[0]:
                        pair[1] = max(pair[1] - rebar_element.a_provided, 0)
                    rebar_element.rebar_subtracted = True
        # print(current_span.top_rebar_req, '\n')

def assign_from_bar_schedule(rebar):
    min_rebar_length = rebar.end_loc - rebar.start_loc
