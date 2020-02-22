task=$1
idr=$2
python get_svm_peak_splits.py \
       --narrowPeak $task/$idr \
       --ntrain 60000 \
       --out_prefix $task/svm.peaks.$task \
       --genome hg38
