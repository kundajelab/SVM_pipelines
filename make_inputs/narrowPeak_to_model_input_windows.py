import argparse
import pandas as pd

def parse_args():
    parser=argparse.ArgumentParser(description="generate unifrmly sized regions for model interpretation/training from a narrowPeak file, making sure to cover the file")
    parser.add_argument("--narrowPeak")
    parser.add_argument("--flank_size",type=int,default=1057)
    parser.add_argument("--chrom_sizes") 
    parser.add_argument("--outf")
    return parser.parse_args()

def main():
    args=parse_args()
    chrom_sizes_contents=open(args.chrom_sizes,'r').read().strip().split('\n')
    chrom_sizes={}
    for line in chrom_sizes_contents:
        tokens=line.split('\t')
        chrom_sizes[tokens[0]]=int(tokens[1]) 
    peaks=pd.read_csv(args.narrowPeak,header=None,sep='\t')
    intervals=set() 
    for index,row in peaks.iterrows():
        peak_start=row[1]
        peak_end=row[2]
        chrom=row[0]
        summit=row[9]
        #start at summit and extend in both directions until peak is fully covered, making sure to not run off the edges
        summit_interval_start=peak_start+summit-args.flank_size
        summit_interval_end=summit_interval_start+2*args.flank_size 
        if summit_interval_start<1:
            summit_interval_start=1
            summit_interval_end=summit_interval_start+2*args.flank_size
        elif summit_interval_end >  chrom_sizes[chrom]:
            summit_interval_end=chrom_sizes[chrom]-1
            summit_interval_start=summit_interval_end-2*args.flank_size
        #just as a sanity check, make sure we have not run off the edges of the chromosome
        assert summit_interval_start>=1
        assert summit_interval_end<=chrom_sizes[chrom]
        intervals.add((chrom,summit_interval_start,summit_interval_end))
        interval_start=summit_interval_start
        while interval_start > peak_start:
            #stride down
            interval_start=max([peak_start,interval_start-args.flank_size])
            interval_end=interval_start+2*args.flank_size
            assert interval_start >=1
            assert interval_end <= chrom_sizes[chrom]
            intervals.add((chrom,interval_start,interval_end))
        interval_end=summit_interval_end
        while interval_end < peak_end:
            #stride up
            interval_end=min([peak_end,interval_end+args.flank_size,chrom_sizes[chrom]])
            interval_start=interval_end-2*args.flank_size
            assert interval_start >=1
            assert interval_end <=chrom_sizes[chrom]
            intervals.add((chrom,interval_start,interval_end))
    intervals=list(intervals)
    outf=open(args.outf,'w')
    for interval in intervals:
        outf.write('\t'.join([str(i) for i in interval])+'\n')
    outf.close()
    
if __name__=="__main__":
    main()
    

    
    
