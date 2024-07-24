#!/usr/bin/env bash
set -e
set -o noclobber

datestamp=$1
if [[ ! -s sequences_$datestamp.fa || ! -s metadata_$datestamp.txt || ! -s nextclade_report.$datestamp.tsv ]]; then
  echo "$0: some of these files are not found:"
  echo "    sequences_$datestamp.fa"
  echo "    metadata_$datestamp.txt"
  echo "    nextclade_report.$datestamp.tsv"
  exit 1
fi

## to determine vadr-failed sequences

#docker pull staphb/vadr:latest
docker run --rm=True -v $PWD:/data -u $(id -u):$(id -g) staphb/vadr:latest \
	v-annotate.pl --split --cpu 32 --glsearch -s -r --nomisc \
		--mkey sarscov2 --lowsim5seq 6 --lowsim3seq 6 \
		--alt_fail lowscore,insertnn,deletinn \
		sequences_$datestamp.fa \
		vadr-outdir_$datestamp
wait

## filter to remove nextclade bad sequences, sequences with >=2400 Ns, and vadr-failed sequences

cut -f2,10,15 nextclade_report.$datestamp.tsv | tail -n+2 | awk '($3 < 2400)&&(/good/||/mediocre/)' | cut -f1 > qc_pass.$datestamp.list

mv sequences_$datestamp.fa sequences_$datestamp.all.fa
cdbfasta sequences_$datestamp.all.fa
#cut -f2,15,44 nextclade_report.$datestamp.tsv |tail -n+2 |python -c "import sys;[sys.stdout.write(line.split()[0]+'\n') for line in sys.stdin if len(line.split())>1 and int(line.split()[1])<2400]" |cdbyank sequences_$datestamp.all.fa.cidx > sequences_$datestamp.fa
grep -w -f qc_pass.$datestamp.list vadr-outdir_$datestamp/vadr-outdir_$datestamp.vadr.pass.list | cdbyank sequences_$datestamp.all.fa.cidx > sequences_$datestamp.fa

mv metadata_$datestamp.txt metadata_$datestamp.all.txt
#(head -1 metadata_$datestamp.all.txt; cat metadata_$datestamp.all.txt |grep $(cut -f2,15,44 nextclade_report.$datestamp.tsv |tail -n+2 |python -c "import sys;[sys.stdout.write(line.split()[0]+'\\|') for line in sys.stdin if len(line.split())>1 and int(line.split()[1])<2400]" |sed 's/\\|$//')) > metadata_$datestamp.txt
(head -1 metadata_$datestamp.all.txt; cat metadata_$datestamp.all.txt | grep "$(grep -w -f qc_pass.$datestamp.list vadr-outdir_$datestamp/vadr-outdir_$datestamp.vadr.pass.list)") > metadata_$datestamp.txt

echo "sequences after filtering:"
grep -c "^>" sequences_$datestamp.fa