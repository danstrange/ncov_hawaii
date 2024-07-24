#!/usr/bin/env python3
import pandas as pd
import datetime as dt
import os
import re

m = pd.read_csv("metadata.tsv", sep="\t", low_memory=False)
m.set_index('strain', inplace=True)
pd.set_option('display.max_rows', None)
p = pd.read_csv('lineage_report.csv', sep=',', low_memory=False)
p.set_index('lineage', inplace=True)
#p.drop('None', inplace=True)
p.reset_index(inplace=True)
p.set_index('taxon', inplace=True)
p.rename(columns={'lineage' : 'pangolin_lineage'}, inplace=True)
#p.loc[p.pangolin_lineage=='None', 'pangolin_lineage'] = p.note.apply(lambda x: re.search(r'lineage assignment ([^\s]+) ', x).groups()[0] if re.search(r'lineage assignment ([^\s]+) ', x) else 'None')
m.update(p)
m.reset_index(inplace=True)
d = dt.datetime.now().isoformat()[:19]
os.rename('metadata.tsv', f'metadata.tsv.{d}')
m.to_csv('metadata.tsv', sep='\t', index=False)
