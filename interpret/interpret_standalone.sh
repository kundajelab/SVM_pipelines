inputf=$1
numchunks=$2
numthreads=$3
modelpath=$4

split -t'>' -n $numchunks -d $inputf $inputf-
#remove leading 0's
rename 's/.fa-0?+/.fa-/g' $inputf-*

#run gkmexplain in parallel
seq 0 $numchunks | xargs -I{} -n 1 -P $numthreads gkmexplain $inputf-{} $modelpath $inputf.gkmexplain.{}

#aggregate the results
for i in `seq 0 $numchunks`
do
    cat $inputf.gkmexplain.$i >> $inputf.gkmexplain.aggregated.txt
done


