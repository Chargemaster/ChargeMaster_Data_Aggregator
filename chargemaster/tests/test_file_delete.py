"""Test for the delete_files function - this module uses unittest. 
1 smoke test
1 one shot test
3 edge tests
"""

from os import renames, unlink
import pathlib
import unittest
import os

from data_cleaning import delete_files

class TestDelete(unittest.TestCase):

    def test_smoke(self):
        """Smoke test to make sure function runs
        """
        
        delete_files()
        return
    
    def test_oneshottest_one(self):
        """
        One shot Test to check that value error is raised when query is greater than 2 dimensions
        """
        parent_dir = pathlib.Path(__file__).parents[2]/"data"/"scraped_data"  
        directory = "random_hospital"
        path = os.path.join(parent_dir, directory)
        os.mkdir(path)
        with open(os.path.join(path, "nothing.txt"), 'w') as fp:
            pass
        with open(os.path.join(path, "data.csv"), 'w') as fp:
            pass
        delete_files()

        return