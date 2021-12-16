"""Test for the file_rename function - this module uses unittest. 
1 smoke test
1 one shot test
3 edge tests
"""

from os import renames, unlink
from pathlib import Path
import unittest

from data_cleaning import rename_files

class TestRename(unittest.TestCase):

    def test_smoke(self):
        """Smoke test to make sure function runs
        """
              
        rename_files()
        return

