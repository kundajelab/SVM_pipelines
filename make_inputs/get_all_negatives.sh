#!/bin/bash

#get the inverse intersection of idr peak file and all gc genome bins

task=$1
peaks=$2
outdir=$3
genomewide_gc=$4

rm -f $outdir/$task/$task.all.positives.bed

for split in `seq 0 9`
do
    cat $outdir/$task/svm.peaks.$task.test.$split.bed >> $outdir/$task/$task.all.positives.bed
done

cat $peaks $outdir/$task/$task.all.positives.bed > $outdir/$task/$task.all.peaks.bed

bedtools intersect -v -a $genomewide_gc -b $idr > $task/$task.candidate.negatives.tsv

