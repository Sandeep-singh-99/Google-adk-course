from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm
from google.genai import types

root_agent = Agent(
    model="gemini-2.5-flash",
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction='Answer user questions to the best of your knowledge',
    generate_content_config=types.GenerateContentConfig(
        temperature=0.7,
        max_output_tokens=512,
        top_k=40,
        top_p=0.95,
        stop_sequences=["\n\n"],
    )
)
