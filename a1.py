

from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.documents import Document

# Step 1: Read PDF (first 20 pages)
pdfreader = PdfReader("Core-java-material.pdf")
raw_text = ""
count = 0
for page in pdfreader.pages:
    if count < 20:
        content = page.extract_text()
        if content:
            raw_text += content
    else:
        break
    count += 1
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
embeddings = OllamaEmbeddings(model="llama3.2")  # Make sure llama3.2 is pulled
print("----------------------------------3")

# Step 4: Vector DB
vectorstore = FAISS.from_texts(texts, embeddings)
print("----------------------------------4")

# Step 5: LLM
llm = Ollama(model="llama3.2")
print("----------------------------------5")

# Step 6A: QA Prompt and Chain
qa_prompt = PromptTemplate.from_template(
    "Use the following context to answer the question:\n\n{context}\n\nQuestion: {question}"
)
qa_chain = create_stuff_documents_chain(llm, qa_prompt)
print("----------------------------------6")

# Step 6B: Question Generation Prompt and Chain
topicwise_prompt = PromptTemplate.from_template(
    "Using the following Java content, generate at least 20 unique and topic-wise interview questions. "
    "Label them clearly with the topic and make sure they are diverse and meaningful.\n\n{context}"
)
question_gen_chain = create_stuff_documents_chain(llm, topicwise_prompt)



documents = [Document(page_content=text) for text in texts]
# Step 8: Generate 100 topic-wise questions from PDF
question_gen_response = question_gen_chain.invoke({
    "context": documents[:6]  # Use multiple chunks for a broader context
})

print("\n=== Generated 20 Topic-wise Java Questions ===\n")
print(question_gen_response)
