#!/bin/bash
#(cat defaults/include.txt; echo " "; grep '^>H' data/sequences.fasta|cut -b2-) > my_profiles/local/include.txt
(cat defaults/include.txt; echo " "; grep '^>H' data/sequences.fasta|tail -9600|cut -b2-) > my_profiles/local/include.txt
