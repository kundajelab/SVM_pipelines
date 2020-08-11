The code assumes you have a bed file with the following columns:

* Chromosome
* Start Position (0-indexed SNP pos)
* End Position (1-indexed SNP pos)
* RSID (or some other SNP name)
* Effect allele
* Noneffect allele


Begin by splitting the bed file into the number of chunks you would like to process in parallel.
I.e. if you want 100 chunks you can run the following: 

```
split -d -n 100 mybed.bed
```

This will generate 100 output files prefixed x00 - x99

Execute **get_seqs.sh** to generate fasta input sequences for each chunk

If running on sherlock or scg, execute **sbatch.explain.sh** to submit the gmkexplain jobs.
**sbatch.explain.sh** is a wrapper around **explain.sh**.


Run **aggregate.sh** to collect the gkmexplain outputs across the chunks.
