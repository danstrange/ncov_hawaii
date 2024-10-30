#!/usr/bin/env bash

datestamp=$1

##To add/update maven id to 'metadata.tsv'

/data/nextstrain/ncov_hawaii/scripts/add_maven_id.py
wait

##Print maven id with lineages to 'maven_lineage_update.csv'

/data/nextstrain/ncov_hawaii/scripts/print_maven_lineage.py
wait

#Change file name to reflect today's date
mv maven_lineage_update.csv maven_lineage_update_$datestamp.csv
