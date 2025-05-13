# Install required packages if not already installed
# pip install langchain langchain-community PyPDF2 faiss-cpu

from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains.question_answering import load_qa_chain
from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings  # Optional if using Ollama's embeddings

# Step 1: Load PDF
pdfreader = PdfReader("Core-java-material.pdf")
print(pdfreader)
print("----------------------------------")
raw_text = ''
for page in pdfreader.pages:
    content = page.extract_text()
    if content:
        raw_text += content
    # break

print(raw_text)
print("----------------------------------1")
# Step 2: Split text into chunks
text_splitter = CharacterTextSplitter(
    separator="\n",
    chunk_size=800,
    chunk_overlap=200,
    length_function=len,
)
texts = text_splitter.split_text(raw_text)

print(texts)
print("----------------------------------2")

# Step 3: Create embeddings (Option 1: Use Ollama's embeddings)
embeddings = OllamaEmbeddings(model="llama3.2")  # Adjust model name as needed
print(embeddings)
print("----------------------------------3")

# Optional: Use HuggingFaceEmbeddings instead
# embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Step 4: Create FAISS vector store
vectorstore = FAISS.from_texts(texts, embeddings)
print(vectorstore)
print("----------------------------------4")

# Step 5: Initialize LLaMA 3 via Ollama
llm = Ollama(model="llama3.2")  # or "llama3:8b" or "llama3.2" if that's what you named it in `ollama run`

# Step 6: Create QA chain
qa_chain = load_qa_chain(llm, chain_type="stuff")

# Step 7: Ask a question
query = "Vision for Amrit Kaal"
relevant_docs = vectorstore.similarity_search(query)

# Step 8: Run chain
response = qa_chain.run(input_documents=relevant_docs, question=query)

# Print the result
print("Answer:", response)
