import fitz  # PyMuPDF
import time
def extract_topics_with_bold_or_caps(pdf_path):
    doc = fitz.open(pdf_path)
    topics = {}
    current_topic = None
    buffer = []

    for page in doc:
        blocks = page.get_text("dict")["blocks"]

        for block in blocks:
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    text = span["text"].strip()
                    font = span["font"].lower()
                    is_bold = "bold" in font
                    is_caps = text.isupper() and len(text) > 3

                    if is_bold or is_caps:
                        # Save previous topic content
                        if current_topic and buffer:
                            topics[current_topic] = '\n'.join(buffer).strip()
                            buffer = []
                        current_topic = text
                    elif current_topic:
                        buffer.append(text)

    # Save last topic
    if current_topic and buffer:
        topics[current_topic] = '\n'.join(buffer).strip()

    return topics

# ---------- Run this ----------
if __name__ == "__main__":
    pdf_path = "/home/ranajit/Desktop/RedIntegro/HuggingFaceWorks/Core-java-material.pdf"  # Replace with your file path
    topics = extract_topics_with_bold_or_caps(pdf_path)

    for i, (topic, content) in enumerate(topics.items(), start=1):
        print(f"\n🔷 {i}. {topic}\n{'-'*len(topic)}\n{content}...\n")
        time.sleep(0.5)
