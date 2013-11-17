import utils
import numpy as np
from matplotlib import pyplot as plot
from matplotlib.colors import Normalize as norm
import time

def find_shots(params={}):
    """
    return all shots that match the passed in params
    """
    db = utils.get_db()
    shots = db.shots.find(params)
    return shots
    
def find_shots_center(x,y,radius=1.,params = {}):
    """
    returns all shots within a given radius of a center point, defined by
    x and y
    """
    x = float(x)
    y = float(y)
    radius = float(radius)
    db = utils.get_db()
    params['pos'] = {'$geoWithin': {'$center': [[x,y] , radius]}}
    shots = db.shots.find(params)
    return list(shots)
    
def fg_pct(shots):
    #print "%d shots" % len(shots)
    if shots:
        return len(filter(lambda x: x['made'], shots)) / float(len(shots))
    else:
        return -1

def fg_pct_by_pos(x,y,radius = 1):
    return fg_pct(find_shots_center(x,y,radius))

def prepare_shotchart_old(params={}):
    """
    loops through all x,y coords in the half court and computes fg pct
    """
    xs = []
    ys = []
    pcts = []
    attempts = []
    tups = []
    for x in range(-25,26):
        for y in range(-4,31):
            shots = find_shots_center(x,y,params = params)
            pct = fg_pct(shots)
            atts = len(shots)
            xs.append(x)
            ys.append(y)
            pcts.append(pct)
            attempts.append(atts)
            tups.append((x,y,pct,atts))
    return tups

@utils.timeit
def prepare_shotchart(params={}):
    shots = find_shots(params)
    pos2shots = {}
    most_common = -1
    for shot in shots:
        x = shot['x']
        y = shot['y']
        cur = pos2shots.get((x,y),[])
        cur.append(shot)
        pos2shots[(x,y)] = cur
        most_common = float(max(len(cur),most_common))

    tups = []
    max_y = 30 # longest pos on court to consider
    for pos,shots in pos2shots.items():
        x,y = pos
        if y > max_y:
            continue
        pct = fg_pct(shots)
        opacity = len(shots)/(0.2*most_common) # need some better scaling!
        tups.append((x,y,pct,opacity))
    return tups

def draw_shotchart(xs,ys,pct):
    plot.scatter(xs,ys,c=pct,marker='s',cmap=plot.cm.jet,norm=norm(vmin=0.25,vmax=0.85),s=100)
    plot.show()
    
def create_shotchart_plot(tups):
    # TODO return figure, not the plot object
    for (x,y,pct,op) in tups:
        plot.scatter(x,y,c=pct,alpha=op,marker='s',cmap=plot.cm.jet,norm=norm(vmin=0.25,vmax=0.7),s=50)
    return plot

def draw_shotchart(tups):
    plot = create_shotchart_plot(tups)
    plot.show()

if __name__ == '__main__':
    tups = prepare_shotchart2()
    pl = create_shotchart_plot(tups)
    pl.show()
