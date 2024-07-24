#!/usr/bin/env bash
set -e
set -o noclobber

datestamp=$1
if [[ ! -s sequences_$datestamp.fasta || ! -s nextclade_report.$datestamp.tsv ]]; then
  echo "$0: some of these files are not found:"
  echo "    sequences_$datestamp.fasta"
  echo "    nextclade_report.$datestamp.tsv"
  exit 1
fi

mv sequences_$datestamp.fasta sequences_$datestamp.all.fasta
cdbfasta sequences_$datestamp.all.fasta
cut -f2,10 nextclade_report.$datestamp.tsv |tail -n+2 |awk '/good/||/mediocre/' |cdbyank sequences_$datestamp.all.fasta.cidx>sequences_$datestamp.fasta
