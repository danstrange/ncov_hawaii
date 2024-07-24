#!/bin/bash
rm data/sequences_2023.fasta
cdbfasta data/sequences.fasta
cat my_profiles/local/include_2023.txt | cdbyank data/sequences.fasta.cidx > data/sequences_2023.fasta
cdbfasta data/sequences_2023.fasta