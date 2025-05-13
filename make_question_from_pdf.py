from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.documents import Document
from stringToDictionanry import rawTextToDictionary
import json
import re


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
                    
    
    
           
        
            
        
 


pdfreader = PdfReader("Core-java-material.pdf")
print("reading pdf is done...")
print(1%2)
text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=800,
            chunk_overlap=200,
            length_function=len,
        )
print("text splitter object created")

embeddings = OllamaEmbeddings(model="llama3.2")
print("generated embedding for llama3.2")
llm = Ollama(model="llama3.2")
print("llm is created for llama 3.2")
pno = 0
qData = {}
for page in pdfreader.pages:
    content = page.extract_text()
    if content and pno>1 and pno<5:
        
        texts = text_splitter.split_text(content)
        documents = [Document(page_content=text) for text in texts]
        
        # vectorstore = FAISS.from_texts(texts, embeddings)
        
        topicwise_prompt = PromptTemplate.from_template(
            "Using the following Java content, generate unique and topic-wise mcq Questions with its answer. "
            "Label them clearly with the topic and make sure they are diverse and meaningful.\n\n{context}"
        )
        question_gen_chain = create_stuff_documents_chain(llm, topicwise_prompt)
        question_gen_response = question_gen_chain.invoke({
            "context": documents[:6]  # Use multiple chunks for a broader context
        })
        # print(question_gen_response)
        mappedData = rawTextToDict(question_gen_response)
        qData[f"Page No: {pno+1}"] =mappedData
        
        
    pno+=1
    
print(json.dumps(qData,indent=2))


    
        
