from google.adk.agents.llm_agent import Agent

def calculate_sum(a: int, b: int) -> dict:
    """Calculate the sum of two integers."""
    return {"result": a + b}

root_agent = Agent(
    model='gemini-3.5-flash',
    name='root_agent',
    description='A math assistant',
    instruction="""
    You are a helpful math assistant.
    Use calculate_sum when the user asks
    you to add two numbers.
    """,
    tools=[calculate_sum]
)
