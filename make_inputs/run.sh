task=$1 #COLL
idr=$2 #COLL.idr.optimal_peak.narrowPeak.summits.max.signal
genomewide_gc=$3
ref_fasta=$4
echo "starting $task $idr" 
./get_svm_peak_splits.sh $task $idr
echo "got svm peak splits" 
./get_gc_positives.sh $task
echo "got gc content of the positive sequences" 
./get_all_negatives.sh $task $idr $genomewide_gc
echo "got candidate negative set" 
./get_chrom_gc_region_dict.sh $task
echo "created python pickle for candidate negatives" 
./form_svm_input_fastas.sh $task $ref_fasta
echo "finished creating SVM inputs" 

 
