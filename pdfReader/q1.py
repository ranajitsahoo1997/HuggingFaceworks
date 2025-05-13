from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OllamaEmbeddings 
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.documents import Document
# from stringToDictionanry import rawTextToDictionary
import json
import re
import os


pdfreader = PdfReader("Core-java-material.pdf")
print("pdf reader object is created")


textSplitter = CharacterTextSplitter(
    separator="\n",
    chunk_size=800,
    chunk_overlap=200,
    length_function=len,
)
print("text splitter object created")


ollamaembedding = OllamaEmbeddings(model="llama3.2")
print("embedding object created")

llm = Ollama(model="llama3.2", temperature=0.7)
print("LLM object created")

# Use a path to store FAISS data
faiss_index_path = "faiss_index_llama3"

if not os.path.exists(faiss_index_path):
    
    all_documents = []
    pno = 0
    for page in pdfreader.pages:
        page_content = page.extract_text()
        if page_content and pno > 2 and pno < 5:
            split_texts = textSplitter.split_text(page_content)
            documents = [Document(page_content=text) for text in split_texts]
            all_documents.extend(documents)
        pno += 1
    print("Documents created")
    vectorstore = FAISS.from_documents(all_documents,ollamaembedding)
    print("vectorstore created")
    vectorstore.save_local(faiss_index_path)
    print("FAISS index created and saved Locally")
else:
    print("Faiss index already exists. Loading from disk...")
    
vectorstore = FAISS.load_local(faiss_index_path, ollamaembedding,allow_dangerous_deserialization=True)
print("FAISS index loaded from disk")

topicwise_prompt = PromptTemplate.from_template(
            "Using the following Java content, generate unique and topic-wise mcq Questions with its answer. "
            "Label them clearly with the topic and make sure they are diverse and meaningful.\n\n{context}"
        )
question_gen_chain = create_stuff_documents_chain(llm, topicwise_prompt)
retrieved_docs = vectorstore.similarity_search("Generate MCQ from the PDF", k=5)

question_gen_response = question_gen_chain.invoke({
    "context": retrieved_docs[:6]  # Use multiple chunks for a broader context
})
print("Question generation response:")
print(question_gen_response)
        
            