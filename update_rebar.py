def update_req_areas(beam_run_info):
    # beam_run_info.get_rebar_req_info()

    # loop through all TOP rebar elements
    for rebar_element in beam_run_info.top_rebar:
        # make sure to only subtract the element's area from the required rebar one time
        if not rebar_element.rebar_subtracted:
            # rebar req is 2d list with [[location1, top selected area1, bot selected area1, span num1], [location2, top selected area2, bot selected area2, span num2]]
            for rebar_req in beam_run_info.rebar_req:
                if rebar_req[0] < rebar_element.start_loc:
                    continue
                elif rebar_req[0] > rebar_element.end_loc:
                    rebar_element.rebar_subtracted = True
                    break
                else:
                    rebar_req[1] = max(rebar_req[1]-rebar_element.a_provided, 0)

    for rebar_req in beam_run_info.rebar_req:
        if rebar_req[1] == 0:
            continue
        else:
            print('NOT DONE')
            return False
    print('DONE')
    return True

def assign_from_bar_schedule(rebar):
    print('assign_from_bar_schedule')
