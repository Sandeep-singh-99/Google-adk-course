from google.adk.apps import app
from google.adk.agents.llm_agent import Agent
import asyncio
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types


root_agent = Agent(
    model='gemini-3.5-flash',
    name='math_agent',
    instruction='You are a helpful math assistant.',
)


session_service = InMemorySessionService()

runner = Runner(
    agent=root_agent,
    app_name="math_app",
    session_service=session_service
)

async def main():
    await session_service.create_session(
        app_name="math_app",
        user_id="user_1",
        session_id="session_1"
    )

    message = types.Content(
        role="user",
        parts=[types.Part(text="What is 10 + 20?")]
    )

    async for event in runner.run_async(
        user_id="user_1",
        session_id="session_1",
        new_message=message
    ):
     
     if event.is_final_response():
        print(event.content.parts[0].text)

asyncio.run(main())