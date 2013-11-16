import utils

def espn_game_id(game_id):
    return {'espn_game_id':game_id}

def distance(min_d,max_d):
    """
    shots with  min_d <= distance <= max_d
    """
    return {'distance':{'$gte':float(min_d),'$lte':float(max_d)}}

def min_distance(dist):
    """ shots with distance >= dist """
    return distance(dist,500)

def max_distance(dist):
    """ shots with distance >= dist """
    return distance(0,dist)

def distance_str(param_str):
    """
    takes a string in the format of min_dist,max_dist
    """
    min_d,max_d = param_str.split(',')
    return distance(min_d,max_d)

def angle(min_angle,max_angle):
    """
    shots with angle in range [min_angle,max_angle]
    """
    return {'angle': {'$gte':min_angle,'$lte':max_angle}}

def angle_str(param_str):
    """
    takes a string in the format of min_angle,max_angle
    """
    min_angle,max_angle = param_str.split(',')
    return angle(min_angle,max_angle)

def quarter(qtr):
    """
    quarter can be a single quarter or a list
    """
    if isinstance(qtr,list):
        return {'qtr':{'$in':qtr}}
    else:
        return {'qtr':qtr}

def quarter_str(param_str):
    """
    param str should be either a single number [1-4] or a cs list of numbers
    """
    return quarter(param_str.split(','))

def half(half):
    """ 1st or 2nd half. half is an int """
    if half == 1:
        return quarter([1,2])
    elif half == 2:
        return quarter([3,4])
    else:
        raise Exception('half needs to be an int, 1 or 2')
    
def home(is_home):
    if isinstance(is_home,str):
        if is_home.lower() == 'false' or is_home.lower() == 'f':
            is_home = False
        elif is_home.lower() == 'true' or is_home.lower() == 't':
            is_home = True
        else:
            raise Exception("'home' parameter expects true or false")
    return {'home':is_home}

def player_name(name):
    return {'espn_player_name_lower':name.lower()}

def player_first_name(name):
    return {'espn_first_name_lower':name.lower()}

def player_last_name(name):
    return {'espn_last_name_lower':name.lower()}

filters = {'espn_game_id': espn_game_id,
           'distance': distance_str,
           'min_distance': min_distance,
           'max_distance': max_distance,
           'angle': angle,
           'quarter': quarter_str,
           'half': half,
           'home': home,
           'name': player_name,
           'first_name': player_first_name,
           'last_name': player_last_name
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

def test():
    q_params = {'min_distance':'20',
                'quarter':'1',
                'last_name':'smith',
                'home':True}
    mongo_filter = merge_filters(q_params)

    db = utils.get_db()
    print db.shots.find(mongo_filter).count()

test()
