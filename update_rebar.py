def update_req_areas(beam_run_info):
    for rebar_element in beam_run_info.top_rebar:
        if not rebar_element.rebar_subtracted:
            for rebar_req in beam_run_info.rebar_req:
                if rebar_req[0] < rebar_element.start_loc:
                    continue
                elif rebar_req[0] > rebar_element.end_loc:
                    rebar_element.rebar_subtracted = True
                    break
                else:
                    rebar_req[1] = max(rebar_req[1]-rebar_element.a_provided, 0)
    # print(beam_run_info.rebar_req)

def assign_from_bar_schedule(rebar):
    min_rebar_length = rebar.end_loc - rebar.start_loc
