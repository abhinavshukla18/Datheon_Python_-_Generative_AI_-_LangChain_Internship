# Task 2: Document Q&A Assistant with RAG & Vector Embeddings

A Retrieval-Augmented Generation (RAG) pipeline that answers questions strictly from a custom PDF and cites the source pages.

## How it works
1. Load the PDF page by page (PyPDFLoader)
2. Split text into overlapping chunks (RecursiveCharacterTextSplitter)
3. Generate embeddings with Gemini and store them in ChromaDB
4. Retrieve the most relevant chunks for a question
5. Gemini answers using only the retrieved context
6. Page numbers of the source chunks are shown with every answer

## Setup
Python 3.12 is recommended (ChromaDB has issues on Python 3.14).
```
pip install -r requirements.txt
```
Copy `.env.example` to `.env` and add your Gemini API key.

## Usage
1. Put any text-based PDF in `data/` and name it `sample.pdf`
2. Build the vector index:
```
python build_index.py
```
3. Ask questions:
```
python qa.py
```

## Project structure
- `ingest.py` - PDF loading and chunking
- `build_index.py` - embeddings and ChromaDB index
- `qa.py` - retrieval, answer generation and page citations
- `data/` - place your PDF here

## Tech
Python, LangChain, ChromaDB, Gemini API (embeddings and LLM), pypdf