import requests
import os
import json
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import joblib

def creat_embedding(text_list):
    r=requests.post("http://localhost:11434/api/embed",json={
        "model":"bge-m3",
        "input":text_list
        })
    embeddings=r.json()["embeddings"]
    return embeddings

# a=creat_embedding(["cat set on the mat","where are you"])
# print(a)
jsons=os.listdir("newjsons")
my_dicts=[]
chunk_id=0
for json_file in jsons:
    with open (f"newjsons/{json_file}") as f:
        content=json.load(f)
    print(f"creating embedding for {json_file}")
    embeddingss=creat_embedding([c['text'] for c in content["chunks"]])
    for i,chunk in enumerate(content['chunks']):
        chunk["chunk_id"]=chunk_id
        chunk["embedding"]=embeddingss[i]
        chunk_id+=1
        my_dicts.append(chunk)
    
    
df=pd.DataFrame.from_records(my_dicts)
#save this dataframe
joblib.dump(df,"embeddings.joblib")

