#!/usr/bin/env bash
source /opt/apps/conda/etc/profile.d/conda.sh
conda activate nextclade
nextclade run -d sars-cov-2-21L  --output-all=nextclade_2023_21L  data/sequences_2023.fasta

