#!/bin/bash

task=$1
fold=$2
indir=$3
outdir=$4
lsgkm_dir=$5

$lsgkm_dir/gkmtrain -m 10000 -v 2 -T 16 $indir/$task/svm.inputs.$task.train.$fold.positives $indir/$task/svm.inputs.$task.train.$fold.negatives $outdir/$task/models/$task.$fold

$lsgkm_dir/gkmpredict -v 2 -T 16 $indir/$task/svm.inputs.$task.test.$fold.positives $outdir/$task/models/$task.$fold.model.txt $outdir/$task/predictions/$task.$fold.positives

$lsgkm_dir/gkmpredict -v 2 -T 16 $indir/$task/svm.inputs.$task.test.$fold.negatives $outdir/$task/models/$task.$fold.model.txt $outdir/$task/predictions/$task.$fold.negatives

