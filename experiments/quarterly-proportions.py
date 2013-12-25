from utils import get_db
from pandas import DataFrame
from utils import ci
import numpy as np

db = get_db()
shots = list(db.shots.find())
shots_df = DataFrame(shots)

q1 = shots_df['qtr'] == '1'
q2 = shots_df['qtr'] == '2'
q3 = shots_df['qtr'] == '3'
q4 = shots_df['qtr'] == '4'
q1q2 = np.any([shots_df['qtr'] == '1', shots_df['qtr'] == '2'], 0)

qtr_ps = {
        'q1': [len(shots_df[np.all([q1, shots_df['made']], 0)]) / float(len(shots_df[q1])), len(shots_df[q1])],
        'q2': [len(shots_df[np.all([q2, shots_df['made']], 0)]) / float(len(shots_df[q2])), len(shots_df[q2])],
        'q3': [len(shots_df[np.all([q3, shots_df['made']], 0)]) / float(len(shots_df[q3])), len(shots_df[q3])],
        'q4': [len(shots_df[np.all([q4, shots_df['made']], 0)]) / float(len(shots_df[q4])), len(shots_df[q4])],
        'q1q2': [len(shots_df[np.all([q1q2, shots_df['made']], 0)]) / float(len(shots_df[q1q2])), len(shots_df[q1q2])]
        }

cis = {}
for q in qtr_ps:
    cis[q] = ci(qtr_ps[q][0], qtr_ps[q][1])
