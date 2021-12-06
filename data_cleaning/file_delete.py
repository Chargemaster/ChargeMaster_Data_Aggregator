""" This script deletes non .csv and .xlsx files from the scraped file output.
It should be used before file_rename.py and the source folder "scraped_data" which
is in the same working directory.
"""

from os import renames, unlink
import pathlib

#This program works to delete files in scraper folder that are not data files.

def delete_files():
    """ This script iterates through all hospital folders in the scraped_data directoy
    and deletes files that are not .csv or .xlsx"""
    path = pathlib.Path.cwd()/"scraped_data"
    #print("This is the path: ", path)

    for folder in path.iterdir():
        if folder.is_dir():
            #counter = 1
            # folder_name = file.stem
            # print("This is the folder name: ", folder_name)
            for file in folder.iterdir():
                if file.is_file():
                    if file.suffix == ".csv":
                       #print("this we keep: ", file.suffix)
                    elif file.suffix == ".xlsx":
                        #print("this we keep: ", file.suffix)
                    else:
                        #print("this we delete: ", file.suffix)
                        file.unlink()
            
                    

delete_files()