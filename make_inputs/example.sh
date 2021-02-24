#!/bin/bash

outdir=/oak/stanford/groups/akundaje/projects/cad/svm_inputs
ref_fasta=/oak/stanford/groups/akundaje/refs/mm10/GRCm38.p4.genome.fa
#genomewide_gc=/oak/stanford/groups/akundaje/soumyak/refs/mm10/gc_mm10_nosmooth.tsv
genome=mm10
ntrain=60000
chrom_sizes=mm10.chrom.sizes

[[ -d $outdir/logs ]] || mkdir $outdir/logs

cd /home/groups/akundaje/soumyak/SVM_pipelines/make_inputs

#python make_gc_nosmooth_track.py --ref_fasta $ref_fasta \
#                       --chrom_sizes $chrom_sizes \
#                       --out_prefix $genomewide_gc

for task in c11 c12 c15 c16 c18
do
    echo $task
    peaks=/oak/stanford/groups/akundaje/projects/cad/peaks/original/$task.peaks.bed
    sbatch --export=ALL --requeue -J $task -o $outdir/logs/$task.o -e $outdir/logs/$task.e -t 1-0 --mem=60000 -p akundaje run.sh $task $peaks $outdir $ref_fasta $genomewide_gc $genome $ntrain
done

