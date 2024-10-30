#!/usr/bin/env python3
import pandas as pd

m = pd.read_csv("metadata.tsv", sep="\t", low_memory=False, dtype=object)
m['maven_number'] = m['maven_number'].fillna('?') # adds '?' to empty maven number fields
m.set_index('strain', inplace=True)
pd.set_option('display.max_rows', None)
p = pd.read_csv('maven_id.tsv', sep='\t', low_memory=False, dtype=object)
p.set_index('WGS_Number', inplace=True)
m.update(p)
m.reset_index(inplace=True)
m.to_csv('metadata.tsv', sep='\t', index=False)
