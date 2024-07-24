#!/usr/bin/env bash

##To run nextclade on GISAID downloads

datestamp=$1

source /opt/apps/conda/etc/profile.d/conda.sh
conda activate nextclade
nextclade run --input-dataset /data/nextclade/nextclade_data/sars-cov-2 --output-tsv=nextclade_report.$datestamp.tsv sequences_$datestamp.fa