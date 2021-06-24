def update_req_areas(top_bot_rebar, rebar_req, top_bot_index):
    # beam_run_info.get_rebar_req_info()

    # loop through all TOP rebar elements
    for rebar_element in top_bot_rebar:
        # make sure to only subtract the element's area from the required rebar one time
        if not rebar_element.rebar_subtracted:
            # rebar req is 2d list with [[location1, top selected area1, bot selected area1, span num1], [location2, top selected area2, bot selected area2, span num2]]
            for req in rebar_req:
                if req[0] < rebar_element.start_loc:
                    continue
                elif req[0] > rebar_element.end_loc:
                    rebar_element.rebar_subtracted = True
                    break
                else:
                    req[top_bot_index] = max(req[top_bot_index]-rebar_element.a_provided, 0)

    for req in rebar_req:
        if req[top_bot_index] == 0:
            continue
        else:
            print('NOT DONE')
            return False
    print('DONE')
    return True

def assign_from_bar_schedule(rebar):
    print('assign_from_bar_schedule')
