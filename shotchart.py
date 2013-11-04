import utils
import numpy as np
from matplotlib import pyplot as plot
from matplotlib.colors import Normalize as norm
import time

def find_shots_center(x,y,radius=1.):
    """
    returns all shots within a given radius of a center point, defined by
    x and y
    """
    x = float(x)
    y = float(y)
    radius = float(radius)
    db = utils.get_db()
    params = {} # probs take in a params var with additional params
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

#TODO prepare a shotchart: for every position, compute pct, plot it!
def prepare_shotchart():
    """
    loops through all x,y coords in the half court and computes fg pct
    """
    xs = []
    ys = []
    pct = []
    opacity = []
    for x in range(-25,26):
        for y in range(-4,31):
            shots = find_shots_center(x,y)
            opacity.append(len(shots))
            xs.append(x)
            ys.append(y)
            pct.append(fg_pct(shots))
    return (xs,ys,pct,opacity)

def draw_shotchart(xs,ys,pct):
    plot.scatter(xs,ys,c=pct,marker='s',cmap=plot.cm.jet,norm=norm(vmin=0.25,vmax=0.85),s=100)
    plot.show()

xs,ys,pct,opacity = prepare_shotchart()
draw_shotchart(xs,ys,pct)


