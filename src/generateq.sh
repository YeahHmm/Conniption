#!/bin/bash

python3 main.py qlearn hybrid qh.pkl
python3 main.py qlearn cells qc.pkl
python3 main.py qlearn sols qs.pkl
python3 main.py qlearn random qr.pkl
python3 main.py qlearn flip qf.pkl
python3 main.py hybrid qlearn hq.pkl
python3 main.py cells qlearn cq.pkl
python3 main.py sols qlearn sq.pkl
python3 main.py random qlearn rq.pkl
python3 main.py flip qlearn fq.pkl
