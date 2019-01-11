"""
Created:   Dec 16, 2018
encoding:  UTF-8
Author:    Shuheng Liu
Contact:   wish1104@outlook.com
GitHub:    https://github.com/Johnny-Wish

(c) All Rights Reserved
License: https://choosealicense.com/licenses/gpl-3.0/

This file contains pre-processing tools of the dataset, assumed to be of a standard .mat format
"""

import os
import numpy as np
from scipy.io import loadmat
from sklearn.preprocessing import LabelEncoder


class Subset:
    def __init__(self, X, y, feature_shape=(-1,), encoder=None):
        """
        An object simulating the training set / testing test / validation set of a super dataset
        :param X: A 2-dim np.ndarray, n_samples x n_feature_dims
        :param y: A 1-dim/2-dim np.ndarray, n_samples or n_samples x 1
        :param encoder: a fitted LabelEncoder instance or a callable that returns an encoded label vector
        """
        self._X = np.reshape(X, (len(X), *feature_shape))
        self._y = y

        if isinstance(self._y, np.ndarray) and len(self._y.shape) == 2:
            self._y = self._y.flatten()  # the method np.ndarray.flatten() is stupid and doesn't update `self`

        # if an encoder is given, encode labels accordingly
        if isinstance(encoder, LabelEncoder):
            self._y = encoder.transform(self._y)
        elif callable(encoder):
            self._y = encoder(self._y)

        assert len(self._X) == len(self._y), "X and y differ in length {} != {}".format(len(self._X), len(self._y))

    @property
    def X(self):
        return self._X

    @property
    def y(self):
        return self._y

    def __dict__(self):
        return {"X": self._X, "y": self._y}

    @classmethod
    def from_dict(cls, d):
        return cls(
            X=d.get("X", None),
            y=d.get("y", None),
        )

    def sampled(self, size=1.0):
        """
        return a new Subset instance which is contained in `self`
        :param size: float or int, size of the new instance
            if float. construed as the ratio to the original instance
            if size, construed as the number of elements in the returned instance
            size of new instance will be ceiled if it exceeds the maximum
        :return: a new Subset instance
        """
        total = len(self)
        if isinstance(size, (int, np.integer)):
            sample = min(total, size)
        else:
            sample = int(total * min(size, 1.0))
        index = np.random.choice(np.arange(total), sample, replace=False)
        return Subset(self._X[index], self._y[index])

    def __len__(self):
        return min(len(self._X), len(self._y))  # in case X and y differ in length, which should not happen

    def __getitem__(self, item):
        assert 0 <= item < len(self)
        return {
            "X": self._X[item],
            "y": self._y[item],
        }

    def __repr__(self):
        return "<Subset: X={}, y={}>".format(self._X, self._y)


class Dataset:
    def __init__(self, filename="emnist-byclass.mat", folder="dataset", label_order=None):
        """
        An object representing a dataset, consisting of training set and testing set
        :param filename: name of the .mat file, including extensions
        :param folder: path to the folder containing data files
        :param label_order: "shift", "reorder" or None, whether and how to treat label orders
        """
        dataset = loadmat(os.path.join(folder, filename)).get("dataset", None)
        train, test, mapping = dataset[0][0]
        train, test = train[0][0], test[0][0]  # `train` and `tests` are tuples of (images, labels, writers)

        if label_order == "shift":
            lower_bound = min(np.min(train[1]), np.min(test[1]))
            self._encoder = lambda old: old - lower_bound
            self._decoder = lambda new: new + lower_bound
        elif label_order == "reorder":
            self._encoder = LabelEncoder().fit(train[1])
            self._decoder = self._encoder
        else:
            if label_order is not None:
                print("unrecognized label order {}".format(label_order))
            self._encoder = None
            self._decoder = None

        self._train = Subset(X=train[0], y=train[1], encoder=self._encoder)
        self._sampled_train = self._train
        self._train_size = len(self._train)
        self._test = Subset(X=test[0], y=test[1], encoder=self._encoder)
        self._sampled_test = self._test
        self._test_size = len(self._test)
        self._mapping = mapping

    def sample_train(self, size=0.1):
        self._sampled_train = self._train.sampled(size)
        self._train_size = len(self._sampled_train)
        return self

    def sample_test(self, size=0.1):
        self._sampled_test = self._test.sampled(size)
        self._test_size = len(self._sampled_test)
        return self

    @property
    def train_size(self):
        return self._train_size

    @property
    def test_size(self):
        return self._test_size

    @property
    def encoder(self):
        return self._encoder

    @property
    def decoder(self):
        return self._decoder

    @property
    def train(self):
        return self._sampled_train

    @property
    def test(self):
        return self._sampled_test

    @property
    def mapping(self):
        return self._mapping

    def __dict__(self):
        return {"train": self._train, "test": self._test, "mapping": self._mapping}

    @classmethod
    def from_dict(cls, d):
        instance = Dataset.__new__(cls)
        instance._train = d.get("train")
        instance._test = d.get("test")
        instance._mapping = d.get("mapping")
        return instance

    def __repr__(self):
        return "<Dataset: train={}, test={}>".format(self._train, self._test)
