"""
Author: Ji Kang
November 30, 2021

Tests for KNN module. Using the unittest module, there're multiple unit tests
that'll go over the validity of the data provided. It will examine the
dimensions, data types of the data itself, and if they are valid values
for the program.

Additionally, there're tests that do sanity checks on whether the
KNN program itself is returning correct data.
"""
import unittest
import sys
import numpy as np
import requests

# Need to append path to access the knn file.
sys.path.append('./chargemaster/web_scraper')


class TestScraper(unittest.TestCase):
    """
    Smoke test to make sure the "knn_regression" function runs. This utilizes
    the sample data given to us.
    """
    def test_smoke(self):
        """
        Smoke test to make sure that the program can actually run.
        """
        knn_regression(n_neighbors=3, data=sample_data, query=sample_query)

    def test_sample_data(self):
        """
        Runs the sample data given to us as part of the homework. 'CORRECT_ANSWER' is set
        to the given answer.
        """
        correct_answer = 773.33 # Given to us from the homework page
        answer = knn_regression(3, sample_data, sample_query)
        assert answer == correct_answer

    def test_varying_num_neighbors(self):
        """
        Testing the varying number of neighbors given the sample data.
        Hand calculated so obviously some room for error but I am fairly sure they are correct.
        Will also test negative number of neighbors.
        """
        # Hand calculated using given data
        correct_answers = [None, None, None, None, None, None, 495.0, 620.0, 773.33, 645.0]
        num_neighbors_list = list(range(-5, 5))
        for num_neighbors, correct_answer in zip(num_neighbors_list, correct_answers):
            try:
                answer = knn_regression(num_neighbors, sample_data, sample_query)
                # If "correct_answer" is not 'None', it should equal the answer returned
                if correct_answer:
                    assert answer == correct_answer
            except ValueError:
                # If a ValueError is thrown, 'correct_answer' should be None
                # since a num_neighbors of less than 1 was given.
                assert correct_answer is None

    def test_invalid_neighbor_values(self): # strings and negative number of neighbors
        """
        Tests the how the program handles invalid number of neighors. This test will also include
        some valid entries. So far, it will test negative number of neighbors,
        having invalid types, as well as a 'number' but in string format.
        """
        correct_answers = [None, None, None, None, None, None, 495.0, 620.0, 773.33, 645.0]
        num_neighbors_list = list(range(-5, 5))
        num_neighbors_list = [str(x) if x % 2 == 0  else x for x in num_neighbors_list]
        answer = -1 #placeholder
        for num_neighbors, correct_answer in zip(num_neighbors_list, correct_answers):
            try:
                answer = knn_regression(num_neighbors, sample_data, sample_query)
                if correct_answer: # If not NoneType
                    assert answer == correct_answer
            except ValueError: # Should throw a ValueError. Otherwise, it's invalid.
                assert True
            except Exception:
                assert False

    def test_different_queries(self):
        """
        Goes through different queries and compares answers to hand
        calculated values as the ground truth.
        """
        num_neighbors = 3
        data = np.array([[3, 1, 230],
                [6, 2, 745],
                [6, 6, 1080],
                [4, 3, 495],
                [2, 5, 260]])
        queries = np.array([[5, 4],
                [1, 2],
                [0, 0],
                [5, 8],
                [10, 10],
                [100, 100],
                [3, 4],
                [5, 6]])
        correct_answers = [773.33, 328.33, 328.33, 611.67, 773.33, 773.33, 328.33, 611.67]
        for correct_answer, query in zip(correct_answers, queries):
            answer = knn_regression(num_neighbors, data, query)
            assert answer == correct_answer

    def test_matrix_dims_error(self):
        """
        Tests different shapes for query and data. Custom exception class
        to test numpy array dimensions. Must make sure it follows
        that data's shape is (m, n+1) and query is (n, )
        """
        # VALID data dimensions
        query = np.empty(shape=(3,))
        data = np.empty(shape=(5,4))
        knn_regression(3, data, query)

        # INVALID data dimensions
        try:
            query = np.empty(shape=(5,5)) #invalid dimensions for query
            data = np.empty(shape=(3, 4)) # valid
            knn_regression(3, data, query)
        except MatrixDimensionError:
            assert True # This should only throw a MatrixDimensionError.
        except Exception:
            assert False # Any other exception type is invalid here.

        # INVALID data dimensions
        try:
            query = np.empty(shape = (100,))
            data = np.empty(shape=(5, 100)) # invalid shape. should be (5, 101)
            knn_regression(3, data, query)
        except MatrixDimensionError:
            assert True # This should only throw a MatrixDimensionError.
        except Exception:
            assert False # Any other exception type is invalid here.