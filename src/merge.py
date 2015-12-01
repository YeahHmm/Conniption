import resource

from itertools import product
import pickle

letters = {'h', 'c', 's', 'r'}
comb = map(lambda p: '../log/' + ''.join(p) + '.pkl', product(letters, repeat=2))

data = []
for f in comb:
	data += pickle.load(open(f, 'rb'))

out = open('../log/merged.pkl', 'wb')
pickle.dump(data, out)
