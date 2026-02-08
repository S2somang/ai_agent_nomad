import streamlit as st

import time
# 리 랜더링되도 저장하고있을 data공간이 필요
if "is_admin" not in st.session_state:
    st.session_state["is_admin"] = False

st.header("하이~~ ")


st.chat_input("write a message form the assistant", accept_file=True)

name =st.text_input("이름뭐야")
if name:
    st.write(f"hi {name}")
    st.session_state["is_admin"] = True

print(st.session_state["is_admin"])