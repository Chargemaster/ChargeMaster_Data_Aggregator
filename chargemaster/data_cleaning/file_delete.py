""" This script deletes non .csv and .xlsx files from the scraped file output.
It should be used before file_rename.py and a source directory should be added
as path_name.
"""

from os import renames, unlink
import pathlib
import os

#This program works to delete files in scraper folder that are not data files.

def delete_files():
    """ This script iterates through all hospital folders in the directory path_name
    and deletes files that are not .csv or .xlsx"""
    # path = pathlib.Path(path_name)
    path = os.path.abspath(__file__+"/../../../data/scraped_data")
    isdir = os.path.isdir(path)
    dirname1 = os.path.basename(path)
    if isdir != True:
        raise ValueError ("Not a valid directory")
    if dirname1 != "scraped_data":
        raise ValueError ("Wrong Directory Specified")
    
    for folder in path.iterdir():
        if folder.is_dir():
            #counter = 1
            # folder_name = file.stem
            # print("This is the folder name: ", folder_name)
            for file in folder.iterdir():
                if file.is_file():
                    if file.suffix == ".csv":
                       pass
                       #print("this we keep: ", file.suffix)
                    elif file.suffix == ".xlsx":
                        pass
                        #print("this we keep: ", file.suffix)
                    else:
                        #print("this we delete: ", file.suffix)
                        file.unlink()
            
                    

delete_files()