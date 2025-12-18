from my_pipeline.video_to_audio import * 
from my_pipeline.audio_to_text import *
from my_pipeline.ingest_chunks import *
from my_pipeline.query import *


if __name__ == "__main__":
    print("converting video to audio...")
    video2audio()
    print("converting audio to text...")
    audio2text()
    print("ingesting chunks into database...")
    send_chunk_embedding_todb()

    FILTER_DAY = input("Enter which day you want to know about (or press Enter to skip): ") or None
    query = input("Enter your question: ")
    top_chunks = retrieve_relevant_chunks(query, filter_day=FILTER_DAY)

    answer = generate_answer_ollama(query, top_chunks)
    print("\nGenerated answer:\n")
    print(answer)