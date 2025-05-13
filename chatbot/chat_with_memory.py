from langchain_community.chat_models import ChatOllama
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from difflib import SequenceMatcher
import os

# === File for saving chat history ===
CHAT_LOG_PATH = "chat_history.txt"

# === Load chat history ===
def load_chat_log(filepath):
    if not os.path.exists(filepath):
        return []
    with open(filepath, "r", encoding="utf-8") as f:
        blocks = f.read().strip().split("\n\n")
    chat_pairs = []
    for block in blocks:
        if "You:" in block and "Bot:" in block:
            parts = block.strip().split("Bot:")
            question = parts[0].replace("You:", "").strip()
            answer = parts[1].strip()
            chat_pairs.append((question, answer))
    return chat_pairs

# === Save new chat to file ===
def save_to_chat_log(filepath, question, answer):
    with open(filepath, "a", encoding="utf-8") as f:
        f.write(f"You: {question}\nBot: {answer}\n\n")

# === Search for similar question ===
def find_similar_question(user_input, history, threshold=0.8):
    for q, a in history:
        similarity = SequenceMatcher(None, user_input.lower(), q.lower()).ratio()
        if similarity >= threshold:
            return a
    return None

# === Initialize model and memory ===
llm = ChatOllama(model="llama3")
memory = ConversationBufferMemory()
conversation = ConversationChain(
    llm=llm,
    memory=memory,
    verbose=True
)

# === Load existing history ===
chat_log = load_chat_log(CHAT_LOG_PATH)

# === Chat loop ===
print("🤖 Chatbot ready! Ask me anything (type 'exit' to quit)\n")
while True:
    user_input = input("You: ")
    if user_input.lower() in ['exit', 'quit']:
        print("👋 Goodbye!")
        break

    # Step 1: Check previous history
    old_answer = find_similar_question(user_input, chat_log)
    if old_answer:
        print("Bot (from memory):", old_answer)
        continue

    # Step 2: Use model if not found
    response = conversation.predict(input=user_input)
    print("Bot:", response)

    # Step 3: Save new interaction
    save_to_chat_log(CHAT_LOG_PATH, user_input, response)
    chat_log.append((user_input, response))
