import os
from pathlib import Path
from dotenv import load_dotenv

# app.py 기준 같은 폴더의 .env를 확실히 로드
load_dotenv(Path(__file__).resolve().parent / ".env")
import asyncio
import streamlit as st
from agents import Agent, Runner, SQLiteSession

if "agent" not in st.session_state:
    st.session_state["agent"] = Agent(
        name="ChatGpt Clone",
        instructions="""
        You are a helpful assistant.
        """
    )

agent = st.session_state["agent"]

# session_state 안ㅔ session이; 없을때만 값을 넣어쥼..
if "session" not in st.session_state:
    st.session_state["session"] = SQLiteSession(
        "chat-history",
        "chat-gpt-clone-memory.db",
    ) 


session = st.session_state["session"]


async def run_agent(message):
    stream = Runner.run_streamed(
        agent,
        message,
        session=session
    )

    async for event in stream.stream_events():
        if event.type == "raw_response_event":
            if event.data.type == "response.output_text.delta":
                with st.chat_message("ai"):
                    st.write(event.data.delta)


prompt = st.chat_input("write a message for your assistant")

if prompt:
    with st.chat_message("human"):
        st.write(prompt) # 이렇게 하면 내가 입력할때마다 재실행되는거라 전에 입력한게 없어짐
    asyncio.run(run_agent(prompt))

with st.sidebar:
    reset = st.button("리셋 메모리")
    if reset:
        asyncio.run(session.clear_session())
    st.write(asyncio.run(session.get_items()))
