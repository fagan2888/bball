from flask import Flask, jsonify, request, make_response, render_template
import shotchart
import shot_filters
import utils
import StringIO
from viz_code import left_right, quarterly, total_quarterly, num_quarterly

app = Flask(__name__)

#TODO: properly handle mongo connections

@app.route('/fg_pct')
def get_fg_pct():
    if request.method == 'GET':
        # TODO: form validation!
        x = request.args.get('x')
        y = request.args.get('y')
        radius= request.args.get('radius')

        shots = shotchart.find_shots_center(x,y,radius)
        pct = shotchart.fg_pct(shots)

        return jsonify({'num_shots':len(shots),
                        'pct':shotchart.fg_pct_by_pos(x,y,radius)})

@app.route('/num_shots')
def num_shots():
    if request.method == 'GET':
        mongo_params = shot_filters.merge_filters(request.args)
        db = utils.get_db()
        return str(db.shots.find(mongo_params).count())

@app.route('/shotchart')
def shotchart_img():
    if request.method == 'GET':
        mongo_params = shot_filters.merge_filters(request.args)
        tups = shotchart.prepare_shotchart(mongo_params)
        print len(tups)
        out = shotchart.create_shotchart_png(tups)
        #plot = shotchart.create_shotchart_plot(tups)
        #out = StringIO.StringIO()
        #plot.savefig(out,ext = 'png')
        resp = make_response(out.getvalue())
        resp.headers['Content-Type'] = 'image/png'
        return resp

@app.route('/shotchart2')
def shotchart2():
    if request.method == 'GET':
        mongo_params = shot_filters.merge_filters(request.args)
        tups = shotchart.prepare_shotchart(mongo_params)
        from numpy import array
        tups = [[x,y,pct,op] for (x,y,pct,op) in tups]
        return render_template('shotchart2.html', tups=tups)

@app.route('/visualizations')
def visualizations():
    if request.method == 'GET':
        # left_right()
        # quarterly()
        # total_quarterly()
        # num_quarterly()
        return render_template('visualizations.html')

if __name__ == '__main__':
    app.run(port=8080,debug = True)
