# Google ADK Python Examples

This repository explores Google's Agent Development Kit (ADK) with small Gemini-powered agents. The examples cover Python function tools, Google Search, delegation to specialist agents, and running an agent directly from Python.

## Setup

Use Python 3.14 or newer and `uv`. From the repository root, install the locked dependencies:

```sh
uv sync --locked
```

In the folder of the example you want to run, create a `.env` file with your Gemini API key:

```dotenv
GOOGLE_GENAI_USE_VERTEXAI=FALSE
GOOGLE_API_KEY=your_gemini_api_key
```

Git ignores `.env` files. Each example sets its Gemini model in `agent.py`. If the API reports that a model is unavailable, use a Gemini model ID that your API key can access.

## Run an agent

Start the calculator in the terminal and ask it to add two numbers:

```sh
uv run adk run calculate_agent
```

Or start the local ADK web UI for the calculator and open the address printed in the terminal:

```sh
uv run adk web calculate_agent
```

Replace `calculate_agent` with another interactive example from the table below.

## Examples

| Folder | What it demonstrates | Try asking |
| --- | --- | --- |
| `calculate_agent` | Calls a Python function to add two integers. | What is 12 plus 30? |
| `google_agent` | Uses the built-in Google Search tool to look up or verify information. | What is the latest stable Python release? |
| `multi_tool_agent` | Uses separate tools for sample weather and the current local time. Both tools support New York. | What time is it in New York? |
| `agent_team` | Demonstrates delegation, session state in a weather tool, and a keyword check before the coordinator calls the model. | What's the weather in Tokyo? |
| `neocoder_bot` | Answers general questions with custom Gemini generation settings. | Explain Python list comprehensions. |
| `runner_example` | Sends a fixed math prompt through ADK's `Runner` with an in-memory session and prints the final response. | Run the script below. |

On Windows, the New York time tool may need the `tzdata` package. Supply it for that run with `uv run --with tzdata adk run multi_tool_agent`.

## Agent team

```sh
uv run adk run agent_team
```

The coordinator delegates requests to weather, greeting, and farewell specialists. Try “Hi, my name is Sam,” “What's the weather in Tokyo?” and “Goodbye.”

- **Weather specialist.** Its tool returns sample conditions in Celsius for Kanpur, Delhi, London, and Tokyo.
- **Coordinator weather tool.** Its separate sample data covers London, New York, and Tokyo. It reads `temperature_unit` from session state, defaults to Celsius, and saves a successful lookup as `last_city`. To try Fahrenheit, initialize the session with `temperature_unit` set to `Fahrenheit`. The example currently exposes no chat command for changing the preference.
- **Input callback.** In a fresh session, send `BLOCK` to see the coordinator return a blocked response before calling Gemini. The check matches that substring case-insensitively in the latest user message and sets `request_blocked` in session state. The callback applies to coordinator model calls.

## Run the Python script

```sh
uv run --env-file runner_example/.env python runner_example/agent.py
```

The script asks “What is 10 + 20?” and prints the model's answer.
