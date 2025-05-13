import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    full_text = ""
    for page in doc:
        full_text += page.get_text()
    return full_text

import ollama

def extract_topics_with_ollama(text, model="llama3"):
    prompt = f"""
You are an assistant. Given the following text from a PDF document, extract all the **topics** and the **corresponding content** for each topic in a structured format like:

Topic: <Topic Name>
Content: <Content related to the topic>

---

Text:
{text}
"""
    response = ollama.chat(model=model, messages=[
        {"role": "user", "content": prompt}
    ])
    return response['message']['content']
pdf_path = "/home/ranajit/Desktop/RedIntegro/HuggingFaceWorks/Core-java-material.pdf"
text = extract_text_from_pdf(pdf_path)
result = extract_topics_with_ollama(text)

print(result)
