from langchain_community.chat_models import ChatOllama
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.memory.chat_message_histories import RedisChatMessageHistory
from langchain_core.runnables import Runnable
from typing import Dict

# Dummy population function
def get_population(city: str) -> str:
    data = {
        "bangalore": "8.4 million",
        "delhi": "19 million",
        "mumbai": "20 million"
    }
    return data.get(city.lower(), "Unknown")

# Custom logic to check input and decide what to return
class CustomRunnable(Runnable):
    def invoke(self, input: str, config: Dict = None) -> str:
        # Custom pattern matching — you can use regex for more robust matching
        if "population of" in input:
            city = input.lower().split("population of")[-1].strip().rstrip("?")
            return f"The population of {city.title()} is {get_population(city)}."
        else:
            # Fallback to LLM if not matched
            return llm.invoke(input)

# Redis session setup
redis_url = "redis://localhost:6379"
session_id = "user-session-1"
chat_history = RedisChatMessageHistory(session_id=session_id, url=redis_url)

# Required function for RunnableWithMessageHistory
def get_session_history():
    return chat_history
# LLM Setup
llm = ChatOllama(model="llama3")

# Wrap your logic into the conversation chain
custom_chain = RunnableWithMessageHistory(
    runnable=CustomRunnable(),  # <-- This is where your custom logic goes
    get_session_history=get_session_history
)

# Chat loop
while True:
    user_input = input("You: ")
    if user_input.lower() in ['exit', 'quit']:
        break

    response = custom_chain.invoke(input=user_input)
    print("Bot:", response.content)
