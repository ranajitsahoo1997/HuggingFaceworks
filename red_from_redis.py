from langchain.memory.chat_message_histories import RedisChatMessageHistory
import redis

# Set up Redis URL and session ID
redis_url = "redis://localhost:6379"  # Adjust if your Redis is remote
session_id = "user-session-1"         # Unique session ID for a user

# Initialize the RedisChatMessageHistory
chat_history = RedisChatMessageHistory(
    session_id=session_id,
    url=redis_url
)

# Fetch all messages for the given session ID
messages = chat_history.messages

# Print out the messages
print("Chat History:")
for message in messages:
    print(message)
    
    # print(f"user: {message.content}")
