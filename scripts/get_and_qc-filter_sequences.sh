#!/bin/bash

##gets sequences for build and filters out 'bad' sequences based on nextclade qc.overallStatus

datestamp=$1

echo "creating make_include_$datestamp"
echo "******"
scripts/make_include_$datestamp.sh
wait

echo "getting $datestamp sequences"
echo "******"
scripts/get_sequences_$datestamp.sh
wait
echo "******"

echo "running nextclade qc filter on sequences_$datestamp.fasta"
echo "******"
source /opt/apps/conda/etc/profile.d/conda.sh
conda activate nextclade
nextclade run  --input-dataset nextclade/nextclade_data/sars-cov-2  --output-all=nextclade/nextclade_$datestamp  data/sequences_$datestamp.fasta
wait
source /opt/apps/conda/etc/profile.d/conda.sh
conda activate nextstrain
mv data/sequences_$datestamp.fasta data/sequences_$datestamp.all.fasta
cdbfasta data/sequences_$datestamp.all.fasta
cut -f2,10 nextclade/nextclade_$datestamp/nextclade.tsv |tail -n+2 |awk '/good/||/mediocre/' |cdbyank data/sequences_$datestamp.all.fasta.cidx>data/sequences_$datestamp.fasta
echo "******"

echo "sequences after filtering:"
grep -c "^>" data/sequences_$datestamp.fasta