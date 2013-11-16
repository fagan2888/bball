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
    return {'espn_player_name_lower':name.lower()}

def player_first_name(name):
    return {'espn_first_name_lower':name.lower()}

def player_last_name(name):
    return {'espn_last_name_lower':name.lower()}

# TODO: handle merging filters that have more than one param
# also think about how the api will be implemented.
# eg. for distance, do we want to pass in distance=min,max
#     or maybe distance=gt10

filters = {'espn_game_id':espn_game_id,
           'distance':distance,
           'angle':angle,
           'quarter':quarter,
           'home':home,
           'name':player_name,
           'first_name':player_first_name,
           'last_name':player_last_name
           }

def merge_filters(params):
    """
    combines all of the filters into one dictionary
    """
    filts = {}
    for k,v in params.items():
        if k in filters:
            cur_filt = filters[k](v)
            filts = dict(cur_filt,**filts)

    return filts
