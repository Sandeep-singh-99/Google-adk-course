from google.adk.agents.llm_agent import Agent
from google.genai import types

"""
Create a weather tool
A tool is a normal Python function that gives an AI agent the ability to perform an action.
"""

def get_weather(city: str) -> dict:
    """
    Retrieves weather information for a specific city.

    Args:
        city: Name of the city.
    
    Returns:
        Weather information.
    """

    mock_weather_db = {
        "kanpur": "Sunny, 28°C",
        "delhi": "Cloudy, 25°C",
        "london": "Rainy, 15°C",
        "tokyo": "Light rain, 18°C",
    }

    city = city.lower().strip()

    if city in mock_weather_db:
        return {
            "status": "success",
            "city": city,
            "weather": mock_weather_db[city]
        }

    return {
        "status": "error",
        "message": f"No Weather information found for {city}"
    }

# Create the weather Agent

weather_agent = Agent(
    name="Weather_agent",
    model="gemini-3.8-flash",
    description="Provides weather information for cities.",
    instruction="""
    You are a helpful assistant.

    When a user asks about weather:
    1. Identify the city.
    2. Call the get_weather tool.
    3. Explain the returned weather information.
    4. If the city is unavailable, explain politely.
    """,

    tools=[get_weather]
)

# Create greeting and farewell tools
def say_hello(name: str = None) -> str:
    """
    Generate a friendly greeting.
    Args:
        name: Optional user name.
    """
    if name:
        return f"Hello {name}! Welcome back."

    return "Hello there! How can I help you?"

def say_goodbye() -> str:
    """
    Generate a farewell message.
    """

    return "Goodbye! Have a great day."

# Create specialized agents

greeting_agent = Agent(
    name="greeting_agent",
    model="gemini-3.8-flash",
    description="Handles greeting and Hello messages.",
    instruction="""
    You are a Greeting Agent.
    Your ONLY responsibility is greeting users.
    Use the say_hello tool.
    If the user provides a name, pass it to the tool.
    Do not perform other task.
    """,
    tools=[say_hello]
)

farewell_agent = Agent(
    name="farewell_agent",
    model="gemini-3.8-flash",
    description="Handles goodbye and farewell messages.",
    instruction="""
    You are a Farewell Agent.
    Your only responsibility is saying goodbye.
    Use the say_goodbye tool.
    Do not perform other tasks.
    """,
    tools=[say_goodbye]
)

root_agent = Agent(
    model='gemini-3.8-flash',
    name='root_agent',
    description='Main coordinator for weather, greetings and farewells.',
    instruction=""" 
    You are the main Assistant.

    You have three responsibilities.

    1. Weather:
       Handle weather questions using weather_agent.

    2. Greetings:
       Delegate greetings to greeting_agent.
    
    3. Farewells:
       Delegate goodbye messages to farewell_agent.

    Analyze the user's request and delegate to the appropriate specialist.

    Do not use the weather tool for greetings
    """,

    sub_agents=[
        weather_agent,
        greeting_agent,
        farewell_agent
    ],

    generate_content_config=types.GenerateContentConfig(
        http_options=types.HttpOptions(
            retry_options=types.HttpRetryOptions(
                attempts=3,
                initial_delay=2,
                max_delay=30,
                exp_base=2,
                http_status_codes=[429, 500, 502, 503, 504]
            )
        )
    )
)
