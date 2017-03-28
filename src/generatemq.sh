#!/bin/bash

python3 main.py minimaxq hybrid mh.pkl
python3 main.py minimaxq cells mc.pkl
python3 main.py minimaxq sols ms.pkl
python3 main.py minimaxq random mr.pkl
python3 main.py minimaxq flip mf.pkl
python3 main.py hybrid minimaxq hm.pkl
python3 main.py cells minimaxq cm.pkl
python3 main.py sols minimaxq sm.pkl
python3 main.py random minimaxq rm.pkl
python3 main.py flip minimaxq fm.pkl
