#!/usr/bin/env python3
import pandas as pd

m = pd.read_csv('metadata.tsv', sep='\t', low_memory=False, dtype=object)
d = m.loc[:, ['maven_number', 'strain', 'pangolin_lineage', 'pango_lineage_unaliased']]
d.rename(columns={'strain':'wgs_number'}, inplace=True)
d = d.dropna() # drops rows containing fields with NaN
d = d.loc[d['maven_number'] != '?'] # drops rows containing '?' in maven number field
d.to_csv('maven_lineage_update.csv', index=False)
