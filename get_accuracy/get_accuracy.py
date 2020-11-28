import os
import sys
from sklearn.metrics import roc_auc_score, average_precision_score

train_dir = sys.argv[1]

for cluster in os.listdir(train_dir):
    if cluster != 'logs':
        print(cluster)
        if not os.path.isdir(train_dir + '/' + cluster + '/accuracy'):
            os.mkdir(train_dir + '/' + cluster + '/accuracy')
        for fold in range(10):
            pos_file = train_dir + '/' + cluster + '/predictions/' + cluster + '.' + str(fold) + '.positives'
            neg_file = train_dir + '/' + cluster + '/predictions/' + cluster + '.' + str(fold) + '.negatives'

            pos_preds = [float(x.rstrip().split("\t")[1]) for x in open(pos_file)]
            neg_preds = [float(x.rstrip().split("\t")[1]) for x in open(neg_file)]

            pos_accuracy = sum([1 for x in pos_preds if x > 0]) / len(pos_preds)
            neg_accuracy = sum([1 for x in neg_preds if x < 0]) / len(neg_preds)

            auroc = roc_auc_score(y_true = [1 for x in pos_preds] + [0 for x in neg_preds],
                                  y_score = pos_preds + neg_preds)
            auprc = average_precision_score(y_true = [1 for x in pos_preds] + [0 for x in neg_preds],
                                             y_score = pos_preds + neg_preds)

            with open(train_dir + '/' + cluster + '/accuracy/' + cluster + '.' + str(fold) + '.accuracy', 'w') as acc_file:
                acc_file.write('\n' + 'Cluster: ' + cluster + '; Fold: ' + str(fold) + '\n' + '\n')
                acc_file.write('AUROC: ' + str(auroc) + '\n')
                acc_file.write('AUPRC: ' + str(auprc) + '\n')
                acc_file.write('Pos Accuracy: ' + str(pos_accuracy) + '\n')
                acc_file.write('Neg Accuracy: ' + str(neg_accuracy) + '\n' + '\n')
                acc_file.write('-----------------------------------------' + '\n')

