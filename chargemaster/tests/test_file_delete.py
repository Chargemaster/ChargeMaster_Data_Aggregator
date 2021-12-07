"""Test for the delete_files function - this module uses unittest. 
1 smoke test
1 one shot test
3 edge tests
"""

from os import renames, unlink
import pathlib
import unittest

from file_delete import delete_files

class TestDelete(unittest.TestCase):

    def test_smoke(self):
        """Smoke test to make sure function runs
        """
        
        delete_files("/Users/maxsgro/Documents/Chargemaster/scraped_data")
        return

    # def test_oneshot(self):
    #     """
    #     One shot test that inputs equal 773.33 as given in example
    #     """
    #     n_neighbors = 3
    #     data = np.array([[3, 1, 230],
    #              [6, 2, 745],
    #              [6, 6, 1080],
    #              [4, 3, 495],
    #              [2, 5, 260]])
    #     query = np.array([5, 4])    
        
    #     if np.isclose(knn_regression(data, query, n_neighbors),773.33, atol=1e-1):
    #         print("Test passed")
    #     else:
    #         print("Test failed")
    #     # self.assertEqual(output,773.33)
    #     return
    #     # assert np.isclose(knn_regression(data, query, n_neighbors),np.array([773.33])
    #     # return

    # def test_edgetest_one(self):
    #     """
    #     Edge Test to check that value error is raised when query is greater than 2 dimensions
    #     """
    #     n_neighbors = 4
    #     data = np.array([[3, 1, 230],
    #              [6, 2, 745],
    #              [6, 6, 1080],
    #              [4, 3, 495],
    #              [2, 5, 260]])
    #     query = np.array([5, 4, 5])    
        
    #     with self.assertRaises(ValueError):
    #         knn_regression(data, query, n_neighbors)
    #     return

    # def test_edgetest_two(self):
    #     """
    #     Edge Test to check that ValueError is raised when n_neighbors is 0
    #     """
    #     n_neighbors = 0
    #     data = np.array([[3, 1, 230],
    #              [6, 2, 745],
    #              [6, 6, 1080],
    #              [4, 3, 495],
    #              [2, 5, 260]])
    #     query = np.array([5, 4])    
        
    #     with self.assertRaises(ValueError):
    #         knn_regression(data, query, n_neighbors)
    #     return    

    # def test_edgetest_three(self):
    #     """
    #     Edge test to check that input data array is in a shape of 5x3
    #     """
    #     n_neighbors = 0
    #     data = np.array([[3, 1, 230, 40],
    #              [6, 2, 745, 40],
    #              [6, 6, 1080, 40],
    #              [4, 3, 495, 40],
    #              [2, 5, 260, 40]])
    #     query = np.array([5, 4])    
        
    #     with self.assertRaises(ValueError):
    #         knn_regression(data, query, n_neighbors)
    #     return   