#!/bin/bash

#get the inverse intersection of all peaks and all gc genome bins

task=$1
peaks=$2
outdir=$3
genomewide_gc=$4

rm -f $outdir/$task/$task.all.positives.bed

for split in `seq 0 9`
do
    cat $outdir/$task/svm.peaks.$task.test.$split.gc.seq | cut -f 1-3 >> $outdir/$task/$task.all.positives.bed
done

cut -f 1-3 $peaks > $outdir/$task/$task.peaks.bed

cat $outdir/$task/$task.peaks.bed $outdir/$task/$task.all.positives.bed > $outdir/$task/$task.all.positives.peaks.bed

bedtools intersect -v -a $genomewide_gc -b $outdir/$task/$task.all.positives.peaks.bed > $outdir/$task/$task.candidate.negatives.tsv

