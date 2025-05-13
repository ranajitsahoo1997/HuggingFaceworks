
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
import os
from PyPDF2 import PdfReader


# Load data
pdf = PdfReader("/home/ranajit/Desktop/RedIntegro/HuggingFaceWorks/Core-java-material.pdf")

# Set up embedding model
embeddings = OllamaEmbeddings(model="mxbai-embed-large")

# DB location
db_location = "faiss_langchain_db"
index_file = os.path.join(db_location, "faiss.index")
store_file = os.path.join(db_location, "store.pkl")
add_documents = not os.path.exists(index_file)

if add_documents:
    documents = []
    for i, page in enumerate(pdf.pages):
        doc = Document(
            page_content=page.extract_text(),
            metadata={"page": i}
        )
        documents.append(doc)

    # Create and store FAISS vector store
    vector_store = FAISS.from_documents(documents, embeddings)
    os.makedirs(db_location, exist_ok=True)
    vector_store.save_local(db_location)
else:
    vector_store = FAISS.load_local(db_location, embeddings, allow_dangerous_deserialization=True)
# Create retriever
retriever = vector_store.as_retriever(search_kwargs={"k": 5})
# Save the retriever to a file  

