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
    def __init__(self, a_required=0, start_loc=100, end_loc=0, bar_size=0):
        self.a_required = a_required     
        self.bar_size = bar_size
        self.start_loc = start_loc
        self.end_loc = end_loc
        self.num_bars = 0

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

class Span:
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
        self.lt_rebar = RebarElement()
        self.cb_rebar = RebarElement()
        self.ct_rebar = RebarElement()
        self.rt_rebar = RebarElement()
        self.stirrups = None

    def get_span_info(self):
        print('\n\nspan number:           ', self.number)
        print('********************************************************************')
        print('span length:           ', self.length)
        print('span width:            ', self.width)
        print('span depth:            ', self.depth)
        print('\ntop rebar:')
        if self.top_rebar_req == []:
            print('  -')
        else:
            self.get_rebar_req_info(self.top_rebar_req)

        print('\nbottom rebar:')
        if self.bot_rebar_req == []:
            print('  -')
        else:
            self.get_rebar_req_info(self.bot_rebar_req)

    def get_rebar_req_info(self, topbot):
        print('  location, selected_area')
        for x in range(len(topbot)):
            print('    ', topbot[x][0], ', ', topbot[x][1])

    def get_best_rebar_sizes(self):
        beam_width_no_cover = self.width - 2 * self.cover_side
        min_num_bars = math.ceil(beam_width_no_cover / 18) + 1

        long_reinf = [self.lt_rebar, self.ct_rebar, self.rt_rebar]
        # print('area', area)

        # loop through all bar sizes to find the most economic size
        for x in range(0,3):
             # set a value for the rebar remainder that will definitely be higher than all other remainder values 
            min_extra_rebar_area = 100

            for bar_num in range(6,12):
                area = long_reinf[x].a_required
                bar_area = float(math.pi * float(bar_num / 8)**2 / 4 )
                num_bars = max(math.ceil(area / bar_area), min_num_bars)
                # print('info', x, area, bar_num, num_bars)

                extra_rebar_area = num_bars * bar_area - area

                # print('xetra rebar area', extra_rebar_area)
                if extra_rebar_area < min_extra_rebar_area:
                    # print('ASSIGN BEST SIZE')
                    best_size = bar_num
                    num_best_bars = num_bars
                    min_extra_rebar_area = extra_rebar_area

            long_reinf[x].bar_size = best_size
            long_reinf[x].num_bars = num_best_bars
        
    # def effective_depth():
    #     return self.depth -
    
    # def max_shear_spacing():

class Stirrups:
    def __init__(self, a_required, start_loc, end_loc):
        self.a_required = a_required
        self.start_loc = start_loc
        self.end_loc = end_loc

class Search:
    def __init__(self, start_flag, end_flag):
        self.looking = False
        self.defined = False
        self.start_flag = start_flag
        self.end_flag = end_flag