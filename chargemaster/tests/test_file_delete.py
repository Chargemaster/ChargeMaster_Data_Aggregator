"""Test for the delete_files function - this module uses unittest. 
1 smoke test
1 one shot test
3 edge tests
"""

from os import renames, unlink
import pathlib
import unittest

from data_cleaning import delete_files

class TestDelete(unittest.TestCase):

    def test_smoke(self):
        """Smoke test to make sure function runs
        """
        
        delete_files()
        return 