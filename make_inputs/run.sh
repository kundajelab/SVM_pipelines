task=COLL
idr=COLL.idr.optimal_peak.narrowPeak.summits.max.signal
echo "starting $task $idr" 
#./get_svm_peak_splits.sh $task $idr
echo "got svm peak splits" 
./get_gc_positives.sh $task
echo "got gc content of the positive sequences" 
./get_all_negatives.sh $task $idr
echo "got candidate negative set" 
./get_chrom_gc_region_dict.sh $task
echo "created python pickle for candidate negatives" 
./form_svm_input_fastas.sh $task
echo "finished creating SVM inputs" 

 
