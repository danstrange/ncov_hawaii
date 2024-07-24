#!/bin/bash
#(cat defaults/include.txt; echo " "; grep '^>H' data/sequences.fasta|cut -b2-) > my_profiles/local/include.txt
(cat defaults/include.txt; echo " "; cut -f1,5 data/metadata.tsv | awk '/2022-06-/||/2022-07-/||/2022-08-/||/2022-09-/||/2022-10-/||/2022-11-/||/2022-12-/' | cut -f1 | sort ) > my_profiles/local/include_2022b.txt
