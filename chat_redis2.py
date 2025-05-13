from langchain_community.chat_models import ChatOllama
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.memory.chat_message_histories import RedisChatMessageHistory
import time

# Set up Redis chat history
redis_url = "redis://localhost:6379" 
# Use a unique session ID per user 
session_id = "user-session-1"         
chat_history = RedisChatMessageHistory(
    session_id=session_id,
    url=redis_url
)

# Define a function to retrieve the session's message history
def get_session_history():
    return chat_history

# LLM Setup
llm = ChatOllama(model="llama3")

# Build the RunnableWithMessageHistory
conversation = RunnableWithMessageHistory(
    runnable=llm,
    get_session_history=get_session_history  # Function to retrieve session history
)


while True:
    user_input = input("You: ")
    
    if user_input.lower() in ['exit', 'quit']:
        break

    # Get the LLM's response
    response = conversation.invoke(input=user_input)
    print(f"AI: {response['output']}")
    # Store the conversation in Redis   
    # chat_history.add_user_message(user_input)
    # chat_history.add_ai_message(response['output'])
    # # Optional: Sleep for a bit to simulate processing time
    # time.sleep(1)
# Close the Redis connection when done
chat_history.close()
# Note: In a real application, you would want to handle exceptions and ensure the Redis connection is properly managed.
# This code sets up a simple chat interface using Redis for message history and the ChatOllama model for responses.
# The conversation is stored in Redis, allowing for persistent chat history across sessions.
# The user can exit the chat by typing 'exit' or 'quit'.

   