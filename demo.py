import streamlit as st

st.set_page_config(page_title="154 demo", page_icon=":wave:", layout="wide")
st.header("Hello!")

clicked = st.button("click me")

if "count" not in st.session_state:
  st.session_state.count = 0

if clicked:
  st.balloons()
  st.session_state.count += 1
  st.write(f"you clicked {st.session_state.count} times!")