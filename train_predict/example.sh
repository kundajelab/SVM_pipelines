#!/bin/bash

task=$1
indir=/home/soumyak/svm_inputs
outdir=/home/soumyak/svm_training
lsgkm_dir=/home/soumyak/lsgkm/src

echo $task
[[ -d $outdir/logs ]] || mkdir $outdir/logs
[[ -d $outdir/$task ]] || mkdir $outdir/$task
[[ -d $outdir/$task/models ]] || mkdir $outdir/$task/models
[[ -d $outdir/$task/predictions ]] || mkdir $outdir/$task/predictions

for fold in {0..9}
do
    echo $fold
    bash /home/soumyak/SVM_pipelines/train_predict/train_predict.sh $task $fold $indir $outdir $lsgkm_dir > $outdir/logs/$task.$fold.o &
done

wait

