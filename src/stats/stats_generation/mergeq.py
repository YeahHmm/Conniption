import resource

from itertools import chain, product
import pickle

'''
This file takes all the pickle objects created during
the simulations and puts them all together for a better
extraction.
'''


letters = {'h', 'c', 's', 'r' ,'f'}
q_letters = {'q', 'm'}
letters = map(''.join, chain(product(letters, q_letters), product(q_letters, letters)))
comb = map(lambda p: '../log_reinforce/' + ''.join(p) + '.pkl', letters)
#print (len(list(comb)))



data = []
for f in comb:
    try:
        data += pickle.load(open(f, 'rb'))
        print(f)
    except:
        continue
out = open('../log_reinforce/merged_qlearn_5evals.pkl', 'wb')
pickle.dump(data, out)

print (list(comb))
