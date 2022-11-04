# SVM_pipelines

Example use case on Kundaje lab cluster for SVM input generation: 

```
/mnt/lab_data2/annashch/alzheimers_parkinsons/svm_pipeline/make_inputs
```

Execute scripts in `make_inputs` to generate input files for SVM model training.  
 
Execute scripts in `train_predict` to train SVM models and get model predictions.  

Execute scripts in `score` to get auPRC & other metrics of model performance.  

Execute scripts in `interpret` to run gkmexplain interpretation.  

Execute scripts in `plot_interpretations` to plot gkmexplain interpretations.  

Execute `util.gkmexplain_to_bigwig.py` to generate a bigwig representation of gkmexplain scores


Note: SVM models for ENCODE tier 1 lines have been pre-trained and stored on oak at this location: 

```
/oak/stanford/groups/akundaje/projects/chrombpnet/svm/dnase
/oak/stanford/groups/akundaje/projects/chrombpnet/svm/atac
```

Predictions for bQTL datasets ref & alt alleles are here: 
```
/oak/stanford/groups/akundaje/projects/chrombpnet/svm/bQTL
```

Predictions genomewide for models trained on tier 1 DNASE data are here: 
```
/oak/stanford/groups/akundaje/projects/chrombpnet/svm/genomewide_encode_tier1_lines_dnase
```
