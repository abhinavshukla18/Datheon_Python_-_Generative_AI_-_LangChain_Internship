import os
import shutil
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

from ingest import load_and_split

load_dotenv()

DB_DIR = "chroma_db"


def get_embeddings():
    return GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=os.getenv("GEMINI_API_KEY"),
    )


def build_index(pdf_path):
    if os.path.exists(DB_DIR):
        shutil.rmtree(DB_DIR)
    chunks = load_and_split(pdf_path)
    db = Chroma.from_documents(chunks, get_embeddings(), persist_directory=DB_DIR)
    return db, len(chunks)


if __name__ == "__main__":
    db, n = build_index("data/sample.pdf")
    print("Stored", n, "chunks")
    results = db.similarity_search("What is type casting?", k=2)
    for r in results:
        print("page", r.metadata["page"] + 1, "|", r.page_content[:150].replace("\n", " "))