#!/bin/bash
rm /data/nextstrain/hawaii_2023/data/metadata_2022.tsv
(head -1 /data/nextstrain/hawaii_2023/data/metadata.tsv; cat /data/nextstrain/hawaii_2023/data/metadata.tsv |  grep $(grep '^>' /data/nextstrain/hawaii_2023/data/sequences_2022.fasta |cut -b2-|tr '\n' '~'|sed 's/~$//;s[~[\\|[g') ) > /data/nextstrain/hawaii_2023/data/metadata_2022.tsv