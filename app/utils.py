

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

def toJson(caseString, info):
    output = []
    casesList = caseString.split(",")
    for item in casesList:
        chain = item.split('/')
        currentNode = output
        for index,node in enumerate(chain):
            wantedNode = node
            lastNode = currentNode
            i = 0
            for x in range(i,len(currentNode)):
                i = x + 1
                if currentNode[x]["title"] == wantedNode:
                    currentNode = currentNode[x]["children"]
                    break
            if lastNode == currentNode:
                if '.' in wantedNode:
                    currentNode.insert(i,{"title":wantedNode,"platform":"chrome","status":info.get("status"),"start_time":info.get("start_time"),"end_time":info.get("end_time"),"children":[]}) 
                else:
                    currentNode.insert(i,{"title":wantedNode,"folder":True,"expanded":True,"children":[]}) 
                newNode = currentNode[i]
                currentNode = newNode["children"]
    return output