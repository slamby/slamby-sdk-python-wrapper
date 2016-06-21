# -*- coding: utf-8 -*-
"""
Created on Tue Jun 21 11:02:48 2016

@author: peter.mezei
"""

from slamby_python_sdk_v01 import Slamby
import uuid

# Connect to Server
demo = Slamby("https://europe.slamby.com/demo/","s3cr3t")

# Create dataset by "schema"
demoDatasetName = "demo-{0}".format(uuid.uuid4())
demo.createDataset(demoDatasetName,{"title":str,"description":str,"price":float})

# List dataset(s)
for dataset in demo.getDataset().getDatasetList():
    print(dataset.name)
    
# Upload document for demo dataset
demo.getDataset(demoDatasetName).createDocument({"id":str(uuid.uuid4()),"tags":[],"title":"demo title","description":"demo description"})

# Upload bulk documents for demo dataset
bulk = []
for document in range(1,10):
    bulk.append(
        {
            "id":str(uuid.uuid4()),
            "tags":[],
            "title":"Macbook pro demo title {0}".format(str(uuid.uuid4())),
            "description":"demo description"
        }
    )
demo.getDataset(demoDatasetName).createDocument(bulk)

# Get document by id
demo.getDataset("demo-dataset").getDocumentById(9)

# Get document by filter
demo.getDataset("demo-dataset").getDocumentByFilter("macbook",limit=3)

# Remove dataset
demo.removeDataset(demoDatasetName)