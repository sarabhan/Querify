from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
VIDEO_ROOT = PROJECT_ROOT / "video"
AUDIO_ROOT = PROJECT_ROOT / "audio"
CHUNKS_ROOT = PROJECT_ROOT / "chunks"
MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "rag_db"
COLLECTION_NAME = "audio_chunks"
MODEL_NAME = "all-MiniLM-L6-v2"
BATCH_SIZE = 64
TOP_K = 20
LLAMA_MODEL = "llama3.2:1b"