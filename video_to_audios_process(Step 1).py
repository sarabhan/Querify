#converting videos (mp4) to audios (mp3)

import os
import subprocess

#getting file directories
video_files = os.listdir("videos/JavaScript 19-32/")
audio_files = os.listdir("audios/JavaScript 19-32/")

for dirpath, dirnames,filenames in os.walk("videos/JavaScript 19-32/"):
    #calculating path of each video file
    rel_path = os.path.relpath(dirpath, "videos/JavaScript 19-32/")
    #calculating path of each audio file
    audio_dir = os.path.join("audios/JavaScript 19-32/", rel_path)
    #making directories to save audio files into
    os.makedirs(audio_dir, exist_ok = True)

    #traversing through each video file
    for file in filenames:
        #checking if it has .mp4 extension
        if file.lower().endswith('.mp4'):
            #getting full path of video file
            video_file = os.path.join(dirpath,file)
            #getting full path of audio file
            audio_file = os.path.join(audio_dir,os.path.splitext(file)[0] + '.mp3')
            #using ffmpeg command to convert video to audio
            cmd = ['ffmpeg','-i',video_file,'-q:a','2','-vn',audio_file]
            #running the command
            subprocess.run(cmd)
            print(f"Converted {video_file} to {audio_file}")