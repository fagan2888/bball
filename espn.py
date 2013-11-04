from datetime import datetime, timedelta
from dateutil import parser as dateparser
import requests
import utils
import re
from bs4 import BeautifulSoup as bs
from hashlib import md5
import math
import sys

import pdb

DT_FORMAT = '%Y%m%d'

def _gen_shot_key(shot_id,game_id):
    """
    generate a mongo key for a shot.
    both game_id and shot_id should be strings
    """
    return md5("game_id:%s shot_id:%s " % (game_id,shot_id)).hexdigest()

def _gen_game_key(game_id):
    """
    generates a mongo key for a game_id
    """
    return md5("game_id:%s" % game_id).hexdigest()

def insert_game_ids():
    """
    iterates through days and finds all espn game_ids from those days.
    inserts them into mongo db.
    """
    #TODO: pass in progress callback
    db = utils.get_db()
    
    url = "http://scores.espn.go.com/nba/scoreboard"
    game_ids = set()
    last = _latest_game_day()
    for dt in utils.day_gen(last):
        day_str = dt.strftime(DT_FORMAT)
        try:
            resp = requests.get(url,params={'date':day_str})
            cur_ids = re.findall('href="/nba/playbyplay\?gameId=(\d*)',resp.text)
            game_ids.update(cur_ids)

            for game_id in cur_ids:
                mongo_game_id = _gen_game_key(game_id)
                doc = {'date':dt,'espn_game_id':game_id,'_id':mongo_game_id}
                db.games.save(doc)

        except Exception as e:
            pdb.set_trace()
    
    return

def get_game_ids_db():
    """
    looks up game_ids from db
    """
    db = utils.get_db()
    game_docs = db.games.find({},{'espn_game_id':True})
    return [game['espn_game_id'] for game in game_docs]

def _latest_game_day():
    db = utils.get_db()
    last_day = dateparser.parse('2012-10-30')
    games = db.games.find().sort('date',-1)
    if games.count() == 0:
        return None
    return str(games[0].get('date'))

def _get_shots(game_id):
    """
    looks up the shots from a given game id.
    """
    url = "http://sports.espn.go.com/nba/gamepackage/data/shot"
    params = {'gameId':game_id}
    resp = requests.get(url,params = params)
    soup = bs(resp.text)
    shots = []
    
    for shot in soup.find_all('shot'):
        shots.append(_format_shot(shot,game_id))

    return shots

def _format_shot(shot,game_id):
    """
    takes a bs element.Tag object that stores shot info and returns a dict
    """
    d = {}
    d['espn_shot_id'] = shot['id']
    d['espn_player_id'] = shot['pid']
    d['qtr'] = shot['qtr']
    if shot['t'] == 'h':
        d['home'] = True
    elif shot['t'] == 'a':
        d['home'] = False
    else:
        raise Exception("I expect the team to be 'h' for home or 'a' for away")

    # normalize shot pos
    (x,y) = _transform_coords(shot['x'],shot['y'],d['home'])
    d['pos'] = (x,y)
    d['x'] = x
    d['y'] = y

    #process shot positions
    _process_shot_pos(d)

    if shot['made'] == 'true':
        d['made'] = True
    elif shot['made'] == 'false':
        d['made'] = False
    else:
        pdb.set_trace()

    d['espn_player_name'] = shot['p']
    d['espn_description'] = shot['d']

    mongo_shot_id = _gen_shot_key(shot['id'],game_id)
    mongo_game_id = _gen_game_key(game_id)
    d['game_id'] = mongo_game_id
    d['espn_game_id'] = game_id # possibly overkill
    d['_id'] = mongo_shot_id
    
    return d

def _get_shot_dist(x,y):
    """
    returns the distance from the hoop
    """
    return (x**2+y**2)**0.5

def _get_shot_angle(x,y):
    """
    probably stupid, but calculate shot angle
    """
    if x == 0 and y == 0:
        quotient = 0 # idk if this is mathematically correct
    elif y == 0:
        quotient = float('inf')
    else:
        quotient = float(x)/y
        
    return math.atan(quotient) / (math.pi/2.) * 90

def _get_shot_zone(x,y):
    """
    returns a 'zone' that corresponds to the chart here:
    http://stats.nba.com/shotcharts.html
    """
    #TODO draw out geo boundaries for these regions!
    pass

def _process_shot_pos(shot):
    """
    prepare info related to shot distance for shot object
    """
    (x,y) = shot['pos']

    shot['distance']  = _get_shot_dist(x,y)
    shot['angle'] = _get_shot_angle(x,y)
    
def _transform_coords(x,y,is_home):
    """
    espn plots all shots on an absolute court, not relative to the basket
    that the shot is attempted on. this function corrects the positions s.t.
    they are now relative to the basket that the shot is attempted on.

    x is distance from the hoop left to right. y is distance from the hoop
    front to back.
    
    (0,0) corresponds to the basket, (-25,-5) corresponds to a jumper from the
    left-most corner. (the rim is ~6 feet from the baseline).

    the court is 50 x 94 ft
    """
    x = float(x)
    y = float(y)
    if is_home:
        x = 50 - x
        y = 94 - y

    # sanity check
    if not (x >= 0 and y >= 0):
        # error with data
        pass

    x = abs(50-x)-25
    y = y-6

    return (x,y)

def _insert_shots(game_id):
    db = utils.get_db()
    if db.shots.find({'espn_game_id':game_id}).count():
       return 
    shots = _get_shots(game_id)
    for shot in shots:
        db.shots.save(shot)

def insert_all_shots():
    # TODO: pass in progress callback
    game_ids = get_game_ids_db()
    
    cnt = 0

    for game_id in game_ids:
        _insert_shots(game_id)

        if cnt % 10 == 0:
            sys.stdout.write("\rshots inserted for %d games" % cnt)
            sys.stdout.flush()

        cnt+=1

def populate_db():
    insert_game_ids()
    insert_all_shots()

if __name__ == '__main__':
    insert_all_shots()
