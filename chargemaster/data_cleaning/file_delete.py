""" This script deletes non .csv and .xlsx files from the scraped file output.
It should be used before file_rename.py and a source directory should be added
as path_name.
"""

#from os import renames, unlink
import pathlib
import os

#This program works to delete files in scraper folder that are not data files.

def delete_files():
    """ This script iterates through all hospital folders in the directory path_name
    and deletes files that are not .csv or .xlsx"""
    path = pathlib.Path(__file__).parents[2]/"data"/"scraped_data"
    isdir = os.path.isdir(path)
    dirname1 = os.path.basename(path)
    if isdir != True:
        raise ValueError ("Not a valid directory")
    if dirname1 != "scraped_data":
        raise ValueError ("Wrong Directory Specified")
    #print(path)
    
    for folder in path.iterdir():
        if folder.is_dir():
            
            for file in folder.iterdir():
                if file.is_file():
                    if file.suffix == ".csv":
                       pass

                    elif file.suffix == ".xlsx":
                        pass

                    else:

                        file.unlink()
            
                    

#delete_files()