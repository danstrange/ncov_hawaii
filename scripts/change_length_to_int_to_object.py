#!/usr/bin/env python3
import pandas as pd

m = pd.read_csv('metadata.tsv', sep='\t', low_memory=False)
m['length'] = m['length'].astype(int)
m['length'] = m['length'].astype(str)
m.to_csv('metadata.tsv', sep='\t', index=False)
