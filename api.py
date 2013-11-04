from flask import Flask, jsonify, request
import shotchart

app = Flask(__name__)

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


if __name__ == '__main__':
    app.run(port=8080,debug = True)
                           
            
