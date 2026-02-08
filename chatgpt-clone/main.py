import streamlit as st

import time

st.header("하이~~ ")

st.button("클릭")

st.text_input("너의 api key 입력해", max_chars=20 )

st.feedback("faces")

with st.sidebar:
    st.badge("Badge 1")


tab1, tab2, tab3 = st.tabs(["Agent", "Chat","Output"])

with tab1:
    st.header("Agent")
with tab2:
    st.header("Agent 2")
with tab3:
    st.header("Agent 3")


with st.chat_message("ai"):
    st.text("하이")
    with st.status('Agent is using tool')as status:
        time.sleep(1)
        status.update(label="Agent is searching the web...")
        time.sleep(2)
        status.update(label="Agent is reading the page...")
        time.sleep(3)
        status.update(state="complete")

with st.chat_message("human"):
    st.text("하이~~")
    

st.chat_input("write a message form the assistant", accept_file=True)