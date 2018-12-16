import unittest
import numpy as np
from preprocess import Dataset, Subset


class TestSubset(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestSubset, self).__init__(*args, **kwargs)
        self.n_samples = 100
        self.n_dim = 15
        X = np.random.rand(self.n_samples, self.n_dim)
        y = np.random.rand(self.n_samples)
        self.subset = Subset(X, y)

    def test_must_pass(self):
        self.assertTrue(True)

    def test_equal_length(self):
        self.assertEqual(len(self.subset.X), len(self.subset.y))

    def test_not_none(self):
        self.assertIsNotNone(self.subset.X)
        self.assertIsNotNone(self.subset.y)

    def test_not_empty(self):
        self.assertGreater(len(self.subset.X), 0)
        self.assertGreater(len(self.subset.y), 0)

    def test_output_dict(self):
        d = self.subset.__dict__()
        self.assertIsInstance(d, dict)
        self.assertIn("X", d)
        self.assertIn("y", d)
        self.assertEqual(len(d), 2)

    def test_from_dict(self):
        d = {
            "X": np.random.rand(self.n_samples, self.n_dim),
            "y": np.random.rand(self.n_samples),
        }
        subset = Subset.from_dict(d)
        d2 = subset.__dict__()
        self.assertTrue((d['X'] == d2['X']).all())
        self.assertTrue((d['y'] == d2['y']).all())

    def test_raise_error(self):
        with self.assertRaises(AssertionError):
            Subset(
                np.random.rand(self.n_samples + 1, self.n_dim),
                np.random.rand(self.n_samples)
            )


class TestDataset(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestDataset, self).__init__(*args, **kwargs)
        self.test_build_dataset()

    def test_build_dataset(self):
        self.dataset = Dataset(folder="../dataset")

    def test_sample_size(self):
        self.assertEqual(self.dataset.train.X.shape[0], self.dataset.train.y.shape[0])
        self.assertEqual(self.dataset.test.X.shape[0], self.dataset.test.y.shape[0])

    def test_dimension_size(self):
        self.assertEqual(self.dataset.train.X.shape[1], self.dataset.test.X.shape[1])
        self.assertEqual(self.dataset.train.y.shape[1], self.dataset.test.y.shape[1])

    def test_type(self):
        self.assertIsInstance(self.dataset.mapping, np.ndarray)
        self.assertIsInstance(self.dataset.train.X, np.ndarray)
        self.assertIsInstance(self.dataset.train.y, np.ndarray)
        self.assertIsInstance(self.dataset.test.X, np.ndarray)
        self.assertIsInstance(self.dataset.test.y, np.ndarray)