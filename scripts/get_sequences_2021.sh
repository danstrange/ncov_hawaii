#!/bin/bash
rm /data/nextstrain/hawaii_2023/data/sequences_2021.fasta
cdbfasta /data/nextstrain/hawaii_2023/data/sequences.fasta
cat /data/nextstrain/hawaii_2023/my_profiles/local/include_2021.txt | cdbyank /data/nextstrain/hawaii_2023/data/sequences.fasta.cidx > /data/nextstrain/hawaii_2023/data/sequences_2021.fasta
cdbfasta /data/nextstrain/hawaii_2023/data/sequences_2021.fasta