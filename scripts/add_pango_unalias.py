#!/usr/bin/env python3
import pandas as pd
from pango_aliasor.aliasor import Aliasor
import argparse


def add_unaliased_column(tsv_file_path, pango_column='pangolin_lineage', unaliased_column='pango_lineage_unaliased'):
    aliasor = Aliasor()
    def uncompress_lineage(lineage):
        if not lineage or pd.isna(lineage):
            return "?"
        return aliasor.uncompress(lineage)

    #df = pd.read_csv(tsv_file_path, sep='\t')
    df = pd.read_csv(tsv_file_path, sep='\t', low_memory=False)
    df[unaliased_column] = df[pango_column].apply(uncompress_lineage)
    return df


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Add unaliased Pango lineage column to a TSV file.')
    parser.add_argument('--input-tsv', required=True, help='Path to the input TSV file.')
    parser.add_argument('--pango-column', default='pangolin_lineage', help='Name of the Pango lineage column in the input file.')
    parser.add_argument('--unaliased-column', default='pango_lineage_unaliased', help='Name of the column to use for the unaliased Pango lineage column in output.')
    args = parser.parse_args()
    df = add_unaliased_column(args.input_tsv, args.pango_column, args.unaliased_column)
    print(df.to_csv(sep='\t', index=False))

