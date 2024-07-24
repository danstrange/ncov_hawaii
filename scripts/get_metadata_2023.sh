#!/bin/bash
rm data/metadata_2023.tsv
(head -1 data/metadata.tsv; cat data/metadata.tsv |  grep $(grep '^>' data/sequences_2023.fasta |cut -b2-|tr '\n' '~'|sed 's/~$//;s[~[\\|[g') ) > data/metadata_2023.tsv