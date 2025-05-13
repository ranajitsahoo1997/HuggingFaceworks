from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from read_and_save_pdf import retriever

model = OllamaLLM(model="llama3.2")

template = """
You are very good at prviding content of the topic from the pdf I have provided you.

Here is the retriever which has already been trained on the pdf content: {retriever}


Here is the topic to answer: {topic}

"""
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

while True:
    print("\n\n-------------------------------")
    topic = input("Provide any Topic name (q to quit): ")
    print("\n\n")
    if topic == "q":
        break
    
    
    reviews = retriever.invoke(topic)
    result = chain.invoke({"retriever": reviews, "topic": topic})
    print(result)
    