import numpy as np
import matplotlib.pyplot as plt
import time

from sklearn.decomposition import PCA
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import ShuffleSplit

from data.read import MnistDataloader
from utils.visualize import plot_learning_curve

visualize = False


mnist_dataloader = MnistDataloader()
X_train, y_train, X_test, y_test = mnist_dataloader.load_data()

# vectorize image 
X_train = X_train.reshape(60000, 784) 
X_test = X_test.reshape(10000, 784)  
X_train = X_train.astype('float32') / 255.
X_test = X_test.astype('float32') / 255.


print('\n' + '-'*10 + "MLP classifier on original dataset" + '-'*10)

tic = time.time()
clf = MLPClassifier(batch_size=256, activation = 'relu', solver='adam', 
                    max_iter=100, early_stopping=True).fit(X_train, y_train)
toc = time.time()

print("time elapsed: {:.5f} sec".format(toc-tic))
print('train acc: {:2.2f}%'.format(100*clf.score(X_train, y_train)))
print('test acc: {:2.2f}%'.format(100*clf.score(X_test, y_test)))


list_variance = [.85, .90, .95, .99]

if visualize:
    cv = ShuffleSplit(n_splits=5, test_size=0.2, random_state=0)
    fig, axes = plt.subplots(1, 4, figsize=(12, 5), dpi=150)


for i, variance in enumerate(list_variance):
    print('-'*60)
    print(f'Dataset dimensional reduction with {variance*100}% variance retained')
    print('-'*60)

    pca = PCA(n_components=variance)
    pca.fit(X_train)

    train = pca.transform(X_train)
    test = pca.transform(X_test)

    tic = time.time()
    clf = MLPClassifier(batch_size=256, activation = 'relu', solver='adam', 
                        max_iter=100, early_stopping=True).fit(train, y_train)
    toc = time.time()

    print(f'variance: {list_variance[i]*100}%')
    print("components:", train.shape[1])
    print("time elapsed: {:.5f} sec".format(toc-tic))
    print('train acc: {:2.2f}%'.format(100*clf.score(train, y_train)))
    print('test acc: {:2.2f}%'.format(100*clf.score(test, y_test)))

    if visualize:
        title = f'variance: {list_variance[i]*100}%'
        plot_learning_curve(clf, title, test, y_test, axes=axes[i], ylim=(0.5, 1.01), cv=cv, n_jobs=-1)

if visualize:
    plt.tight_layout()
    plt.savefig("docs/pca")  