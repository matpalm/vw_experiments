#!/usr/bin/env python

# generate a confusion matrix
# code take nearly verbatim from 
# http://stackoverflow.com/questions/5821125/how-to-plot-confusion-matrix-with-string-axis-rather-than-integer-in-python

import numpy as np
import matplotlib.pyplot as plt
import sys, re

predictions_file, group_id_seqs_file, output_file = sys.argv[1:]

# read group -> seq (this represents the correct value)
group_to_label = {}
groups = []
for line in open(group_id_seqs_file, 'r'):
    group, label = line.strip().split("\t")
    group_to_label[group] = int(label)
    groups.append(group)

# read predictions and built up confusion matrix
conf_arr = np.zeros((20,20))
correct = wrong = 0
for line in open(predictions_file, 'r'):
    prediction, example_label = line.strip().split(" ")
    prediction = int(float(prediction))
    group = re.sub("_.*", '', example_label)
    actual = group_to_label[group]
    conf_arr[prediction-1, actual-1] += 1
    if prediction == actual:
        correct += 1
    else:
        wrong += 1
    
print "correct", correct, "wrong", wrong

norm_conf = []
for i in conf_arr:
    a = 0
    tmp_arr = []
    a = sum(i, 0)
    for j in i:
        tmp_arr.append(float(j)/float(a))
    norm_conf.append(tmp_arr)

fig = plt.figure()
plt.clf()
ax = fig.add_subplot(111)
plt.setp([], fontsize=4)
res = ax.imshow(np.array(norm_conf), cmap=plt.cm.jet, 
                interpolation='nearest')

width = len(conf_arr)
height = len(conf_arr[0])

#for x in xrange(width):
#    for y in xrange(height):
#        ax.annotate(str(conf_arr[x][y]), xy=(y, x), 
#                    horizontalalignment='center',
#                    verticalalignment='center')

cb = fig.colorbar(res)
alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
# ylabels have group name then alpha

# xlabels have just alpha
plt.yticks(range(height), groups) # ['ad','sdv','ertr']) #lphabet[:height])
plt.xticks(range(width), alphabet[:width])

plt.savefig('confusion_matrix.png', format='png')
