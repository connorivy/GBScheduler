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
    def __init__(self, a_required=0, start_loc=100, end_loc=0, start_middle_loc=100, end_middle_loc=0, bar_size=0):
        self.a_required = a_required     
        self.bar_size = bar_size
        self.start_loc = start_loc
        self.end_loc = end_loc
        self.start_middle_loc = start_middle_loc
        self.end_middle_loc = end_middle_loc

    def get_area(self):
        self.bar_diameter = float(self.bar_size / 8)
        self.a_provided = float(math.pi * self.bar_diameter ** 2 / 4 )

    def get_rebar_info(self):
        self.get_area
        print('  area required:       ', self.a_required)
        # print('  area provided:       ', self.a_provided)
        print('  bar size:            ', self.bar_size)
        print('  start location:      ', self.start_loc)
        print('  end location:        ', self.end_loc)

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
        self.top_rebar_req = None
        self.bot_rebar_req = None
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
        if self.top_rebar_req == None:
            print('  -')
        else:
            self.top_rebar_req.get_rebar_req_info()

        print('\nbottom rebar:')
        if self.bot_rebar_req == None:
            print('  -')
        else:
            self.bot_rebar_req.get_rebar_req_info()
        
    # def effective_depth():
    #     return self.depth -
    
    # def max_shear_spacing():

class RebarRequirements:
    def __init__(self, point_loc, selected_area, bar_size=0, yield_strength=60000):
        self.point_loc = [point_loc]
        self.selected_area = [selected_area]
        self.a_required = 0
        self.start_loc = 0
        self.end_loc = 0
        self.bar_size = bar_size
        self.yield_strength = yield_strength

    def get_rebar_req_info(self):
        print('  location, selected_area')
        for x in range(len(self.point_loc)):
            print('    ', self.point_loc[x], ', ', self.selected_area[x])

        # print('  area required:       ', self.a_required)
        # print('  start location:      ', self.start_loc)
        # print('  end location:        ', self.end_loc)
        # print('  bar size:            ', self.bar_size)

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