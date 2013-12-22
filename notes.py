import utils
import shot_filters
from pandas import DataFrame, Series
import numpy as np

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

# hypothesis test: different sides of court
pooled_p = (left_p*n_l + right_p*n_r)/(n_r + n_l)
pooled_se = np.sqrt(pooled_p * (1-pooled_p) * ((1.0/n_l) + (1.0/n_r)) )
pooled_z_stat = (right_p - left_p) / pooled_se
