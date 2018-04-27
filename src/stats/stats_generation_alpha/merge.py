import os
from os import sys
_PATH_ = os.path.dirname(__file__)
print (_PATH_)
if _PATH_ not in sys.path:
    sys.path.append(_PATH_)
    sys.path.append("src")


from resources import resource

from itertools import product, chain
import pickle

import datetime
now = datetime.datetime.now()

letters = {'h', 'c', 's', 'f', 'r'}
comb = map(lambda p: './log_alpha/' + '4' + '-' + '26-' + ''+ ''.join(p) + '.pkl',
            chain(product(letters, {'a'}), product({'a'}, letters)))
print(comb)

data = []
for f in comb:
    data += pickle.load(open(f, 'rb'))

out = open('./log_alpha/results/merged_26evals.pkl', 'wb')
#out = open('./log_alpha/results/merged_'+ str(now.day)+ '_' + str(now.month) +'evals.pkl', 'wb')
pickle.dump(data, out)
