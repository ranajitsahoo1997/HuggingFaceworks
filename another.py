# pip install langchain langchain-community PyPDF2 faiss-cpu

from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain

# Step 1: Read PDF
pdfreader = PdfReader("Core-java-material.pdf")
raw_text = ""
count = 0
for page in pdfreader.pages:
    if count<20:
        content = page.extract_text()
        if content:
            raw_text += content
    else:
        break
    count+=1
print("----------------------------------1")
# Step 2: Split into chunks
text_splitter = CharacterTextSplitter(
    separator="\n",
    chunk_size=800,
    chunk_overlap=200,
    length_function=len,
)
texts = text_splitter.split_text(raw_text)
print("----------------------------------2")

# Step 3: Embeddings
embeddings = OllamaEmbeddings(model="llama3.2")  # make sure llama3.2 is pulled
print("----------------------------------3")

# Step 4: Vector DB
vectorstore = FAISS.from_texts(texts, embeddings)
print("----------------------------------4")

# Step 5: LLM
llm = Ollama(model="llama3.2")
print("----------------------------------5")

# Step 6: Prompt and chain
prompt = PromptTemplate.from_template(
    "Use the following context to answer the question:\n\n{context}\n\nQuestion: {question}"
)
qa_chain = create_stuff_documents_chain(llm, prompt)
print("----------------------------------6")

# Step 7: Ask a Java-related question
query = "what is the code of Sum of even?"
relevant_docs = vectorstore.similarity_search(query)
response = qa_chain.invoke({
    "context": relevant_docs,
    "question": query
})

# Step 8: Output
print("Answer:", response)
