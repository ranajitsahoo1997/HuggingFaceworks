from langchain_community.embeddings import OllamaEmbeddings
from sklearn.metrics.pairwise import cosine_similarity


ollama_emb = OllamaEmbeddings(model="llama3.2")

# Embed the MCQ question
# question_embedding = ollama_emb.embed_query("Which planet is known as the Red Planet?")
# question = 3*3
# question_embedding = ollama_emb.embed_query("What is {question}?")
question_embedding = ollama_emb.embed_query("Which of the following types of inheritance is used when a single parent can have multiple children?")

# Embed the answer choices
# choices = [{"Earth":False}, {"Jupiter":False}, {"Mars":True}, {"Venus":False}]
# choices = [ "Earth is known as Blue Planet",
#     "Jupiter is knwon as Grey planet",
#     "Mars is known as the Red Planet and near to Earth.",
#     "Venus is the Cold planet"]
# choices = ["{question}=3","{question}=6","{question}=7","{question}=9"]
choices = ["Single inheritance can have only sigle children",
           "Multilevel inheritance can have one children and that chindren have one",
           "Multiple inheritance can have multiple children",
           "Hybrid inheritance can have single inheritance,multilevel inheritance and so on"]
choice_embeddings = ollama_emb.embed_documents(choices)


similarities = cosine_similarity([question_embedding], choice_embeddings)
print(similarities)


for label, choice, score in zip(['A', 'B', 'C', 'D'], choices, similarities[0]):
    print(f"{label}. {choice} — Similarity: {score:.4f}")


best_index = similarities.argmax()
print(f"\nMost relevant answer: {['A', 'B', 'C', 'D'][best_index]} ({choices[best_index]})")
