#!/bin/bash
#(cat defaults/include.txt; echo " "; grep '^>H' data/sequences.fasta|cut -b2-) > my_profiles/local/include.txt
(cat defaults/include.txt; echo " "; cut -f1,5 data/metadata.tsv | awk '/2023-12-/||/2024-/' | cut -f1 | sort ) > my_profiles/local/include_2024.txt
