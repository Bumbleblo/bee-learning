import unittest

from unittest import TestCase

import tensorflow as tf

from tensorflow import SparseTensor

from infer import preprocessing_fn

import logging
logger = tf.get_logger()

logger.setLevel(logging.CRITICAL)


class TestInfer(TestCase):

    def setUp(self):

        self.keys = ['PassengerId', 'Survived', 'Pclass']

        tensor = SparseTensor(indices=[[0, 0], [1, 2]], values=[1, 2], dense_shape=[3, 4])

        self.input = dict()

        for key in self.keys:
            self.input[key] = tensor

    def test_verify_keys(self):

        output = preprocessing_fn(self.input)

        for key in self.keys:
            self.assertIn(key, output.keys())

        
    




if __name__ == '__main__':
    unittest.main()
