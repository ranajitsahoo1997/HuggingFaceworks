from langchain_community.chat_models import ChatOllama
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.memory.chat_message_histories import RedisChatMessageHistory

# Set up Redis chat history
redis_url = "redis://localhost:6379"  # adjust if your Redis is remote
session_id = "user-session-1"         # use a unique session ID per user
chat_history = RedisChatMessageHistory(
    session_id=session_id,
    url=redis_url
)

# Memory that uses Redis for storing chat history
memory = ConversationBufferMemory(
    chat_memory=chat_history,
    return_messages=True
)

# Set up your LLM (e.g., llama3 via Ollama)
llm = ChatOllama(model="llama3")

# Build the chain
conversation = ConversationChain(
    llm=llm,
    memory=memory,
    verbose=True
)

# Chat loop
while True:
    user_input = input("You: ")
    if user_input.lower() in ['exit', 'quit']:
        break
    response = conversation.predict(input=user_input)
    print("Bot:", response)
