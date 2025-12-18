from pathlib import Path
import json
import whisper
from my_pipeline.config import *

# ---- WHISPER CONFIG ----
MODEL_NAME = "tiny"
LANGUAGE = "hi"
TASK = "translate"

def audio2text():
    model = whisper.load_model(MODEL_NAME)

    # Traverse all audio files recursively
    for audio_file in AUDIO_ROOT.rglob("*.mp3"):
        # Preserve folder structure (day1/day2/...)
        relative_path = audio_file.relative_to(AUDIO_ROOT)

        # Build output path
        output_file = (
            CHUNKS_ROOT / relative_path.parent / f"{audio_file.stem}_chunks.json"
        )

        # Create output directory if needed
        output_file.parent.mkdir(parents=True, exist_ok=True)

        # Skip if already processed
        if output_file.exists():
            print(f"Skipping (already done): {audio_file}")
            continue

        print(f"Processing: {audio_file}")

        # Transcribe audio
        result = model.transcribe(
            audio=str(audio_file),
            language=LANGUAGE,
            task=TASK,
            fp16=False
        )

        # Convert Whisper segments to chunks
        chunks = [
            {
                "start": seg["start"],
                "end": seg["end"],
                "text": seg["text"],
                "audio": str(audio_file)
            }
            for seg in result["segments"]
        ]

        # Save chunks
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(chunks, f, ensure_ascii=False, indent=2)

        print(f"Saved → {output_file}")
