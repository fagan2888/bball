import utils
import numpy as np
import pdb
import time
import StringIO

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
    for shot in shots:
        x = shot['x']
        y = shot['y']
        cur = pos2shots.get((x,y),[])
        if shot['made']:
            cur.append(1)
        else:
            cur.append(0)
        pos2shots[(x,y)] = cur

    xs = []
    ys = []
    pcts = []
    ops = []
    filter_width = 1 # number of adjacent locations to check
    for x in range(-25,26):
        for y in range(-5,31):
            shots = []
            for x_offset in range(-filter_width, filter_width+1):
                for y_offset in range(-filter_width, filter_width+1):
                    shots += pos2shots.get((x+x_offset,y+y_offset),[])
            count = len(shots)
            if count == 0:
                continue
            pct = float(sum(shots))/count
            xs.append(x)
            ys.append(y)
            pcts.append(pct)
            ops.append(count)

    max_count = float(max(ops))
    for i in range(len(ops)):
        ops[i]/=(0.5*max_count)

    return zip(xs,ys,pcts,ops)

def draw_shotchart(xs,ys,pct):
    from matplotlib import pyplot as plot
    from matplotlib.colors import Normalize as norm
    plot.scatter(xs,ys,c=pct,marker='s',cmap=plot.cm.jet,norm=norm(vmin=0.25,vmax=0.85),s=100)
    plot.show()
    
def create_shotchart_plot(tups):
    from matplotlib import pyplot as plot
    from matplotlib.colors import Normalize as norm
    for (x,y,pct,op) in tups:
        plot.scatter(x,y,c=pct,alpha=op,marker='s',cmap=plot.cm.jet,norm=norm(vmin=0.25,vmax=0.7),s=50)
    return plot


#TODO: fix axes. label pcts. work on opacity scaling.
@utils.timeit
def create_shotchart_png(tups):
    """
    returns a stringIO object that stores the binary PNG data for a plot
    """
    from matplotlib import pyplot as plot
    from matplotlib.colors import Normalize as norm
    for (x,y,pct,op) in tups:
        plot.scatter(x,y,c=pct,alpha=op,marker='s',cmap=plot.cm.jet,norm=norm(vmin=0.25,vmax=0.7),s=50)
    out = StringIO.StringIO()
    plot.savefig(out,ext='png')
    plot.close()
    return out
    

def draw_shotchart(tups):
    plot = create_shotchart_plot(tups)
    plot.show()

if __name__ == '__main__':
    tups = prepare_shotchart()
    pl = create_shotchart_plot(tups)
    pl.show()
