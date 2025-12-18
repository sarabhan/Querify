# ingest_chunks.py

import json
from pathlib import Path
import numpy as np
from sentence_transformers import SentenceTransformer
from pymongo import MongoClient
from my_pipeline.config import *

def load_chunks_from_dir(root_dir: Path):
    """Recursively load all JSON chunk files under the directory."""
    chunks = []
    for json_file in root_dir.rglob("*.json"):  # recursive search
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            chunks.extend(data)
    return chunks

def send_chunk_embedding_todb():
    # Load all chunks
    chunks = load_chunks_from_dir(CHUNKS_ROOT)
    print(f"Loaded {len(chunks)} chunks from {CHUNKS_ROOT}")

    # Initialize sentence transformer
    model = SentenceTransformer(MODEL_NAME)

    # Connect to MongoDB
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]

    # Optional: clear existing collection
    collection.delete_many({})

    # Process chunks in batches
    for i in range(0, len(chunks), BATCH_SIZE):
        batch = chunks[i:i+BATCH_SIZE]
        texts = [chunk["text"] for chunk in batch]
        embeddings = model.encode(texts, convert_to_numpy=True, show_progress_bar=True)

        # Prepare documents for bulk insert
        docs_to_insert = []
        for chunk, emb in zip(batch, embeddings):
            doc = {
                "text": chunk["text"],
                "start": chunk["start"],
                "end": chunk["end"],
                "audio_path": chunk["audio"],
                "embedding": emb.tolist()  # convert numpy array to list for MongoDB
            }
            docs_to_insert.append(doc)

        # Bulk insert
        if docs_to_insert:
            collection.insert_many(docs_to_insert)
            print(f"Inserted batch {i//BATCH_SIZE + 1} with {len(docs_to_insert)} chunks")

    print(f"Successfully ingested all {len(chunks)} chunks into MongoDB collection '{COLLECTION_NAME}'.")
