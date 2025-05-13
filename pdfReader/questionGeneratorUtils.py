from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
# from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OllamaEmbeddings 
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.documents import Document
# from stringToDictionanry import rawTextToDictionary
import json
import re
import os


def pdf_reader(file_path):

    pdfreader = PdfReader(file_path)
    textSplitter = CharacterTextSplitter(
    separator="\n",
    chunk_size=800,
    chunk_overlap=200,
    length_function=len,
    )
    all_documents = []
    pno = 0
    for page in pdfreader.pages:
        page_content = page.extract_text()
        if page_content and pno > 2 and pno < 5:
            split_texts = textSplitter.split_text(page_content)
            documents = [Document(page_content=text) for text in split_texts]
            all_documents.extend(documents)
        pno += 1
    ollamaembedding = OllamaEmbeddings(model="llama3.2")
    print("embedding object created")

    llm = Ollama(model="llama3.2", temperature=0.7)
    print("LLM object created")
    if os.path.exists("documents.json"):
        print("wait sometime for documents to be created")
        with open("documents.json", "w") as f:
            json.dump([doc.page_content for doc in all_documents], f)
        print("Documents are created and saved in local")
    else:
        print("File already exists. Loading from disk...")
    with open("documents.json", "r") as f:
        contents = json.load(f)
    documents = [Document(page_content=txt) for txt in contents]
    return documents, llm

def rawTextToDict(data):
    splitted = data.split("**")
    # print(splitted)
    c=0
    data_gen = {}
    map_data = None
    for spli in splitted:
        text_split = spli.split("Topic")
        if c>0:
            if c%2==1:
               topic = text_split[1].lstrip(": ").strip() 
               
               data_gen[topic]=[]
            else:
                text = re.sub(r'\n(?=\nAnswer:)', '', text_split[0])
                questions = text.split("\n\n")
                for i,qq in enumerate(questions):
                    if i!=0:
                        d = qq.split("\n")
                        data_gen[topic].append({
                            "question": d[0],
                            "options": d[1:5],
                            "answer": d[-1]
                        })
                
        c+=1
    
    return data_gen
                    
    

def generate_questions(documents,llm):
    topicwise_prompt = PromptTemplate.from_template(
            "Using the following Java content, generate unique and topic-wise mcq Questions with its answer. "
            "Label them clearly with the topic and make sure they are diverse and meaningful.\n\n{context}"
        )
    print("Prompt template created")
    question_gen_chain = create_stuff_documents_chain(llm, topicwise_prompt)
    print("Question generation llm chain created")

    question_gen_response = question_gen_chain.invoke({
        "context": documents[:10]  # Use multiple chunks for a broader context
    })
    mappedData = rawTextToDict(question_gen_response)
    return mappedData

