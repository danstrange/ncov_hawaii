#!/bin/bash

datestamp=$1

docker pull staphb/vadr:latest
docker run --rm=True -v $PWD:/data -u $(id -u):$(id -g) staphb/vadr:latest \
	v-annotate.pl --split --cpu 36 --glsearch -s -r --nomisc \
		--mkey sarscov2 --lowsim5seq 6 --lowsim3seq 6 \
		--alt_fail lowscore,insertnn,deletinn \
		sequences_$datestamp.fa \
		vadr-outdir
echo "VADR failed sequences:"
#grep -o -E "^>\w+" vadr-outdir/vadr-outdir.vadr.fail.fa | tr -d ">" ## This command pulls the WGS number from the respective .fa
cat vadr-outdir/vadr-outdir.vadr.fail.list