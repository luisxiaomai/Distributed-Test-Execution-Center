import os
from . import cases_folder

def path_to_dict(path):
    d = {'title':os.path.basename(path)}
    if os.path.isdir(path):
        d['folder'] = True
        d['expanded'] = True
        d['children'] = [path_to_dict(os.path.join(path,x)) for x in os.listdir(path) if x != ".DS_Store"]
    d["key"]=os.path.relpath(path,cases_folder)
    return d
