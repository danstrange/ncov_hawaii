#!/usr/bin/env bash

##To run pangolin on GISAID downloads

datestamp=$1

source /opt/apps/conda/etc/profile.d/conda.sh
conda activate pangolin
pangolin -t 32 sequences_$datestamp.fa  --outfile lineage_report.$datestamp.csv