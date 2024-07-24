#!/usr/bin/env python3
import pandas as pd
import datetime as dt
import os
import re

m = pd.read_csv("metadata.tsv", sep="\t", low_memory=False)
m.set_index('strain', inplace=True)
pd.set_option('display.max_rows', None)
p = pd.read_csv('mips_list.csv', sep=',', low_memory=False)
p.set_index('WGS_number', inplace=True)
m.update(p)
q = pd.read_csv('CL_list.csv', sep=',', low_memory=False)
q.set_index('WGS_number', inplace=True)
m.update(q)
m.reset_index(inplace=True)
d = dt.datetime.now().isoformat()[:19]
os.rename('metadata.tsv', f'metadata.tsv.{d}')
m.to_csv('metadata.tsv', sep='\t', index=False)
