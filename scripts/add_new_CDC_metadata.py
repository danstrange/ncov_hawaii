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
     'originating_lab': ['CDC' for i in r],
     'submitting_lab': ['CDC' for i in r],
     'authors': ['CDC' for i in r],
     'url': ['?' for i in r],
     'title': ['?' for i in r],
     'paper_url': ['?' for i in r]
     }

m1 = pd.concat([m, pd.DataFrame(d)], ignore_index=True)
m1.set_index('strain', inplace=True)

p = pd.read_csv(f'lineage_report.{timestamp}.csv', sep=',', low_memory=False)
p.set_index('taxon', inplace=True)
p.rename(columns={'lineage' : 'pangolin_lineage'}, inplace=True)
#p.rename(columns={'lineage' : 'pangolin_lineage'}, inplace=False)
#p.loc[p.pangolin_lineage=='None', 'pangolin_lineage'] = p.note.apply(lambda x: re.search(r'lineage assignment ([^\s]+) ', x).groups()[0] if re.search(r'lineage assignment ([^\s]+) ', x) else 'None')
m1.update(p)

n = pd.read_csv(f'nextclade_report.{timestamp}.tsv', sep='\t', low_memory=False)
n.set_index('seqName', inplace=True)
n.rename(columns={'clade' : 'nextstrain_clade'}, inplace=True)
m1.update(n)

mm = pd.read_csv(f'metadata_{timestamp}.txt', sep='\t', low_memory=False, dtype=object)
#mm.rename(columns={'Collection date' : 'date', 'Virus name' : 'strain', 'Accession ID' : 'gisaid_epi_isl', 'Sequence length' : 'length', 'Host' : 'host', 'Patient age' : 'age', 'Gender' : 'sex', 'Clade' : 'GISAID_clade', 'Submission date' : 'date_submitted'}, inplace=True)
mm.set_index('strain', inplace=True)
mm['date'] = pd.to_datetime(mm['date'], errors='coerce')
mm['date'] = mm['date'].dt.strftime('%Y-%m-%d')
ds = timestamp
ds = re.sub(r'^CDC_', '', ds)
ds = dt.datetime.strptime(ds, '%Y%m%d').strftime('%Y-%m-%d')
mm['date_sequenced'] = ds
mm['HI_cluster'] = 'CDC surveillance'
#mm['location'] = '?'
mm.loc[mm.location == 'AIEA', ['location', 'location_exposure']] = 'Honolulu County HI'
mm.loc[mm.location == 'Aiea', ['location', 'location_exposure']] = 'Honolulu County HI'
mm.loc[mm.location == 'EWA BEACH', ['location', 'location_exposure']] = 'Honolulu County HI'
mm.loc[mm.location == 'Ewa Beach', ['location', 'location_exposure']] = 'Honolulu County HI'
mm.loc[mm.location == 'Ewa Beac', ['location', 'location_exposure']] = 'Honolulu County HI'
mm.loc[mm.location == 'EWA GENTRY', ['location', 'location_exposure']] = 'Honolulu County HI'
mm.loc[mm.location == 'Ewa Gentry', ['location', 'location_exposure']] = 'Honolulu County HI'
mm.loc[mm.location == 'HONOLULU', ['location', 'location_exposure']] = 'Honolulu County HI'
mm.loc[mm.location == 'Honolulu', ['location', 'location_exposure']] = 'Honolulu County HI'
mm.loc[mm.location == 'HOLUALOA', ['location', 'location_exposure']] = 'Hawaii County HI'
mm.loc[mm.location == 'Holualoa', ['location', 'location_exposure']] = 'Hawaii County HI'
mm.loc[mm.location == 'HILO', ['location', 'location_exposure']] = 'Hawaii County HI'
mm.loc[mm.location == 'Hilo', ['location', 'location_exposure']] = 'Hawaii County HI'
mm.loc[mm.location == 'KAAAWA', ['location', 'location_exposure']] = 'Honolulu County HI'
mm.loc[mm.location == 'Kaaawa', ['location', 'location_exposure']] = 'Honolulu County HI'
mm.loc[mm.location == 'KAHULUI', ['location', 'location_exposure']] = 'Maui County HI'
mm.loc[mm.location == 'Kahului', ['location', 'location_exposure']] = 'Maui County HI'
mm.loc[mm.location == 'KAILUA', ['location', 'location_exposure']] = 'Honolulu County HI'
mm.loc[mm.location == 'Kailua', ['location', 'location_exposure']] = 'Honolulu County HI'
mm.loc[mm.location == 'KAILUA KONA', ['location', 'location_exposure']] = 'Hawaii County HI'
mm.loc[mm.location == 'Kailua Kona', ['location', 'location_exposure']] = 'Hawaii County HI'
mm.loc[mm.location == 'KAILUA-KONA', ['location', 'location_exposure']] = 'Hawaii County HI'
mm.loc[mm.location == 'Kailua-Kona', ['location', 'location_exposure']] = 'Hawaii County HI'
mm.loc[mm.location == 'KAPOLEI', ['location', 'location_exposure']] = 'Honolulu County HI'
mm.loc[mm.location == 'Kapolei', ['location', 'location_exposure']] = 'Honolulu County HI'
mm.loc[mm.location == 'KANEOHE', ['location', 'location_exposure']] = 'Honolulu County HI'
mm.loc[mm.location == 'Kaneohe', ['location', 'location_exposure']] = 'Honolulu County HI'
mm.loc[mm.location == 'KIHEI', ['location', 'location_exposure']] = 'Maui County HI'
mm.loc[mm.location == 'Kihei', ['location', 'location_exposure']] = 'Maui County HI'
mm.loc[mm.location == 'KONA', ['location', 'location_exposure']] = 'Hawaii County HI'
mm.loc[mm.location == 'Kona', ['location', 'location_exposure']] = 'Hawaii County HI'
mm.loc[mm.location == 'LAHAINA', ['location', 'location_exposure']] = 'Maui County HI'
mm.loc[mm.location == 'Lahaina', ['location', 'location_exposure']] = 'Maui County HI'
mm.loc[mm.location == 'MAKAWAO', ['location', 'location_exposure']] = 'Maui County HI'
mm.loc[mm.location == 'Makawao', ['location', 'location_exposure']] = 'Maui County HI'
mm.loc[mm.location == 'WAIANAE', ['location', 'location_exposure']] = 'Honolulu County HI'
mm.loc[mm.location == 'Waianae', ['location', 'location_exposure']] = 'Honolulu County HI'
mm.loc[mm.location == 'WAILUKU', ['location', 'location_exposure']] = 'Maui County HI'
mm.loc[mm.location == 'Wailuku', ['location', 'location_exposure']] = 'Maui County HI'
mm.loc[mm.location == 'WAIMANALO', ['location', 'location_exposure']] = 'Honolulu County HI'
mm.loc[mm.location == 'Waimanalo', ['location', 'location_exposure']] = 'Honolulu County HI'
mm.loc[mm.location == 'WAIPAHU', ['location', 'location_exposure']] = 'Honolulu County HI'
mm.loc[mm.location == 'Waipahu', ['location', 'location_exposure']] = 'Honolulu County HI'
mm.loc[mm.division == 'Pacific', ['location', 'location_exposure']] = '?'
mm.loc[mm.division == 'Pacific', ['division', 'division_exposure']] = 'Hawaii'
m1.update(mm)
m1.reset_index(inplace=True)
#m1['strain'] = m1.strain.apply(lambda x: re.sub(r'^hCoV-19/USA/', '', re.sub(r'/2021$', '', x)))
m1['date'] = pd.to_datetime(m1['date'], errors='coerce')
m1['date'] = m1['date'].dt.strftime('%Y-%m-%d')
m1['date_submitted'] = pd.to_datetime(m1['date_submitted'], errors='coerce')
m1['date_submitted'] = m1['date_submitted'].dt.strftime('%Y-%m-%d')
m1.loc[m1.location_exposure.isnull(), 'location_exposure'] = '?'
m1.loc[m1.zip_code.isnull(), 'zip_code'] = '?'
m1.loc[m1.zip_code_exposure.isnull(), 'zip_code_exposure'] = m1.zip_code
m1['url'] = m1.strain.apply(lambda x: f"http://10.164.4.194/registry/genomes/{x}/")

d = dt.datetime.now().isoformat()[:19]
os.rename('metadata.tsv', f'metadata.tsv.{d}')
m1.to_csv('metadata.tsv', sep='\t', index=False)
