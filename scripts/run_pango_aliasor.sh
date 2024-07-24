#adds unaliased lineage to pango_lineage_unaliased column to metadata.tsv
source /opt/apps/conda/etc/profile.d/conda.sh
conda activate pango-aliasor
../scripts/add_pango_unalias.py --input-tsv metadata.tsv > metadata_unaliased.tsv
mv metadata_unaliased.tsv metadata.tsv
#remove last line (the unalias script adds a line)
sed -i '$ d' metadata.tsv