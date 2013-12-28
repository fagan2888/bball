import utils
import shot_filters
from pandas import DataFrame, Series, unique
import numpy as np
import json
import pickle

def left_right():
    db = utils.get_db()

    left_f = shot_filters.merge_filters({'left':0})
    left_df = DataFrame(list(db.shots.find(left_f)))
    n_l = len(left_df)
    left_p = len(left_df[left_df['made']]) / float(n_l)
    left_ci = utils.ci(left_p, n_l)

    right_f = shot_filters.merge_filters({'right':0})
    right_df = DataFrame(list(db.shots.find(right_f)))
    n_r = len(right_df)
    right_p = len(right_df[right_df['made']]) / float(n_r)
    right_ci = utils.ci(right_p, n_r)

    # # hypothesis test: different sides of court
    # pooled_p = (left_p*n_l + right_p*n_r)/(n_r + n_l)
    # pooled_se = np.sqrt(pooled_p * (1-pooled_p) * ((1.0/n_l) + (1.0/n_r)) )
    # pooled_z_stat = (right_p - left_p) / pooled_se
    json.dump([{
            'name': 'Right',
            'value': right_p,
            'l': right_ci[0],
            'u': right_ci[1]
        },
        {
            'name': 'Left',
            'value': left_p,
            'l': left_ci[0],
            'u': left_ci[1]
        }], open('static/data/left-right.json','w'))

def quarterly():
    db = utils.get_db()
    shots = list(db.shots.find())
    shots_df = DataFrame(shots)

    q1 = shots_df['qtr'] == '1'
    q2 = shots_df['qtr'] == '2'
    q3 = shots_df['qtr'] == '3'
    q4 = shots_df['qtr'] == '4'
    q1q2 = np.any([shots_df['qtr'] == '1', shots_df['qtr'] == '2'], 0)

    qtr_ps = {
            'Q1': [len(shots_df[np.all([q1, shots_df['made']], 0)]) / float(len(shots_df[q1])), len(shots_df[q1])],
            'Q2': [len(shots_df[np.all([q2, shots_df['made']], 0)]) / float(len(shots_df[q2])), len(shots_df[q2])],
            'Q3': [len(shots_df[np.all([q3, shots_df['made']], 0)]) / float(len(shots_df[q3])), len(shots_df[q3])],
            'Q4': [len(shots_df[np.all([q4, shots_df['made']], 0)]) / float(len(shots_df[q4])), len(shots_df[q4])],
            # 'q1q2': [len(shots_df[np.all([q1q2, shots_df['made']], 0)]) / float(len(shots_df[q1q2])), len(shots_df[q1q2])]
            }

    cis = {}
    for q in qtr_ps:
        cis[q] = utils.ci(qtr_ps[q][0], qtr_ps[q][1])

    json.dump([{
        'name': q,
        'value': qtr_ps[q][0],
        'l': cis[q][0],
        'u': cis[q][1]
        } for q in qtr_ps], open('static/data/quarterly.json','w'))

def total_quarterly():
    db = utils.get_db()
    num_shots = []
    for i in range(1,5):
        params = {'quarter': '%i' % i}
        shots = db.shots.find(shot_filters.merge_filters(params))
        num_shots.append({'name': 'Q%i' % i, 'value': shots.count()})
    json.dump(num_shots, open('static/data/total_quarterly.json','w'))

def num_quarterly():
    # db = utils.get_db()
    # games = []
    # shots = db.shots.find()
    # shots_df = DataFrame(list(shots))
    # game_ids = unique(shots_df['espn_game_id'])
    # num_shots = {'Q1':{},'Q2':{},'Q3':{},'Q4':{}}
    # l = len(game_ids)
    # for k in range(len(game_ids)):
        # game = game_ids[k]
        # print '%i left' % (l-k)
        # game_qs = {}
        # for i in range(1,5):
            # q_shots = np.all([shots_df['espn_game_id'] == game, shots_df['qtr'] == str(i)],0)
            # num_shots['Q%i' % i][game] = len(shots_df[q_shots])
    # pickle.dump(num_shots, open('num_shots.p','wb'))
    num_shots = pickle.load(open('num_shots.p','rb'))
    num_shots_df = DataFrame(num_shots)

    q_shots =  [
            {
                'name': s,
                'value': np.mean(num_shots_df[s]),
                'l': np.mean(num_shots_df[s]) - 1.96 * np.sqrt(np.std(num_shots_df[s]) / len(num_shots_df[s])),
                'u': np.mean(num_shots_df[s]) + 1.96 * np.sqrt(np.std(num_shots_df[s]) / len(num_shots_df[s]))
                }
            for s in ['Q1','Q2','Q3','Q4']]
    json.dump(q_shots, open('static/data/num_shots.json','w'))
