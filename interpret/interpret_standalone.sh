inputf=$1  ## input fasta file 
numchunks=$2 ## number of parallel chunks to split input fasta file into 
numthreads=$3 ## number of chunks to process in parallel with gkmexplain 
modelpath=$4 ## path to model to use with gkmexplain. 

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


