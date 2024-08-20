import numpy as np
import matplotlib.pyplot as plt
import time

from sklearn.svm import SVC
from sklearn.decomposition import PCA

from data.read import MnistDataloader

visualize = False
kernel = "rbf" # linear, poly, rbf, sigmoid
C = 10
gamma = 0.01
max_iter = 100

mnist_dataloader = MnistDataloader()
X_train, y_train, X_test, y_test = mnist_dataloader.load_data()

# vectorize image 
X_train = X_train.reshape(60000, 784) 
X_test = X_test.reshape(10000, 784)  
X_train = X_train.astype('float32') / 255.
X_test = X_test.astype('float32') / 255.


tic = time.time()
svm = SVC(kernel=kernel, C=C, gamma=gamma, max_iter=max_iter).fit(X_train, y_train)
toc = time.time()
print("time elapsed: {:.5f} sec".format(toc-tic))
print('train acc: {:2.2f}%'.format(100*svm.score(X_train, y_train)))
print('test acc: {:2.2f}%'.format(100*svm.score(X_test, y_test)))


if visualize:

    svm_coef = svm.dual_coef_
    n_supp = svm.n_support_
    supp_vec = svm.support_

    ind = 0
    plt.subplots(2, 5, figsize=(12,5))
    for i in range(len(n_supp)):
        l1 = plt.subplot(2, 5, i + 1)
        sv_image = X_train[supp_vec[ind:ind+n_supp[i]]][0]
        l1.imshow(sv_image.reshape(28, 28), cmap=plt.cm.RdBu_r)
        l1.set_xticks(())
        l1.set_yticks(())
        l1.set_xlabel('Class %i vs All' % i)
        ind = ind + n_supp[i]
    plt.suptitle('Support Vectors for Positive Classes')
    plt.savefig("docs/svm_" + kernel + "_pos") 

    ind = n_supp[0]
    plt.subplots(2, 5, figsize=(12,5))
    for i in range(len(n_supp)-1):
        l1 = plt.subplot(2, 5, i + 1)
        sv_image = X_train[supp_vec[ind:ind+n_supp[i+1]]][100]
        l1.imshow(sv_image.reshape(28, 28), cmap=plt.cm.RdBu_r)
        l1.set_xticks(())
        l1.set_yticks(())
        l1.set_xlabel('Class %i vs All' % i)
        ind = ind + n_supp[i+1]
    ind = 0
    l1 = plt.subplot(2, 5, 10)
    sv_image = X_train[supp_vec[ind:ind+n_supp[0]]][100]
    l1.imshow(sv_image.reshape(28, 28), cmap=plt.cm.RdBu_r)
    l1.set_xticks(())
    l1.set_yticks(())
    l1.set_xlabel('Class 9 vs All')
    plt.suptitle('Support Vectors for Negative Classes')
    plt.savefig("docs/svm_" + kernel + "_neg") 




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
    svm = SVC(kernel=kernel, C=C, gamma=gamma, max_iter=max_iter).fit(train, y_train)
    toc = time.time()
    print("time elapsed: {:.5f} sec".format(toc-tic))
    print('train acc: {:2.2f}%'.format(100*svm.score(train, y_train)))
    print('test acc: {:2.2f}%'.format(100*svm.score(test, y_test)))