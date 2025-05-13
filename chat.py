import requests

messages = []




def chat_with_model(user_input):
    messages.append({"role": "user", "content": user_input})
    response = requests.post(
        'http://localhost:11434/api/chat',
        json={
            "model": "deepseek-r1",
            "messages": messages,
            "stream": False 
        }
    )
    bot_reply = response.json()['message']['content']
    messages.append({"role": "assistant", "content": bot_reply})
    return bot_reply

# Start chatting

while True:
    ask = input("write any question? >> ")
    reply = chat_with_model(ask)
    print(reply)
# print(chat_with_model("Hey there!"))
