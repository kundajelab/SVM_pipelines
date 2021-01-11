#generates bigwig track of gmkexplain scores

import argparse
import pdb
import operator
import pandas as pd
import pysam
import pyBigWig
import pickle
from utils import *

def parse_args():
    parser=argparse.ArgumentParser(description="Generate Bigwig track from GKMexplain file")
    parser.add_argument("--gkmexplain_out")
    parser.add_argument("--chrom_index",type=int,default=0)
    parser.add_argument("--pos_index",type=int,default=1)
    parser.add_argument("--allele_index",type=int,default=-1)
    parser.add_argument("--pickled_scores")
    parser.add_argument("--chrom_sizes",default="/mnt/data/annotations/by_release/hg38/hg38.chrom.sizes")
    parser.add_argument("--ref_fasta",default="/mnt/data/GRCh38_no_alt_analysis_set_GCA_000001405.15.fasta")
    parser.add_argument("--out_bigwig")
    return parser.parse_args()

def open_bigwig(chrom_sizes_file,out_bigwig):
    chromsizes=[i.split('\t') for i in open(chrom_sizes_file,'r').read().strip().split('\n')]
    chromsizes=[tuple([i[0],int(i[1])]) for i in chromsizes]
    chromsizes=sorted(chromsizes,key=operator.itemgetter(0))
    print(chromsizes)
    bw=pyBigWig.open(out_bigwig,'w')
    bw.addHeader(chromsizes)
    return bw

def main():
    args=parse_args()
    bw=open_bigwig(args.chrom_sizes,args.out_bigwig)
    print("opened bigwig for writing and added header")
    ref=pysam.FastaFile(args.ref_fasta)
    gkmexplain_scores=pd.read_csv(args.gkmexplain_out,header=None,sep='\t')
    pickled_scores = []
    with open(args.pickled_scores, 'rb') as infile:
        pickled_scores = pickle.load(infile)
    #sort
    gkmexplain_scores[2] = pickled_scores
    gkmexplain_scores=gkmexplain_scores.sort_values(by=0)
    numscores=gkmexplain_scores.shape[0]

    new_dict = {'chrom': [], 'start': [], 'end': [], 'cur_seq': [], 'observed_scores': []}

    for index,row in gkmexplain_scores.iterrows():
        if index%100==0:
            print(str(index)+'/'+str(numscores))
        #hyp_scores=get_vals_from_gkm_line(row[2])
        hyp_scores=row[2]
        chrom=row[0].split(':')[0]
        start=int(row[0].split(':')[1].split('-')[0]) + 250
        end=int(row[0].split(':')[1].split('-')[1]) - 250
        cur_seq=get_seq(ref,chrom,start,end)
        #observed_scores=np.sum(cur_seq*hyp_scores,axis=1).tolist()
        observed_scores=np.sum(hyp_scores[250:750],axis=1).tolist()

        new_dict['chrom'].append(chrom)
        new_dict['start'].append(start)
        new_dict['end'].append(end)
        new_dict['cur_seq'].append(cur_seq)
        new_dict['observed_scores'].append(observed_scores)

    new_df = pd.DataFrame.from_dict(new_dict)
    new_df.sort_values(by=['chrom', 'start'], inplace=True)

    for index,row in new_df.iterrows():
        if index%100==0:
            print(str(index)+'/'+str(numscores))
        bw.addEntries(row['chrom'],row['start'],values=row['observed_scores'],span=1,step=1)

    bw.close()
if __name__=="__main__":
    main()
