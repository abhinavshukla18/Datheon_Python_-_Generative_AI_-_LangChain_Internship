from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


def load_and_split(pdf_path):
    loader = PyPDFLoader(pdf_path)
    pages = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    return splitter.split_documents(pages)


if __name__ == "__main__":
    chunks = load_and_split("data/sample.pdf")
    print("Total chunks:", len(chunks))
    print(chunks[0].metadata)
    print(chunks[0].page_content[:300])