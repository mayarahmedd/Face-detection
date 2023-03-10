# -*- coding: utf-8 -*-
"""AI_Project2_MachineLearining.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Wgb8jxLFKM-1CTVzMtw8Lhh8y9NjFsw9

**Imports and Fetching data from lfw (Labeled Faces in the Wild) Dataset**
"""

from numpy import mean
from numpy import std
from sklearn import datasets
from sklearn.decomposition import PCA
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
dataSet = datasets.fetch_lfw_people(min_faces_per_person=70)
# dataSet = datasets.load_digits()
# print(dataSet.feature_names)

"""**Printing target**"""

print(dataSet.target)

"""**Printing Target name**"""

print(dataSet.target_names)

"""**Printing the shape of data**"""

print(dataSet.data.shape)

"""**X has the image data, y has target (the index of the image) and training the data and splitting it for test**"""

X = dataSet.data.reshape(len(dataSet.data), -1) #Converting 2d array to Vector
y = dataSet.target
target_names = dataSet.target_names
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20)

"""**Convert X_train to zero mean and variance of 1 to be easier to use by using the PCA(Principal Component Analysis) to fit the X_train which reduce the variable numbers to smaller number to be easier and faster to deal with, whiten is used to make input less redundent**"""

# performing preprocessing part
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

# Compute a PCA 
n_components = 75
pca = PCA(n_components=n_components, whiten=True).fit(X_train)
#n_components -> principal components used in dimensionality reduction
#whiten -> it is needed for some algorithms. If we are training on images, the raw input is redundant, 
#since adjacent pixel values are highly correlated. The goal of whitening is to make the input less redundant
# apply PCA transformation
X_train_pca = pca.transform(X_train)
X_test_pca = pca.transform(X_test)

"""**Naive Bayes is used which gave an accuracy between 0.7-0.8**"""

from sklearn.naive_bayes import GaussianNB
# from sklearn.neighbors import KNeighborsClassifier
print("Fitting the classifier to the training set")
# clf = KNeighborsClassifier(n_neighbors=7).fit(X_train_pca, y_train)
clf= GaussianNB().fit(X_train_pca, y_train)
# clf= GaussianNB(var_smoothing=2e-5).fit(X_train_pca, y_train)
#1e-9 -> default variance so when decreasing it , accuracy decreases

"""**Using test in prediction and printing a classification report and an accuracy score**"""

y_pred = clf.predict(X_test_pca)
print(metrics.classification_report(y_test, y_pred, target_names=target_names))
print("Accuracy:",metrics.accuracy_score(y_test, y_pred))

"""**KFold is used to cross so that the test data and trained data are merged and the naive bayes model is used**"""

for i in range(5,20):
  # cv = KFold(n_splits=i, random_state=1, shuffle=True)
  cv = KFold(n_splits=i)
  scores = cross_val_score(clf, X_train_pca, y_train, scoring='accuracy', cv=cv, n_jobs=-1)
  # report performance
  print('Accuracy: %.3f (%.3f)' % (mean(scores), std(scores)))