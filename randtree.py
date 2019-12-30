# -*- coding: utf-8 -*-
# @Time    : 2018/8/21 9:35
# @Author  : Barry
# @File    : mnist.py
# @Software: PyCharm Community Edition

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import tensorflow.examples.tutorials.mnist.input_data as input_data

import tensorflow as tf
mnist = tf.keras.datasets.mnist
(X_train, y_train), (X_test, y_test) = mnist.load_data()



# data_dir = 'MNIST_data/'
# mnist = input_data.read_data_sets(data_dir, one_hot=False)
# batch_size = 50000
# batch_x, batch_y = mnist.train.next_batch(batch_size)
# test_x = mnist.test.images[:10000]
# test_y = mnist.test.labels[:10000]

print("start random forest")
for i in range(10, 200, 10):
    clf_rf = RandomForestClassifier(n_estimators=i)
    clf_rf.fit(X_train, y_train)

    y_pred_rf = clf_rf.predict(X_test)
    acc_rf = accuracy_score(y_test, y_pred_rf)
    print("n_estimators = %d, random forest accuracy:%f" % (i, acc_rf))
