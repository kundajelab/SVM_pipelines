#!/bin/bash

task=$1
peaks=$2
outdir=$3
ref_fasta=$4
genomewide_gc=$5
genome=$6
ntrain=$7

[[ -d $outdir/$task ]] || mkdir $outdir/$task

echo "starting $task $peaks"

bash get_svm_peak_splits.sh $task $peaks $outdir $genome $ntrain

echo "got svm peak splits"

bash get_gc_positives.sh $task $outdir $ref_fasta

echo "got gc content of the positive sequences"

bash get_all_negatives.sh $task $peaks $outdir $genomewide_gc

echo "got candidate negative set"

bash get_chrom_gc_region_dict.sh $task $outdir

echo "created python pickle for candidate negatives"

bash form_svm_input_fastas.sh $task $outdir $ref_fasta

echo "finished creating SVM inputs"

