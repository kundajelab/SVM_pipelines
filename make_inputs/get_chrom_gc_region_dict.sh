task=$1
python get_chrom_gc_region_dict.py --input_bed $task/$task.candidate.negatives.tsv --outf $task/$task.candidate.negatives.gc.p
