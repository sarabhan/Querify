# RAG-based AI Teaching Assistant (Upgraded Fork)

This project is an upgraded version of [Prince-723/RAG-based-AI-teaching-assistant](https://github.com/Prince-723/RAG-based-AI-teaching-assistant). It implements a **RAG (Retrieval-Augmented Generation) pipeline** using **MongoDB for embeddings storage**, **SentenceTransformers** for embeddings, and **Ollama LLaMA 3.2 1B** model for generating answers. 

---

## 🚀 New Additions in This Fork

This fork introduces several major enhancements over the original project:

1. **Optimized Chunk Retrieval**
   - Batch processing to handle thousands of chunks efficiently.
   - Metadata-based filtering (e.g., by day or video) for more precise context selection.
   - Sorted chunks by start time to maintain logical order.
     
2. **SentenceTransformers for Embeddings**
   - Replaces LangChain/OpenAI embeddings with local SentenceTransformers.
   - Enables fast, cost-free embedding generation for all chunks.
   - Provides better quality semantic embeddings optimized for similarity search.

3. **Improved Answer Quality**
   - Optimized prompt engineering for detailed and precise answers.
   - Adjustable parameters like `TOP_K`, `temperature`, and `max_tokens`.
   - Context-aware, deterministic responses with less vagueness.

4. **Scalability & Flexibility**
   - Designed for multi-day, multi-video datasets.
   - Easy to expand: add more metadata filters, chunk summarization, or larger LLaMA models.

---

## 🌟 Features

- Convert **videos → audio → text chunks**.  
- Store **text chunks with embeddings** in MongoDB.  
- Retrieve **top-k relevant chunks** efficiently with **metadata filtering and batch processing**.  
- Generate **accurate natural language answers** using LLaMA 3.2 1B via Ollama.  
- Optimized pipeline to handle **multi-day / multi-video datasets**.

---
## Setup Instructions

### Step 1: Clone this fork 
```
   $ git clone <fork-url>
   $ cd RAG-based-AI-teaching-assistant
```
### Step 2: Install dependencies
```
pip install -r requirements.txt
```
### Step 3: Install & setup ollama
```
pip install ollama
ollama pull llama-3.2:1b
```
### Step 4: Setup MongoDB & Mongosh (for Windows)
- Setup MongoDB using the attached .msi file: _mongodb-windows-x86_64-8.0.16-signed.msi_
- Setup Mongosh using the attached .msi file: _mongosh-2.5.10-x64.msi_


### Step 5: Run main.py file
---
## 🛠️ Optimization Tips

- TOP_K: Increase number of chunks retrieved for richer context.
- Chunk size: Use larger chunks for better context coverage.
- Metadata filtering: Restrict search by day or video to reduce noise.
- Prompt engineering: Include explicit instructions in prompts for more precise answers.
- Temperature / max_tokens: Adjust in Ollama for deterministic or detailed outputs.


### This repo is open for further collaborations, discussions, and issues!
Feel free to create your own issues or head to the discussions page!
