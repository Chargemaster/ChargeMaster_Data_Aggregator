from os import renames, unlink
import pathlib

#This program works to rename files in scraper folder with hospital name and a number ID for each file.

def rename_files():
    path = pathlib.Path.cwd()/ 'scraped_data'
    print("This is the path: ", path)

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
            
                    

rename_files()

# directory = file.parent
#                 old_name = file.stem