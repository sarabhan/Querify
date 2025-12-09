import whisper
import json
import os

all_req_path_list = []

#here we are calculating the directory path which we want to do processing on.
def dirctory():
    for dirpath,dirnames,filenames in os.walk("audios/JavaScript 19-32/"):
        all_req_path_list.append(dirpath)
        
    print("Select the directory number from the following list which you want to process:")
    for i in range(len(all_req_path_list)):
        print(f"{i} : {all_req_path_list[i]}")

    n = int(input("Enter the number of folder you want to process : "))
    req_dir = all_req_path_list[n]

    return req_dir
    
req_directory = dirctory()
print(f"You have selected the directory for processing : {req_directory}")
def createfile_done_chunks(req_dir):
    req_chunks_dir = req_dir.replace("audios/JavaScript 19-32/","chunks/")
    req_chunks_done = []
    for dirpath,dirnames,filenames in os.walk(req_chunks_dir):
        for file in filenames:
            if file.endswith("_chunks.json"):
                req_chunks_done.append(file.split("_chunks.json")[0])
    formate = {}    
    for i in range(len(req_chunks_done)):
        formate[req_chunks_done[i]] = "done"
    
    with open(os.path.join(req_chunks_dir ,"done.json" ), 'w') as f:
        json.dump(formate,f)
    return os.path.join(req_chunks_dir,"done.json")

def adding_content_to_done(req_done_dir,filename):
    data = {}
    with open(req_done_dir,'r') as f:
        data = json.load(f)
        data[filename] = "done"
    with open(req_done_dir,'w') as f:
        json.dump(data,f)
    with open(req_done_dir,'r') as f:
        data = json.load(f)

#here we are loading the whisper model
model = whisper.load_model("large-v2")

#here we will me chunking the audio files and storing the chunks in a relevant directory
def chunking():
    #making a directory to store chunks
    os.makedirs("chunks",exist_ok = True)
    dir_name = req_directory.split('/')[-1]
    chunks_subdir = os.path.join("chunks",dir_name)
    os.makedirs(chunks_subdir , exist_ok = True)

    #checking which file are already done
    req_done_dir = createfile_done_chunks(req_directory)

    data = {}
    with open(req_done_dir,'r') as f:
        data = json.load(f)
    
    req_done_data = list(data.keys())

    #doing the actual process of chunking
    for file in os.listdir(req_directory):
        file_name = file.split(".")[0]
        if(file_name in req_done_data):
            continue
        else:
            print(f"Processing file : {file}")
            chunks = []
            result = model.transcribe(audio = os.path.join(req_directory,file) , language = "hi" , task = "translate" , word_timestamps = False  , fp16 = False)
            for segment in result["segments"]:
                chunks.append({
                    "start":segment["start"],
                    "end":segment["end"],
                    "text":segment["text"],
                    "video":f"{req_directory}/{file}",
                })
            with open(os.path.join(chunks_subdir , os.path.splitext(file)[0] + "_chunks.json") , 'w' ) as f:
                json.dump(chunks,f)
            adding_content_to_done(req_done_dir,file_name)
chunking()













# result = model.transcribe(audio = "K:/anaconda coding/Rag Based Project/audios/JavaScript 19-32/3/sampleoutput.mp3" ,language = "hi", task = "translate",word_timestamps=False,fp16 = False)

#now we will using the followng command in the terminal to get the first 10 sec of the selected file which i can use for testing purpose of chunking.

# ffmpeg -ss 0 -t 10 -i input.mp3 output.mp3 (this is the command)
#remember to run the command in the directory where is the input file is located because ffmpeg does not have permission to open the foler.



# for segment in result["segments"]:
#     chunks.append({
#         "start":segment["start"],
#         "end":segment["end"],
#         "text":segment["text"]
#         "video": 
#     })
# print(chunks)
# with open("output.json" , 'w') as f:
#     json.dump(chunks,f)