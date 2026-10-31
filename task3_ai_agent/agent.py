import os
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI

from tools import web_search, calculator, read_file

load_dotenv()

SYSTEM_PROMPT = """You are a research assistant with three tools: web_search, calculator, read_file.
Before every tool call, write one short sentence starting with 'Thought:' explaining why you need the tool.
Use calculator for any arithmetic instead of doing it yourself.
Use read_file when the user mentions a local file.
When you have enough information, give a clear final answer."""


def text_of(msg):
    if isinstance(msg.content, str):
        return msg.content
    return "".join(p.get("text", "") for p in msg.content if isinstance(p, dict))


def build_agent():
    llm = ChatGoogleGenerativeAI(
        model="gemini-flash-lite-latest",
        google_api_key=os.getenv("GEMINI_API_KEY"),
        temperature=0,
        timeout=60,
    )
    return create_agent(
        model=llm,
        tools=[web_search, calculator, read_file],
        system_prompt=SYSTEM_PROMPT,
    )


def run(agent, question):
    seen = 0
    final = ""
    stream = agent.stream(
        {"messages": [{"role": "user", "content": question}]},
        stream_mode="values",
        config={"recursion_limit": 15},
    )
    for state in stream:
        messages = state["messages"]
        for msg in messages[seen:]:
            if msg.type == "ai":
                text = text_of(msg).strip()
                if msg.tool_calls:
                    if text:
                        print(f"\n{text}")
                    for call in msg.tool_calls:
                        print(f"Action: {call['name']}({call['args']})")
                else:
                    final = text
            elif msg.type == "tool":
                print(f"Observation: {text_of(msg)[:300]}")
        seen = len(messages)
    return final


if __name__ == "__main__":
    agent = build_agent()
    print("Research agent ready. Type 'exit' to quit.")
    while True:
        q = input("\nYou: ").strip()
        if q.lower() == "exit":
            break
        if not q:
            continue
        try:
            print("\nFinal answer:", run(agent, q))
        except Exception as e:
            print("Error:", e)