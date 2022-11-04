echo "chr10	104419735	104419736	chr10_104419735_C_G	C	G" > snps.bed
repo_prefix="/users/annashch/SVM_pipelines/"
model_prefix="/oak/stanford/groups/akundaje/projects/chrombpnet/svm"

#get the fasta sequence flanking the effect (C) and noneffect (G) alleles
fasta_prefix=snps_of_interest
python $repo_prefix/interpret/get_seqs.py --variant_bed snps.bed \
       --fasta_ref /mnt/data/GRCh38_no_alt_analysis_set_GCA_000001405.15.fasta \
       --out_prefix $fasta_prefix \
       --flank 500

#predictions & interpretations for {effect,noneffect} x {GM12878, H1ESC, HEPG2, IMR90, K562} x {DNASE & ATAC} x {folds 0-9}
for assay in atac dnase
do
    for fold in `seq 0 9`
    do
	for line in GM12878 H1ESC HEPG2 IMR90 K562
	do
	    for allele in effect noneffect
	    do
		input_fasta=$fasta_prefix.$allele.fa
		model=$model_prefix/$assay/$line/models/model.$line.$fold.txt
		output_pred=pred.$assay.$line.$fold.$allele.txt
		output_interpret=interp.$assay.$line.$fold.$allele.txt
		gkmpredict -v2  $input_fasta $model $output_pred 
		gkmexplain $input_fasta $model $output_interpret 
		#make bigwig
		python $repo_prefix/utils/gkmexplain_to_bigwig.py --gkmexplain_out $output_interpret \
		       --chrom_index 0 \
		       --pos_index 1 \
		       --allele_index -1 \
		       --chrom_sizes /mnt/data/hg38.chrom.sizes \
		       --ref_fasta /mnt/data/GRCh38_no_alt_analysis_set_GCA_000001405.15.fasta \
		       --out_bigwig $assay.$line.$fold.$allele.bw
	    done
	done
    done
done


#visualize the interpretations
for assay in atac dnase
do
    for line in GM12878 H1ESC HEPG2 IMR90 K562
    do
	python $repo_prefix/plot_interpretations/plot_folds.py --snpinfo snps.bed \
	       --gkmexplain_prefix interp.$assay.$line \
	       --gkmexplain_suffix .txt \
	       --out_prefix interp.$assay.$line \
	       --flank 500 \
	       --plot_start_base 400 \
	       --plot_end_base 600 \
	       --snp_pos 501
    done
done
