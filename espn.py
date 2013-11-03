from datetime import datetime, timedelta
from dateutil import parser as dateparser
import requests
import utils
import re
from bs4 import BeautifulSoup as bs
import pdb

DT_FORMAT = '%Y%m%d'

def _get_game_ids_online():
    db = utils.get_db()
    
    url = "http://scores.espn.go.com/nba/scoreboard"
    game_ids = set()
    last = _latest_game_day()
    for dt in utils.day_gen(str(last)):
        day_str = dt.strftime(DT_FORMAT)
        try:
            resp = requests.get(url,params={'date':day_str})
            cur_ids = re.findall('href="/nba/playbyplay\?gameId=(\d*)',resp.text)
            game_ids.update(cur_ids)

            for game_id in cur_ids:
                doc = {'date':dt,'espn_game_id':game_id}
                db.games.save(doc)

        except Exception as e:
            pdb.set_trace()
            
    return game_ids

def _latest_game_day():
    db = utils.get_db()
    last_day = dateparser.parse('2012-10-30')
    games = db.games.find().sort('date',-1)
    if not games:
        return None
    return games[0].get('date')
    
def _update_game_ids():
    db = utils.get_db()
    game_ids = _get_game_ids_online()

#_get_game_ids_online()
