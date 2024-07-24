#!/usr/bin/env python3
import pandas as pd
import datetime as dt
import os, sys, re, pathlib

if len(sys.argv) > 1:
    gisaid_file = sys.argv[1]
else:
    gisaid_file = '/data/gisaid/download/20220824/gisaid_hcov-19_2022_08_24_21_metadata.tsv'

if  not (pathlib.Path(gisaid_file).is_file() and pathlib.Path(gisaid_file).exists()):
    sys.exit(f"file {gisaid_file} does not exist!\n")

m = pd.read_csv("metadata.tsv", sep="\t", low_memory=False)
m.set_index('strain', inplace=True)
pd.set_option('display.max_rows', None)
p = pd.read_csv(gisaid_file, sep='\t', low_memory=False)
p['strain'] = p['Virus name'].apply(lambda x:re.sub(r'^hCoV-19/USA/HI-','', re.sub(r'/202\d$','', x)))
p.set_index('strain', inplace=True)
p.rename(columns={'Accession ID' : 'gisaid_epi_isl'}, inplace=True)
m.update(p)
m.reset_index(inplace=True)
d = dt.datetime.now().isoformat()[:19]
os.rename('metadata.tsv', f'metadata.tsv.{d}')
m.to_csv('metadata.tsv', sep='\t', index=False)

