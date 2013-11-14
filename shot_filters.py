filters = {'espn_game_id':espn_game_id,
           'distance':distance,
           'angle':angle,
           'quarter':quarter,
           'home':home}

def espn_game_id(game_id):
    return {'espn_game_id':game_id}

def distance(distance,op):
    """
    op is for operator, takes 'gt','lt','gte','lte'
    """
    if op not in ['gt','lt','gte','lte']:
        raise Exception("op needs to be in ['gt','lt','gte','lte']")
    return {'distance':{'$'+op:distance}}

def angle(min_angle,max_angle):
    """
    shots with angle in range [min_angle,max_angle]
    """
    return {'angle': {'$gte':min_angle,'$lte':max_angle}}

def quarter(qtr):
    """
    quarter can be a single quarter or a list
    """
    if isinstance(qtr,list):
        return {'qtr':{'$in':qtr}}
    else:
        return {'qtr':qtr}

def home(is_home):
    return {'home':is_home}

def player_name(name):
    """
    #TODO first, last, both
    """
    pass
