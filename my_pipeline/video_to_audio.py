from pathlib import Path
import subprocess
from my_pipeline.config import *

def video2audio():
    for video_path in VIDEO_ROOT.rglob("*.mp4"):
        relative_path = video_path.relative_to(VIDEO_ROOT)
        audio_path = AUDIO_ROOT / relative_path.with_suffix(".mp3")

        audio_path.parent.mkdir(parents=True, exist_ok=True)

        cmd = [
            "ffmpeg",
            "-i", str(video_path),
            "-q:a", "2",
            "-vn",
            str(audio_path)
        ]

        subprocess.run(cmd, check=True)
        print(f"Converted {video_path} → {audio_path}")
