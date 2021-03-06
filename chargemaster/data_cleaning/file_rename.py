"""
This script is used to rename .csv and .xlsx data files that remain after all other file types
have been deleted, during the data cleaning process. """
from os import renames, unlink
import pathlib
import os

def rename_files():
    """
    The function iterates through each folder, and renames files with the same 
    name as the folder (hospital name) and a number, increasing by one for each file
    in the folder.
    """
    path = pathlib.Path(__file__).parents[2]/"data"/"scraped_data"
    isdir = os.path.isdir(path)
    dirname1 = os.path.basename(path)
    if isdir != True:
        raise ValueError ("Not a valid directory")
    if dirname1 != "scraped_data":
        raise ValueError ("Wrong Directory Specified")

    for folder in path.iterdir():
        if folder.is_dir():
            counter = 1
            # folder_name = file.stem
            # print("This is the folder name: ", folder_name)
            for file in folder.iterdir():
                if file.is_file():
                    if file.suffix == ".xlsx" or file.suffix == ".csv":
                        new_file = folder.stem + "_" + str(counter) + file.suffix
                        #print("this is the original file: ", file)
                        #print("this is the new file name: ", new_file)
                        file.rename(path / folder.name / new_file)
                        # print("this is the new file name: ", file)
                        counter += 1
            
                    

#rename_files()

