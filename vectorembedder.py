import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer, util
import dask.dataframe as dd
from datetime import datetime
from elasticsearch import Elasticsearch, helpers
from pymongo import MongoClient

def gendata(passage_embedding, ADDRESS, captions):
    for vec in range(len(passage_embedding)):
        yield {
            "_op_type": "create",
            "_index": "captions-index",
            "caption-vector": passage_embedding[vec],
            "file-name": ADDRESS[captions[vec]],
            "file-type": "audio"
        }

df = dd.read_csv('DATASET/Captioned/*.csv')
captions = list(df["captioning"])

ADDRESS = dict()  #key:caption, value:file_name
for _,row in df.iterrows():
    ADDRESS[row['captioning']] = row['file_name']

VDB_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
passage_embedding = VDB_model.encode(captions)

client = MongoClient("mongodb://localhost:27017/?directConnection=true")
testdb = client.testdb
captionsData = testdb.captions
for caption in captions:
    captionsData.insert_one({
        "caption": caption,
        "file-name": ADDRESS[caption]
    })
captionsData.create_index("file-name")

# es = Elasticsearch(['https://66d731f461bf42b09d7000cf2ade257b.us-central1.gcp.cloud.es.io'], http_auth=("username", "password"))

# #helpers.bulk(es , gendata(passage_embedding, ADDRESS, captions))
# res = es.knn_search(index="captions-index", knn={
#     "field": "caption-vector",
#     "query_vector": VDB_model.encode("I want a slow and mellow song for sleep"),
#     "k": 5,
#     "num_candidates": 1000
#   }, source=[ "file-name", "file-type" ])

# print(res)
