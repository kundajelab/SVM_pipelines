#generates bigwig track of gmkexplain scores
import argparse
import pdb 
import operator
import pandas as pd
import pysam
import pyBigWig
from utils import * 
def parse_args():
    parser=argparse.ArgumentParser(description="Generate Bigwig track from GKMexplain file")
    parser.add_argument("--gkmexplain_out")
    parser.add_argument("--chrom_index",type=int,default=0)
    parser.add_argument("--pos_index",type=int,default=1)
    parser.add_argument("--allele_index",type=int,default=-1)
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
    #sort
    gkmexplain_scores=gkmexplain_scores.sort_values(by=0)
    numscores=gkmexplain_scores.shape[0]
    for index,row in gkmexplain_scores.iterrows():
        if index%100==0:
            print(str(index)+'/'+str(numscores))
        #get hypothetical scores from gkmexplain 
        hyp_scores=get_vals_from_gkm_line(row[2])
        #get observed gkmexplain scores based on underlying sequence + allele of interst 
        flank=int(hyp_scores.shape[0]/2)
        metadata=row[0].split('_')
        chrom=metadata[args.chrom_index]
        pos=int(metadata[args.pos_index])
        allele=metadata[args.allele_index][0]
        cur_seq=get_seq(ref,chrom,pos,allele,flank)
        observed_scores=np.sum(cur_seq*hyp_scores,axis=1).tolist()
        #add entries to the file
        try:
            bw.addEntries(chrom,pos-flank,values=observed_scores,span=1,step=1)
        except:
            #there is overlap, only store the non-overlapping part, as pyBigWig cna't handle overlap
            last_end=last_pos+flank
            cur_start=pos-flank
            overlap=last_end-cur_start
            shift_start=pos-flank+overlap
            observed_scores=observed_scores[overlap::]
            bw.addEntries(chrom,shift_start,values=observed_scores,span=1,step=1)
        last_pos=pos
    bw.close()
if __name__=="__main__":
    main()
    
