import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import joblib
import requests

def creat_embedding(text_list):
    r=requests.post("http://localhost:11434/api/embed",json={
        "model":"bge-m3",
        "input":text_list
        })
    embeddings=r.json()["embeddings"]
    return embeddings

def inference(prompt):
    r=requests.post("http://localhost:11434/api/generate",json={
        "model":"llama3.2",
        "prompt":prompt,
        "stream":False
        })
    response=r.json()
    return response

df=joblib.load("embeddings.joblib")
incoming_quary=input("Ask a question ?")
question_embedding=creat_embedding([incoming_quary])[0]
# print(question_embedding)

#find the similarity of question embedding with other embeddings
# print("?????????")
# print(np.vstack(df["embedding"].values))
# print(np.vstack(df["embedding"]).shape)

similarities=cosine_similarity(np.vstack(df["embedding"]),[question_embedding]).flatten()
# print(similarities)
top_result=5
max_index=similarities.argsort()[::-1][0:top_result]
new_df=df.loc[max_index]
# print(new_df[["title","number","text"]])

prompt=f'''I am teaching web development in my the sigma web development course. Here are video subtitle chunks containing video title, video number, start time in second, endtime in second, the text at that time:
{new_df[["title","number","start","end","text"]].to_json(orient="records")}
-------------------------------------------
"{incoming_quary}"
User asked this question related to the video chunks, you have to answer in human way (don't mention the above format, it just for you) where and how much content is taught in which video ( in which video and at what timstamp) and guide the user to go to that particular video. If user ask unrelated question, tell him that you can only answer questions related to the course
'''

# for index,item in new_df.iterrows():
#     print(index,item["title"],item["number"],item["text"],item["start"],item["end"])  

with open("prompt.txt","w") as f:
    f.write(prompt)

response=inference(prompt)["response"]
print(response)

with open("response.txt","w") as f:
    f.write(response)
