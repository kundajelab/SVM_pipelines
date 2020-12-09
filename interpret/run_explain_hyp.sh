#!/bin/bash

model=$1
infile=$2
outfile=$3
lsgkm_dir=$4

$lsgkm_dir/gkmexplain -m 1 $infile $model $outfile

