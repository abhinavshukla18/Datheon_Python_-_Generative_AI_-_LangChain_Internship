# Task 3: Multi-Tool Autonomous AI Agent

A console AI agent built with LangChain and Gemini that decides on its own which tool to use to solve multi-step questions, and prints its reasoning as it goes.

## Tools
- `web_search` - real-time web search (DuckDuckGo)
- `calculator` - safe math expression evaluator
- `read_file` - reads local text files from the `files/` folder

## How it works
The agent loops: Thought -> Action (tool call) -> Observation (tool result) -> repeat until it has enough information for a final answer. Every step is printed in the console.

## Setup
Python 3.12 is recommended.
```
pip install -r requirements.txt
```
Copy `.env.example` to `.env` and add your Gemini API key.

## Usage
```
python agent.py
```
Example questions:
- Read notes.txt and tell me the approved budget divided by the number of team members.
- Search the web for the height of Mount Everest in meters, then convert it to feet by multiplying by 3.281.

## Project structure
- `tools.py` - tool definitions
- `agent.py` - agent setup and the console loop
- `test_tools.py` - quick test of the tools without the LLM
- `files/` - local files the agent can read

## Tech
Python, LangChain (`create_agent`), Gemini API, ddgs