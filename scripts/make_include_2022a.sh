#!/bin/bash
#(cat defaults/include.txt; echo " "; grep '^>H' data/sequences.fasta|cut -b2-) > my_profiles/local/include.txt
(cat defaults/include.txt; echo " "; cut -f1,5 data/metadata.tsv | awk '/2021-12-/||/2022-01-/||/2022-02-/||/2022-03-/||/2022-04-/||/2022-05-/||/2022-06-/' | cut -f1 | sort ) > my_profiles/local/include_2022a.txt
