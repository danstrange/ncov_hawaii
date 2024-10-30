#!/usr/bin/env python3
import pandas as pd
import numpy as np
from Bio import SeqIO
import re
import os
import sys
from pathlib import Path
import datetime as dt

timestamp = sys.argv[1]
if  not (Path(f"sequences_{timestamp}.fa").exists() and
         Path(f"metadata_{timestamp}.txt").exists() and
         Path(f"lineage_report.{timestamp}.csv").exists() and
         Path(f"nextclade_report.{timestamp}.tsv").exists()):
    sys.exit(f"One or more of these 4 files can not be found!\nsequences_{timestamp}.fa\nmetadata_{timestamp}.txt\nlineage_report.{timestamp}.csv\nnextclade_report.{timestamp}.tsv\n")


#m = pd.read_csv("metadata.tsv", sep='\t', low_memory=False)
m = pd.read_csv("metadata.tsv", sep='\t', low_memory=False, dtype=object)

rdict = SeqIO.to_dict(SeqIO.parse(f"sequences_{timestamp}.fa", "fasta"))
r = range(len(rdict.keys()))

d = {'strain': list(rdict.keys()),
     'virus': ['ncov' for i in r],
     'gisaid_epi_isl': ['?' for i in r],
     'genbank_accession': ['?' for i in r],
     'region': ['North America' for i in r],
     'country': ['USA' for i in r],
     'division': ['Hawaii' for i in r],
     'region_exposure': ['North America' for i in r],
     'country_exposure': ['USA' for i in r],
     'division_exposure': ['Hawaii' for i in r],
     'segment': ['genome' for i in r],
     'length': ['29903' for i in r],
     'host': ['Homo sapiens' for i in r],
     'age': ['?' for i in r],
     'sex': ['?' for i in r],
     'GISAID_clade': ['?' for i in r],
     'originating_lab': ['HDOH' for i in r],
     'submitting_lab': ['HDOH' for i in r],
     'authors': ['HDOH' for i in r],
     'url': ['?' for i in r],
     'title': ['?' for i in r],
     'paper_url': ['?' for i in r]
     }

m1 = pd.concat([m, pd.DataFrame(d)], ignore_index=True)
m1.set_index('strain', inplace=True)

n = pd.read_csv(f'nextclade_report.{timestamp}.tsv', sep='\t', low_memory=False)
n.set_index('seqName', inplace=True)
n.rename(columns={'clade' : 'nextstrain_clade'}, inplace=True)
m1.update(n)

p = pd.read_csv(f'lineage_report.{timestamp}.csv', sep=',', low_memory=False)
p.set_index('taxon', inplace=True)
p.rename(columns={'lineage' : 'pangolin_lineage'}, inplace=True)
#p.loc[p.pangolin_lineage=='None', 'pangolin_lineage'] = p.note.apply(lambda x: re.search(r'lineage assignment ([^\s]+) ', x).groups()[0] if re.search(r'lineage assignment ([^\s]+) ', x) else 'None')
m1.update(p)

mm = pd.read_csv(f'metadata_{timestamp}.txt', sep='\t', low_memory=False)
mm.rename(columns={'DOC' : 'date', 'Notes' : 'epi_more', 'WGS Number' : 'strain'}, inplace=True)
indexes_to_drop = mm[mm.strain.apply(lambda x: bool(re.match('cDNA|Couldn|Sent', str(x))) | pd.isnull(x))].index
mm.drop(indexes_to_drop, inplace=True)
indexes_to_drop = mm[mm.strain.apply(lambda x: not bool(re.match('H\d{7}', str(x))))].index
mm.drop(indexes_to_drop, inplace=True)
mm.set_index('strain', inplace=True)
mm['date'] = pd.to_datetime(mm['date'], errors='coerce')
mm['date'] = mm['date'].dt.strftime('%Y-%m-%d')
ds = timestamp
#ds = re.sub(r'[-_]\d+$', '', ds)
ds = re.sub(r'^CL_', '', ds)
ds = dt.datetime.strptime(ds, '%Y%m%d').strftime('%Y-%m-%d')
mm['date_sequenced'] = ds
m1.update(mm)
m1.reset_index(inplace=True)
m1.loc[m1.location.isnull(), 'location'] = m1.epi_more.astype(str).apply(lambda x: 'Honolulu County HI' if bool(re.search(r'Oahu|Honolulu', x)) else 
                                                                                   'Maui County HI' if bool(re.search(r'Maui|Molokai|Lanai', x)) else 
                                                                                   'Hawaii County HI' if bool(re.search(r'Hawaii', x)) else 
                                                                                   'Kauai County HI' if bool(re.search(r'Kauai', x)) else '?')
m1.epi_more = m1.epi_more.astype(str).apply(lambda x: re.sub(r'^\s*(WGS)*\s*TaqPath\s*\(O,N,S\),*\s*', '', x))
m1.loc[m1.HI_cluster.isnull(), 'HI_cluster'] = m1.epi_more.astype(str).apply(lambda x: 'Community' if bool(re.search('Community', x)) else '')
m1['date'] = pd.to_datetime(m1['date'], errors='coerce')
m1['date'] = m1['date'].dt.strftime('%Y-%m-%d')
m1['date_submitted'] = pd.to_datetime(m1['date_submitted'], errors='coerce')
m1['date_submitted'] = m1['date_submitted'].dt.strftime('%Y-%m-%d')
m1.loc[m1.location_exposure.isnull(), 'location_exposure'] = m1.location
m1.loc[m1.zip_code.isnull(), 'zip_code'] = '?'
m1.loc[m1.zip_code_exposure.isnull(), 'zip_code_exposure'] = m1.zip_code
m1.loc[m1.authors == 'HDOH', 'url'] = m1.strain.apply(lambda x: f"http://10.164.4.194/registry/genomes/{x}/")

d = dt.datetime.now().isoformat()[:19]
os.rename('metadata.tsv', f'metadata.tsv.{d}')
m1.to_csv('metadata.tsv', sep='\t', index=False)
