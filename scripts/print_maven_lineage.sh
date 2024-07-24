#!/usr/bin/env bash

##To print lineage and maven number

awk -F"\t" '$1 && $23 && $35 && $36 {print $36,",",$1,",",$23,",",$35}' metadata.tsv > maven_updated_lineage.csv
