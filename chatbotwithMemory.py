from langchain_community.chat_models import ChatOllama
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

# Use your local model — e.g., deepseek-coder, llama3, etc.
llm = ChatOllama(model="llama3")

# Add memory
memory = ConversationBufferMemory()

# Create the conversation chain with memory
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
