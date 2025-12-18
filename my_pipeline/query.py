# query_rag_ollama_optimized.py

from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
import numpy as np
from numpy.linalg import norm
from pathlib import Path
import ollama
from my_pipeline.config import *
# --------- Config ---------
BATCH_SIZE = 500  # Number of embeddings to process in memory at a time
# Optional: pre-filter by day
FILTER_DAY = None  # e.g., "day1" or None for all

# --------------------------
# Initialize embeddings
model = SentenceTransformer(MODEL_NAME)

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

def cosine_similarity(a, b):
    return np.dot(a, b) / (norm(a) * norm(b))

def retrieve_relevant_chunks(query, top_k=TOP_K, filter_day=None):
    """Retrieve top-k relevant chunks using batch processing and optional metadata filtering."""
    query_embedding = model.encode(query)

    # Build MongoDB filter
    mongo_filter = {}
    if filter_day:
        mongo_filter['audio_path'] = {'$regex': filter_day}

    # Count total chunks to process
    total_chunks = collection.count_documents(mongo_filter)
    print(f"Total chunks to process: {total_chunks}")

    top_results = []

    # Process in batches
    cursor = collection.find(mongo_filter, {"text": 1, "start": 1, "end": 1, "audio_path": 1, "embedding": 1})
    batch = []
    for doc in cursor:
        batch.append(doc)
        if len(batch) >= BATCH_SIZE:
            top_results.extend(process_batch(query_embedding, batch, top_k))
            batch = []
    if batch:
        top_results.extend(process_batch(query_embedding, batch, top_k))

    # Sort final results and return top_k
    top_results.sort(key=lambda x: x[0], reverse=True)
    return [chunk for sim, chunk in top_results[:top_k]]

def process_batch(query_embedding, batch, top_k):
    """Compute cosine similarity for a batch and return top_k tuples (similarity, chunk)."""
    sims = []
    for chunk in batch:
        chunk_embedding = np.array(chunk['embedding'])
        sim = cosine_similarity(query_embedding, chunk_embedding)
        sims.append((sim, chunk))
    # Keep only top_k in this batch
    sims.sort(key=lambda x: x[0], reverse=True)
    return sims[:top_k]

def generate_answer_ollama(query, top_chunks):
    """Generate answer using Ollama LLaMA model."""
    context_text = "\n".join([chunk['text'] for chunk in top_chunks])
    prompt = f"Use the following context to answer the question:\n\n{context_text}\n\nQuestion: {query}\nAnswer:"

    response = ollama.chat(
        model=LLAMA_MODEL,
        messages=[{"role": "user", "content": prompt}],
        options={"temperature": 0.2, "max_tokens": 300}  # pass these in 'options'
    )

    # response = ollama.chat(
    #     model=LLAMA_MODEL,
    #     messages=[{"role": "user", "content": prompt}],
    #     temperature=0.2,
    #     max_tokens=300
    # )
    return response['message']['content']


