from langchain.agents import create_agent
from src.models.chat_model import chat_model

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_agent(
    model=chat_model,
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

# Run the agent
print(agent.invoke(
    {"messages": [{"role": "user", "content": "what is the weather in sf"}]}
))