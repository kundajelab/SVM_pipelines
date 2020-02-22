#get the inverse intersection of idr peak file and all gc genome bins
task=$1
idr=$2
bedtools intersect -v -a /srv/scratch/annashch/5_cell_lines_bias_correction/genomewide_gc/gc_hg38_nosmooth.tsv -b $task/$idr > $task/$task.candidate.negatives.tsv
