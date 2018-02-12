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


def toJson(caseString):
    iter = caseString.split("/", 1)
    d = {'title':iter[0]}
    if len(iter)>1 :
        d['folder'] =True
        d['expanded'] = True
        d['children'] = [toJson(iter[1])]

    return d