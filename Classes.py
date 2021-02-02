import math

class ParamatersDefinedByUser:
    def __init__(self, fc, yield_strength, psi_t, psi_e, lam):
        self.fc = fc
        self.yield_strength = yield_strength

        # per ACI 318-14 table 25.4.2.4
        self.psi_t = psi_t
        self.psi_e = psi_e
        self.lam = lam

class RebarElement:
    def __init__(self, a_required=0, start_loc=100, end_loc=0, bar_size=0, num_bars=0):
        self.a_required = a_required
        self.bar_size = bar_size
        self.start_loc = start_loc
        self.end_loc = end_loc
        self.num_bars = num_bars
        self.rebar_subtracted = False

    def get_area(self):
        self.bar_diameter = float(self.bar_size / 8)
        self.a_provided = float(math.pi * self.bar_diameter ** 2 / 4 ) * self.num_bars

    def get_rebar_info(self):
        self.get_area()
        print('  area required:       ', self.a_required)
        print('  area provided:       ', round(self.a_provided,2))
        print('  bar size:            ', self.bar_size)
        print('  num of bars:         ', self.num_bars)
        print('  start location:      ', self.start_loc)
        print('  end location:        ', self.end_loc)

    def development_len(self, user_input):
        bar_diameter = float(self.bar_size / 8)

        # per ACI 318-14 table 25.4.2.2
        if self.bar_size <= 6:
            constant = 20
        else:
            constant = 25
        ld = user_input.yield_strength * user_input.psi_t * user_input.psi_e / (constant*user_input.lam*math.sqrt(user_input.fc)) * bar_diameter * (1.3/12)
        
        # print('development length', ld)
        return ld

class SingleSpan:
    def __init__(self, number, length, width, depth, fc=4000, cover_bot=3, cover_top=1.5, cover_side=2):
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

    def get_rebar_req_info(self, topbot):
        print('  location, selected_area')
        for x in range(len(topbot)):
            print('    ', topbot[x][0], ', ', topbot[x][1])

    def get_min_num_bars(self):
        # no more than 18" between bars
        beam_width_no_cover = self.width - 2 * self.cover_side
        self.min_num_bars = math.ceil(beam_width_no_cover / 18) + 1

        
    # def effective_depth():
    #     return self.depth -
    
    # def max_shear_spacing():

class VirtualSingleSpan:
    def __init__(self, left, top, right, bot):
        self.left = left
        self.top = top
        self.right = right
        self.bot = bot

class Stirrups:
    def __init__(self, a_required, start_loc, end_loc):
        self.a_required = a_required
        self.start_loc = start_loc
        self.end_loc = end_loc