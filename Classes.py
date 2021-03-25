import math

class BeamRunInfo:
    def __init__(self):
        self.spans = []
        self.top_rebar = []
        self.bot_rebar = []
        self.rebar_req = []
        self.original_rebar_req = []
        self.all_spans_len = 0
        self.max_beam_depth = 0
        self.max_rebar_area = 0

    def get_rebar_req_info(self):
        print('  location, top_selected_area, bot_selected_area')
        for x in range(len(self.rebar_req)):
            print('    ', x, round(self.rebar_req[x][0],2), ', ', self.rebar_req[x][1], ', ', self.rebar_req[x][2], ', ', self.rebar_req[x][3])

    def get_span_num(self, loc):
        for index in range(len(self.spans)-1):
            if loc < self.spans[index].len_prev_spans:
                return index
        return len(self.spans)

class ParametersDefinedByUser:
    def __init__(self, fc, fy, stirrup_diam = .375, num_layers_of_top_reinf = 1, num_layers_of_bot_reinf = 1, psi_t = 1, psi_e = 1, lam = 1):
        
        self.fc = fc
        self.fy = fy
        self.stirrup_diam = stirrup_diam

        # per ACI 318-14 table 25.4.2.4
        self.psi_t = psi_t
        self.psi_e = psi_e
        self.lam = lam
        self.num_layers_of_top_reinf = num_layers_of_top_reinf
        self.num_layers_of_bot_reinf = num_layers_of_bot_reinf

class RebarElement:
    def __init__(self, a_required=0, start_loc=100, end_loc=0, bar_size=0, num_bars=0, min_num_bars=0):
        self.a_required = a_required
        self.bar_size = bar_size
        self.start_loc = start_loc
        self.end_loc = end_loc
        self.num_bars = num_bars
        self.min_num_bars = min_num_bars
        self.rebar_subtracted = False
        self.a_from_smaller = 0
        self.scheduled_shape = 'None'
        self.span_nums = []
        self.get_volume()

    def get_area(self):
        self.bar_diameter = float(self.bar_size / 8)
        self.a_provided = float(math.pi * self.bar_diameter ** 2 / 4 ) * self.num_bars

    def get_volume(self):
        self.get_area()
        self.volume = self.a_provided * (self.end_loc - self.start_loc) * 12
        return self.volume


    def get_rebar_info(self):
        print('  area required:       ', self.a_required)
        print('  area provided:       ', round(self.a_provided,2))
        print('  bar size:            ', self.bar_size)
        print('  num of bars:         ', self.num_bars)
        print('  start location:      ', self.start_loc)
        print('  end location:        ', self.end_loc)
        print('  area for bars under: ', self.a_from_smaller)
        print('  scheduled shape:     ', self.scheduled_shape)

    def development_len(self, user_input):
        bar_diameter = float(self.bar_size / 8)

        # per ACI 318-14 table 25.4.2.2
        if self.bar_size <= 6:
            constant = 20
        else:
            constant = 25
        ld = user_input.fy * user_input.psi_t * user_input.psi_e / (constant*user_input.lam*math.sqrt(user_input.fc)) * bar_diameter * (1.3/12)
        
        # print('development length', ld)
        return ld

class SingleSpan:
    def __init__(self, number, length, width, depth, len_prev_spans, fc=4000, cover_bot=3, cover_top=1.5, cover_side=2):
        self.number = number
        self.length = length
        self.width = width
        self.depth = depth
        self.fc = fc
        self.cover_bot = cover_bot
        self.cover_top = cover_top
        self.cover_side = cover_side
        self.top_rebar_req = []
        self.bot_rebar_req = []
        self.original_top_rebar_req = []
        self.original_bot_rebar_req = []
        self.top_rebar_elements = []
        self.bot_rebar_elements = []
        self.stirrups = None
        self.len_prev_spans = len_prev_spans

    def get_span_info(self):
        print('\n\nspan number:           ', self.number)
        print('********************************************************************')
        print('span length:           ', self.length)
        print('span width:            ', self.width)
        print('span depth:            ', self.depth)
        print('\ntop rebar:')
        
        if self.top_rebar_elements == []:
            print('  -')
        else:
            for rebar_element in self.top_rebar_elements:
                rebar_element.get_rebar_info()

        print('\nbottom rebar:')
        if self.bot_rebar_elements == []:
            print('  -')
        else:
            for rebar_element in self.bot_rebar_elements:
                rebar_element.get_rebar_info()

    def get_min_num_bars(self, user_input):

        # according to ACI 318-14 24.3.2.1
        fs = 2 / 3 * user_input.fy

        # according to ACI 318-14 table 24.3.2
        # the .625 is asumming a #5 stirrup
        max_spacing = min(15 * 40000/fs - 2.5 * (self.cover_side + user_input.stirrup_diam), 12 * 40000/fs)
        
        beam_width_no_cover = self.width - 2 * (self.cover_side + user_input.stirrup_diam)

        self.min_num_bars = math.ceil(beam_width_no_cover / max_spacing) + 1


        
    # def effective_depth():
    #     return self.depth -
    
    # def max_shear_spacing():

class VolDiff:
    def __init__(self, vol_diff, old_bar, new_large_bar, new_small_bar):
        self.vol_diff = vol_diff
        self.old_bar = old_bar
        self.new_large_bar = new_large_bar
        self.new_small_bar = new_small_bar

class RevGB:
    def __init__(self,num,string):
        string = string.strip()
        bad_chars = [',', ')', '(']
        for i in bad_chars:
            string = string.replace(i, '')
        string_list = string.split(' ')
        self.num = num
        self.start_x = float(string_list[0])
        self.start_y = float(string_list[1])
        self.start_z = float(string_list[2])
        self.end_x = float(string_list[3])
        self.end_y = float(string_list[4])
        self.end_z = float(string_list[5])
        self.width = float(string_list[6])
        self.depth = float(string_list[7])
        self.run = ''


class Stirrups:
    def __init__(self, a_required, start_loc, end_loc):
        self.a_required = a_required
        self.start_loc = start_loc
        self.end_loc = end_loc