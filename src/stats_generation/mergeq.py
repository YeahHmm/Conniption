import resource

from itertools import product
import pickle

letters = {'h', 'c', 's', 'f', 'r'}
q_letters = {'q', 'm'}
comb = map(lambda p: '../log_reinforce/' + ''.join(p) + '.pkl', product(letters, q_letters))
print (list(comb))
print (len(list(comb)))


'''
data = []
for f in comb:
	data += pickle.load(open(f, 'rb'))

out = open('../log/merged_qlearn_5evals.pkl', 'wb')
pickle.dump(data, out)
'''
