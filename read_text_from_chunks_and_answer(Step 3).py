import os
import json
import requests
from mongodb_connect import DBconnect
from pymongo import MongoClient
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import joblib

all_req_chunk_paths = []

def chunk_embedding(text_list):
    r = requests.post("http://localhost:11434/api/embed",json = {
        "model" : "bge-m3",
        "input" : text_list
    })
    
    embedding = r.json()['embeddings']
    return embedding

def inference(prompt):
    r = requests.post("http://localhost:11434/api/generate",json = {
        # "model" : "deepseek-r1",
        "model" : "llama3.2",
        "prompt" : prompt,
        "stream" : False
    })

    response = r.json()
    return response

#here we are finding the directory which we want to process
def req_chunk_dir():
    for dirpath,dirnames,filenames in os.walk("chunks"):
        all_req_chunk_paths.append(dirpath)

    for i in range(len(all_req_chunk_paths)):
        print(f"{i} : {all_req_chunk_paths[i]}")
    n = int(input("Enter the number of folder you want to process : "))
    
    req_chunk_dir = all_req_chunk_paths[n]
    print(f"Selected directory: {req_chunk_dir}")
    return req_chunk_dir

def get_chunks_from_file(file_path):
    my_dict = []
    for dirpath,dirnames,filenames in os.walk(file_path):
        for file in filenames:
            if(file.endswith("_chunks.json")):
                print(file)
                print("--------------------------------------------------")
                count = 0
                with open(f"{file_path}/{file}", "r") as f:
                    data = json.load(f)
                embeddings = chunk_embedding([chunk['text'] for chunk in data])
                for i,chunk in enumerate(data):
                    chunk['chunk_id'] = count
                    chunk['embedding'] = embeddings[i]
                    count += 1
                    my_dict.append(chunk)
                    #we are connecting to the database and inserting the chunk
                    db = DBconnect("mongodb://localhost:27017/","teaching_assistant_db","chunks_collection")
                    db.insert_document(chunk)

                print("\n")
    print(f"{dirpath} inserted successfully into the database.")
    return my_dict

def create_df():
    #we are using it to create dataframe from the stored chunks in database
    client = MongoClient("mongodb://localhost:27017/")
    db = client["teaching_assistant_db"]
    collection = db["chunks_collection"]

    data = list(collection.find())
    df = pd.DataFrame(data)

    if "_id" in df.columns:
        df = df.drop(columns = ["_id"] , axis = 1)
    
    return df


print("Select the process: \n 1. choose '1' to read chunks from file and store in database. \n 2. choose '2' to make dataframe from the stored chunks in database.\n 3. choose '3' to ask question and get relevant chunks as answer.")

value = int(input("Enter your Choice:"))

match value:
    case 1:
        #variable that stores the path of required chunk directory
        req_chunk_dir_path = req_chunk_dir()
        #making the database entries from the files that has chunks stored in them
        get_chunks_from_file(req_chunk_dir_path)
    
    case 2:
        #here we are making the dataframe using the stored chunks in database
        result_df = create_df()

        #we are here saving the dataframe so that don't have to create it again and again
        joblib.dump(result_df,"embedding_df.joblib")
        print("Dataframe created and saved successfully.")

    case 3:
        #taking input query from user
        incoming_query = input("Ask a Question:")
        question_embedding = chunk_embedding([incoming_query])[0]
        print("Question embedding created successfully.")

        #here we are loading the dataframe from the .joblib file
        print("Dataframe loading ...")
        result_df = joblib.load("embedding_df.joblib")
        print(result_df.shape)
        print("Dataframe loaded successfully.")

        #find cosine similaritie of question embedding with embeddings in dataframe
        similarities = cosine_similarity(np.vstack(result_df['embedding']),[question_embedding]).flatten()

        #here we are selecting how many results we want to see
        top_results = 5;
        
        #here we are using .argsort to get the indices of the results and then reversing(because largest values index is at last) and then taking the top results
        max_indx = similarities.argsort()[::-1][0:top_results] 

        #we are printing the top results
        new_df = result_df.loc[max_indx]

        #here is the prompt what we are going to give to the LLM
        prompt = f'''
        Here are video chunks containing video's text of the chunk , video name audios/JavaScript 19-32/2/2.mp4 here the 2.mp4 is the name of the video and 2 before 2.mp4 is the number of the chapter also Javascript 19-32 is the chapter title where 19-32 tells that this javascript charpter continues from 19th to 32nd chapter in the course , the chunk also have start time in seconds and end time in seconds of the partcular chunk (if user asks unrelated questions tell that question is unrelated to your expertiese):

        {new_df[["text","video","start","end"]].to_json(orient = 'records') }
        -------------------------------------------
        Question : {incoming_query}

        The user asked this question related to the video chunks, you have to answer where and how much content is taught where(in which video and at hat timestamp) and guide the user to that particular video
        '''
        with open("prompt.txt","w") as f:
            f.write(prompt) 

        #here we are getting the response of inference from the LLM 
        response = inference(prompt)['response']
        print(response)

        #here we are saving the response to a text file
        with open("response.txt","w") as f:
            f.write(response)   
        # for index,row in new_df.iterrows():
        #     print(f"Index:{index} Text:{row['text']} chunks:{row['video']} Start:{row['start']} end:{row['end']}")