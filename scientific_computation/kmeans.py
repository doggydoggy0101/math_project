import numpy as np
import time

from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import accuracy_score

from data.read import MnistDataloader
from utils.cluster import infer_cluster_labels, infer_data_labels

mnist_dataloader = MnistDataloader()
X_train, y_train, X_test, y_test = mnist_dataloader.load_data()

# vectorize image 
X_train = X_train.reshape(60000, 784)
X_test = X_test.reshape(10000, 784) 
X_train = X_train.astype('float32') / 255.
X_test = X_test.astype('float32') / 255.


list_cluster = [10, 64, 128, 256]

for n_clusters in list_cluster:
    print('-'*60)
    print(f'Number of {n_clusters} clusters')

    tic = time.time()
    kmeans = KMeans(n_clusters, n_init="auto").fit(X_train)
    toc = time.time()
    print("time elapsed: {:.5f} sec".format(toc-tic))

    cluster_labels = infer_cluster_labels(kmeans, y_train)
    pred_train = infer_data_labels(kmeans.labels_, cluster_labels)
    print("training acc: {:2.2f}%".format(100*accuracy_score(y_train, pred_train)))

    predict_labels = kmeans.predict(X_test)
    pred_test = infer_data_labels(predict_labels, cluster_labels)
    print("testing acc: {:2.2f}%".format(100*accuracy_score(y_test, pred_test)))


n_clusters = 256
print("\nApply PCA to Kmeans with fixed number of clusters {}".format(n_clusters))


list_variance = [.85, .90, .95, .99]

for i, variance in enumerate(list_variance):
    print('-'*60)
    print(f'Dataset dimensional reduction with {variance*100}% variance retained')
    print('-'*60)

    pca = PCA(n_components=variance)
    pca.fit(X_train)

    train = pca.transform(X_train)
    test = pca.transform(X_test)

    tic = time.time()
    kmeans = KMeans(n_clusters, n_init="auto").fit(train)
    toc = time.time()
    print("time elapsed: {:.5f} sec".format(toc-tic))

    cluster_labels = infer_cluster_labels(kmeans, y_train)
    pred_train = infer_data_labels(kmeans.labels_, cluster_labels)
    print("training acc: {:2.2f}%".format(100*accuracy_score(y_train, pred_train)))

    predict_labels = kmeans.predict(test)
    pred_test = infer_data_labels(predict_labels, cluster_labels)
    print("testing acc: {:2.2f}%".format(100*accuracy_score(y_test, pred_test)))