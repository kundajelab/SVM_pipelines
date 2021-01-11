#!/bin/bash

fold=0

for cluster in c11 c12 c15 c16 c18
do

    python gkmexplain_to_bigwig.py --gkmexplain_out /oak/stanford/groups/akundaje/projects/cad/explain_scores/$cluster/$cluster.fold$fold.explain \
       --chrom_index 0 \
       --pos_index 1 \
       --allele_index -1 \
       --pickled_scores /oak/stanford/groups/akundaje/projects/cad/explain_scores/$cluster/$cluster.fold$fold.explain.normed.pkl \
       --chrom_sizes /oak/stanford/groups/akundaje/refs/mm10/mm10.male.chrom.sizes \
       --ref_fasta /oak/stanford/groups/akundaje/refs/mm10/GRCm38.p4.genome.fa \
       --out_bigwig /oak/stanford/groups/akundaje/projects/cad/explain_scores/$cluster/$cluster.fold$fold.explain.bigwig
done

