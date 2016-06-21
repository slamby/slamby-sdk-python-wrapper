# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import slamby_sdk
# from slamby_sdk.rest import ApiException

class Dataset:
    client = object
    datasetApi = object
    documentApi = object
    
    def __init__(self,client=object,dataset=""):
        self.client=client
        self.client.set_default_header("X-DataSet", dataset)
        self.datasetApi = slamby_sdk.DataSetApi(self.client)
        self.documentApi = slamby_sdk.DocumentApi(self.client)

    def getDatasetList(self):
        return self.datasetApi.get_data_sets()
        
    def getDocumentById(self,id=""):
        return self.documentApi.get_document(id=id) if id else False
        
    def getDocumentByFilter(self,query="",tagIds="",offset=0,limit=100):
        filter = {
            "Filter" : {
              "TagIds":tagIds,
              "Query" : query
            },
            "Pagination" : {
                "Offset" : offset,
                "Limit": limit
            }
        }
        return self.documentApi.get_filtered_documents(filter_settings=filter)
        
    def createDocument(self,document={}):
        if type(document) is list:
            tmpDocs = {"documents":document}
            return self.documentApi.bulk_documents(settings=tmpDocs)
        else:
            return self.documentApi.create_document(document=document)

class Slamby:
    client = object
    def __init__(self,server="",secret=""):
        self.client = slamby_sdk.ApiClient(server)
        self.client.set_default_header("Authorization", "Slamby {0}".format(secret))
        
    def getDataset(self,dataset=""):
        self.client.set_default_header("X-DataSet", dataset)
        return Dataset(self.client,dataset)
        
    def createDataset(self,name="",variables=[],id="",ngramCount=3,tagField="",interPretedFields=[]):
        autoFields = ["id","tags"]
        sampleDocument = {}
        if type(variables) is list:
            for field in variables:
                sampleDocument[field] = ""
        elif type(variables) is dict:
            for field in variables.keys():
                value = variables[field]
                if value is str:
                    sampleDocument[field] = ""
                elif value is int:
                    sampleDocument[field] = 9
                elif value is float:
                    sampleDocument[field] = 9.9
                elif value is list:
                    sampleDocument[field] = ["a"]
                elif value is dict:
                    sampleDocument[field] = {"a":"b"}
                else:
                    sampleDocument[field] = ""
                    
        if not id and "id" not in sampleDocument.keys():
            id="id"
            sampleDocument["id"] = ""

        if not id and "id" in sampleDocument.keys():
            id="id"            

        if not tagField and "tags" not in sampleDocument.keys():
            tagField="tags"
            sampleDocument["tags"] = ["a"]

        if not tagField and "tags" in sampleDocument.keys():
            tagField="tags"
        
        if not interPretedFields:
            interPretedFields = list()
            for field in sampleDocument.keys():
                if (field not in autoFields) and (type(sampleDocument[field]) is str):
                    interPretedFields.append(field)

        obj = {
            "IdField": id,
            "InterpretedFields": interPretedFields,
            "Name": name,
            "NGramCount": ngramCount,
            "TagField": tagField,
            "SampleDocument": sampleDocument
        }
        return slamby_sdk.DataSetApi(self.client).create_data_set(data_set=obj)
        
    def removeDataset(self,name=""):
        return slamby_sdk.DataSetApi(self.client).delete_data_set(name=name)