#!/bin/bash
rm data/sequences_2024.fasta
cdbfasta data/sequences.fasta
cat my_profiles/local/include_2024.txt | cdbyank data/sequences.fasta.cidx > data/sequences_2024.fasta
cdbfasta data/sequences_2024.fasta