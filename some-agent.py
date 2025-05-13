# pip install langchain langchain-community pydantic requests


from langchain_community.chat_models import ChatOllama
from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType
from langchain.tools import tool

@tool
def getWeather(city: str):
    """Returns the weather for a given city (mocked response)."""
    if city.lower() == "bangalore":
        return f"Weather in {city} is cloudy with a high of 20°C."
    elif city.lower() == "delhi":
        return f"Weather in {city} is rainy with a high of 15°C."
    
    return f"Weather in {city} is sunny with a high of 25°C."
@tool
def addition(a: int, b: int) -> int:
    """Adds two numbers."""
    return a + b

llm = ChatOllama(
    model="llama3",
    temperature=0.7,
    max_tokens=1000,
    )

tools = [
    Tool(
        name="getWeather",
        func=getWeather,
        description="Get the weather for a given city. Input should be a string with the city name.",
    ),
    Tool(
        name="addition",
        func=addition,
        description="Adds two numbers. Input should be two integers.",
    ),
]

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent_type=AgentType.OPENAI_FUNCTIONS,
    verbose=True,
)

response = agent.run("what is the weather of Delhi")
print("response",response)
