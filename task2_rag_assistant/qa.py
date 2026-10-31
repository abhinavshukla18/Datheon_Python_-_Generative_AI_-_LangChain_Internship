import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_chroma import Chroma

from build_index import get_embeddings, DB_DIR

load_dotenv()

PROMPT = """Answer the question using ONLY the context below.
If the answer is not in the context, say: I couldn't find that in the document.

Context:
{context}

Question: {question}
Answer:"""


def get_llm():
    return ChatGoogleGenerativeAI(
        model="gemini-flash-lite-latest",
        google_api_key=os.getenv("GEMINI_API_KEY"),
        temperature=0,
        timeout=60,
    )


def message_text(msg):
    if isinstance(msg.content, str):
        return msg.content
    return "".join(p.get("text", "") for p in msg.content if isinstance(p, dict))


def ask(question, db, llm):
    docs = db.as_retriever(search_kwargs={"k": 4}).invoke(question)
    context = "\n\n".join(
        f"[Page {d.metadata['page'] + 1}] {d.page_content}" for d in docs
    )
    answer = message_text(llm.invoke(PROMPT.format(context=context, question=question)))
    pages = sorted({d.metadata["page"] + 1 for d in docs})
    return answer, pages


if __name__ == "__main__":
    db = Chroma(persist_directory=DB_DIR, embedding_function=get_embeddings())
    llm = get_llm()
    print("Ask questions about the PDF. Type 'exit' to quit.")
    while True:
        q = input("\nYou: ").strip()
        if q.lower() == "exit":
            break
        if not q:
            continue
        answer, pages = ask(q, db, llm)
        print("\nAnswer:", answer)
        print("Sources: pages", ", ".join(str(p) for p in pages))