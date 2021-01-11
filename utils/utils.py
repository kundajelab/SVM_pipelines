import numpy as np
import pysam

ltrdict = {'a':[1,0,0,0],
           'c':[0,1,0,0],
           'g':[0,0,1,0],
           't':[0,0,0,1],
           'n':[0,0,0,0],
           'A':[1,0,0,0],
           'C':[0,1,0,0],
           'G':[0,0,1,0],
           'T':[0,0,0,1],
           'N':[0,0,0,0]}

def get_vals_from_gkm_line(seq):
    return np.asarray([[float(i) for i in i.split(',')] for i in seq.split(';')])

def one_hot_encode(seq):
    return np.array([ltrdict.get(x,[0,0,0,0]) for x in seq])


def get_seq(ref,chrom,start,end):
    #seq_prefix=ref.fetch(chrom,int(pos)-flank,int(pos)).upper() 
    #seq_suffix=ref.fetch(chrom,int(pos)+1,int(pos)+flank).upper()
    seq=ref.fetch(chrom,start,end).upper()
    #one-hot-encode the seq 
    return one_hot_encode(seq)
