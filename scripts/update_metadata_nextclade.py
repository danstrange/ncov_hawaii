#!/usr/bin/env python3
import pandas as pd
import datetime as dt
import os

m = pd.read_csv("metadata.tsv", sep="\t", low_memory=False)
m.set_index('strain', inplace=True)
pd.set_option('display.max_rows', None)
p = pd.read_csv('nextclade_report.tsv', sep='\t', low_memory=False)
p.set_index('seqName', inplace=True)
p.rename(columns={'clade' : 'nextstrain_clade'}, inplace=True)
m.update(p)
m.reset_index(inplace=True)
d = dt.datetime.now().isoformat()[:19].replace('-','_').replace(':','_')
os.rename('metadata.tsv', f'metadata.tsv.{d}')
m.to_csv('metadata.tsv', sep='\t', index=False)

