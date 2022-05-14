import os
import glob
from posixpath import split

def get_all_file_paths(path):
    data = {}
    subjects = glob.glob(path+"*")
    for sub_dir in subjects:
        sub_id = os.path.split(sub_dir)[1]
        data[sub_id] = {}
        data[sub_id]['L'] = glob.glob(os.path.join(sub_dir, "L") + "\\*")
        data[sub_id]['R'] = glob.glob(os.path.join(sub_dir, "R") + "\\*")
    
    return data

def get_only_file_by_dataset(data):
    files = []
    subjects = list(data.keys())
    
    for sub in subjects:
        files = files + data[sub]["L"]
        files = files + data[sub]["R"]
    
    return files