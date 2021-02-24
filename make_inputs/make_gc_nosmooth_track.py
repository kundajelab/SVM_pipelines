"""
Borrowed from Anna Shcherbina's code at:
https://github.com/kundajelab/model_input_tracks/blob/master/model_input_tracks/gc_nosmooth/__init__.py
"""

import pandas as pd
import pysam
import argparse
import pdb

def parse_args():
    parser=argparse.ArgumentParser(description="get gc content from a bed file")
    parser.add_argument("--chrom_sizes")
    parser.add_argument("--ref_fasta")
    parser.add_argument("--out_prefix")
    parser.add_argument("--region_size",type=int,default=1000)
    parser.add_argument("--stride",type=int,default=50)
    return parser.parse_args()

def main():
    args=parse_args()
    ref=pysam.FastaFile(args.ref_fasta)
    chrom_sizes=pd.read_csv(args.chrom_sizes,header=None,sep='\t')
    region_dict=dict()
    for index,row in chrom_sizes.iterrows():
        chrom=row[0]
        print(chrom)
        chrom_size=row[1]
        for bin_start in range(0,chrom_size,args.stride):
            if bin_start%1000000==0:
                print(str(bin_start))
            bin_end=bin_start+args.region_size
            seq=ref.fetch(chrom,bin_start,bin_end).upper()
            g=seq.count('G')
            c=seq.count('C')
            gc=g+c
            fract=round(gc/args.region_size,2)
            region_dict[tuple([chrom,bin_start,bin_end])]=fract
    #generate pandas df from dict
    print("making df")
    df=pd.DataFrame.from_dict(region_dict,orient='index')
    print("made df")
    new_index=pd.MultiIndex.from_tuples(df.index, names=('CHR', 'START','END'))
    df = pd.DataFrame(df[0], new_index)
    df.to_csv(args.out_prefix,sep='\t', header=False, index=True)

if __name__=="__main__":
    main()
