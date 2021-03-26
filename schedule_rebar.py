import copy

def schedule_rebar(beam_run_info):
    # print('schedule rebar')
    num_spans = len(beam_run_info.spans)
    schedule_values = []
    center_top_bars = '-'
    center_bottom_bars = '-'

    for current_span_num in range(num_spans):
        current_span = beam_run_info.spans[current_span_num]

        # ASSUMPTION - only single spans have top center rebar
        if num_spans == 1:
            loc = current_span.mid_span_loc
            center_bottom_bars = schedule_bot_rebar(beam_run_info, loc, current_span)
            center_top_bars = schedule_top_rebar(beam_run_info, loc, current_span)

        else:
            if current_span_num == 0:
                loc = current_span.len_prev_spans
                left_end_top_bars = schedule_top_rebar(beam_run_info, loc, current_span)
            else:
                left_end_top_bars = '-'

            loc = current_span.mid_span_loc
            center_bottom_bars = schedule_bot_rebar(beam_run_info, loc, current_span)

            loc = current_span.len_prev_spans + current_span.length
            right_end_top_bars = schedule_top_rebar(beam_run_info, loc, current_span)
        schedule_values.append([current_span.width, current_span.depth, left_end_top_bars, center_bottom_bars, center_top_bars, right_end_top_bars])
    
    return schedule_values

def schedule_top_rebar(beam_run_info, loc, current_span):
    # print('schedule_top_rebar')
    rebar_elements = get_rebar_at_location(beam_run_info.top_rebar, loc)
    top_bars = []
    for bar in rebar_elements:
        first_span_req_len = min(bar.end_loc - loc, current_span.length / 2)
        L3_req_len = bar.end_loc - loc
        L1_req_len = loc - bar.start_loc

        # if only one span
        if current_span.prev_span_len == 0 and current_span.next_span_len == 0:
            top_bars.append([bar.num_bars, bar.bar_size, 'J'])
        # if location is within 1 foot of start of bar, assume loc == start of bar aka loc == start of beam run
        elif loc <= 1:
            top_bars.append(end_of_beam_shapes(L3_req_len, loc, current_span, bar))
        # if location is within 1 foot of end of bar, assume loc == end of bar aka loc == end of beam run
        elif L3_req_len <= 1:
            top_bars.append(end_of_beam_shapes(L1_req_len, loc, current_span, bar))
        else:
            top_bars.append(over_support_shapes(L1_req_len, L3_req_len, loc, current_span, bar))
        
    print(get_schedule_text(top_bars))
    print()

    return get_schedule_text(top_bars)



def schedule_bot_rebar(beam_run_info, loc, current_span):
    # print('schedule_bot_rebar')
    rebar_elements = get_rebar_at_location(beam_run_info.bot_rebar, loc)
    bot_bars = []
    for bar in rebar_elements:
        
        L2_req_len = max(loc - bar.start_loc - current_span.length / 2, 0)
        L3_req_len = max(bar.end_loc - loc - current_span.length / 2, 0)
        L1_back = min(current_span.length / 2, loc - bar.start_loc)
        L1_front = min(current_span.length / 2, bar.end_loc - loc)

        print(bar.start_loc, bar.end_loc, bar.num_bars)
        print(L1_front,L3_req_len)

        # if only one span
        if current_span.prev_span_len == 0 and current_span.next_span_len == 0:
            bot_bars.append([bar.num_bars, bar.bar_size, 'J'])
        # if location is part of first span
        elif current_span.prev_span_len == 0:
            bot_bars.append(end_mid_span_shapes(L1_back, L1_front, L2_req_len, L3_req_len, loc, current_span, bar))
        # if location is part of last span
        elif current_span.next_span_len == 0:
            bot_bars.append(end_mid_span_shapes(L1_back, L1_front, L2_req_len, L3_req_len, loc, current_span, bar))
        else:
            bot_bars.append(mid_span_shapes(L1_back, L1_front, L2_req_len, L3_req_len, loc, current_span, bar))
        
    print(get_schedule_text(bot_bars))
    print()

    return get_schedule_text(bot_bars)


def get_rebar_at_location(rebar_list, loc):
    # print('get_rebar_at_location')
    elements = []
    for bar in rebar_list:
        if bar.start_loc <= loc <= bar.end_loc:
            elements.append(bar)

    return elements

def end_of_beam_shapes(L1_req_len, loc, current_span, bar):
    print('end of beam shapes')
    half_L1_plus_15_bar_diam = .5*current_span.length + 15 * bar.bar_diameter / 12
    one_third_L1 = .33 * current_span.length
    one_fourth_L1 = .25 * current_span.length

    # shape, len required into prev span, len required into next span
    if not loc:
        B = ['B', 0, half_L1_plus_15_bar_diam]
        F = ['F', 0, one_fourth_L1]
        S = ['S', 0, one_third_L1]

        return get_shape([B,F,S], bar, loc, len_front_req=L1_req_len, default=B)

    else:
        B = ['B', half_L1_plus_15_bar_diam, 0]
        F = ['F', one_fourth_L1, 0]
        S = ['S', one_third_L1, 0]

        return get_shape([B,F,S], bar, loc, len_back_req=L1_req_len, default=B)

def over_support_shapes(L1_req_len, L3_req_len, loc, current_span, bar):
    # print('over support shapes')
    half_L1_plus_15_bar_diam = .5 * current_span.length + 15 * bar.bar_diameter / 12
    half_L3_plus_15_bar_diam = .5 * current_span.next_span_len + 15 * bar.bar_diameter / 12
    one_third_L1_or_L3 = .33 * max(current_span.length, current_span.next_span_len)
    one_fourth_L1_or_L3 = .25 * max(current_span.length, current_span.next_span_len)

    # shape, len required into prev span, len required into next span
    A = ['A', half_L1_plus_15_bar_diam, half_L3_plus_15_bar_diam]
    E = ['E', one_fourth_L1_or_L3, one_fourth_L1_or_L3]
    H = ['H', one_third_L1_or_L3, one_third_L1_or_L3]

    shapes = [A, E, H]
    return get_shape(shapes, bar, loc, len_back_req=L1_req_len, len_front_req=L3_req_len, default=A)

def end_mid_span_shapes(L1_back, L1_front, L2_req_len, L3_req_len, loc, current_span, bar):
    print('end mid_span_shapes')
    half_curr_span = current_span.length / 2
    one_third_L1_or_L3 = .33 * max(current_span.length, current_span.next_span_len)
    one_half_L3_plus_15_bar_diam = current_span.next_span_len / 2 + 15 * bar.bar_diameter / 12
    thirty_bar_diam = 30 * bar.bar_diameter / 12

    # shape, len req backwards, len req forward
    if current_span.prev_span_len == 0:
        D = ['D', half_curr_span, half_curr_span + one_third_L1_or_L3]
        G = ['G', half_curr_span, half_curr_span + one_half_L3_plus_15_bar_diam]
        P = ['P', half_curr_span, half_curr_span]
        T = ['T', half_curr_span, half_curr_span + thirty_bar_diam]

        return get_shape([D, G, P, T], bar, loc, len_back_req=L1_back + L2_req_len, len_front_req=L1_front + L3_req_len, default=T)
    
    # shape, len req backwards, len req forward    
    else:
        D = ['D', half_curr_span + one_third_L1_or_L3, half_curr_span]
        G = ['G', half_curr_span + one_half_L3_plus_15_bar_diam, half_curr_span]
        P = ['P', half_curr_span, half_curr_span]
        T = ['T', half_curr_span + thirty_bar_diam, half_curr_span]

        return get_shape([D, G, P, T], bar, loc, len_back_req=L1_back + L2_req_len, len_front_req=L1_front + L3_req_len, default=T)

    shapes = [D, G, P, T]

def mid_span_shapes(L1_back, L1_front, L2_req_len, L3_req_len, loc, current_span, bar):
    print('mid_span_shapes')
    half_curr_span = current_span.length / 2
    one_third_L1_or_L2 = .33 * max(current_span.length, current_span.prev_span_len)
    one_third_L1_or_L3 = .33 * max(current_span.length, current_span.next_span_len)
    one_eighth_L1 = 1/8 * current_span.length
    thirty_bar_diam = 30 * bar.bar_diameter / 12
    one_half_L1_plus_15_bar_diam = current_span.prev_span_len / 2 + 15 * bar.bar_diameter / 12
    one_half_L3_plus_15_bar_diam = current_span.next_span_len / 2 + 15 * bar.bar_diameter / 12
    
    # shape, len req backwards, len req forward
    C = ['C', half_curr_span + one_third_L1_or_L2, half_curr_span + one_third_L1_or_L3]
    K = ['K', half_curr_span - one_eighth_L1, half_curr_span -one_eighth_L1]
    L = ['L', half_curr_span, half_curr_span + thirty_bar_diam]
    M = ['M', half_curr_span, half_curr_span]
    N = ['N', half_curr_span + thirty_bar_diam, half_curr_span + thirty_bar_diam]
    U = ['U', half_curr_span, half_curr_span - one_eighth_L1]
    # V = ['P', half_curr_span, half_curr_span]
    Y = ['P', half_curr_span + one_half_L1_plus_15_bar_diam, half_curr_span + one_half_L3_plus_15_bar_diam]

    shapes = [C, K, L, M, N, U, Y]
    return get_shape(shapes, bar, loc, len_back_req=L1_back + L2_req_len, len_front_req=L1_front + L3_req_len, default=N)

def get_shape(shapes, bar, loc, len_back_req=0, len_front_req=0, default=[]):
    # print('get shape')
    best_shape = 'Z'
    min_len = 10000
    # len_back = 0
    for shape in shapes:
        if shape[1] < len_back_req:
            continue
        if shape[2] < len_front_req:
            continue
        temp = copy.copy(min_len)
        min_len = min(min_len, shape[1] + shape[2])
        if min_len != temp:
            best_shape = shape[0]
            len_back = shape[1]
            len_front = shape[2]

    bar.scheduled_shape = best_shape

    try:
        dummy = len_back
    except:
        print('bar %d continues into more spans' %(bar.idnum))

        bar.start_loc = loc + default[2]
        bar.scheduled_shape = default[0]

        return [bar.num_bars, bar.bar_size, bar.scheduled_shape]

    if loc - bar.start_loc > len_back:
        print('bar %d doesnt reach back enough. This is a problem' %(bar.idnum))
        # bar.start_loc += min_len
    elif bar.end_loc - loc > len_front:
        print('bar %d continues into more spans' %(bar.idnum))
        bar.start_loc = loc + len_front
    else:
        print('bar %d is scheduled' %(bar.idnum))
        bar.start_loc = 0
        bar.end_loc = 0 

    # print('%d-%d-%s'  %(bar.num_bars, bar.bar_size, bar.scheduled_shape))
    return [bar.num_bars, bar.bar_size, bar.scheduled_shape]

def get_schedule_text(bars):
    # print('get scheduled text')
    bar_text = ''
    for x in range(len(bars)):
        for y in range(len(bars)):
            if x == y:
                continue
            if bars[x][1] == bars[y][1] and bars[x][2] == bars[y][2]:
                bars[x][0] += bars[y][0]
                bars[y][2] = 'Z'
    for bar in bars:
        if bar[2] != 'Z':
            if bar_text == '' :
                bar_text = '%d-%d-%s'  %(bar[0], bar[1], bar[2])
            else:
                bar_text += ', ' + '%d-%d-%s'  %(bar[0], bar[1], bar[2])

    return bar_text