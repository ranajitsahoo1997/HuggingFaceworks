# pdf_utils.py
from langchain.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_ollama.llms import OllamaLLM

def load_and_split_pdf(pdf_path):
    loader = PyMuPDFLoader(pdf_path)
    documents = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = splitter.split_documents(documents)[2:5]
    return docs

def store_in_faiss(docs):
    embeddings = OllamaEmbeddings(model="mxbai-embed-large")
    vectorstore = FAISS.from_documents(docs, embeddings)
    return vectorstore

def extract_topics(docs):
    combined_text = "\n".join([doc.page_content for doc in docs])
    model = OllamaLLM(model="llama3")
    prompt = PromptTemplate.from_template("""
    Analyze the following document and list all the main topics covered. Only provide the topic names as a list.

    Document:
    {content}
    """)
    chain = LLMChain(llm=model, prompt=prompt)
    response = chain.invoke({"content": combined_text})
    return response

def generate_mcqs(vectorstore, topic):
    retriever = vectorstore.as_retriever()
    docs = retriever.invoke(topic)
    context = "\n".join([doc.page_content for doc in docs])
    model = OllamaLLM(model="llama3")
    prompt = PromptTemplate.from_template("""
    You are a quiz expert. Based on the following topic content, generate 3 multiple choice questions with 4 options each and indicate the correct answer.

    Topic: {topic}

    Content:
    {context}
    """)
    chain = LLMChain(llm=model, prompt=prompt)
    return chain.invoke({"topic": topic, "context": context})
