import streamlit as st
import requests
from streamlit_lottie import st_lottie


st.set_page_config(page_title="Cool website" ,page_icon = ":fire:", layout="wide")

def lottie_request(url):
  res = requests.get(url)
  if res.status_code != 200:
    return None
  return res.json()


st.header("Hi, Welcome to my website :wave:")
st.divider()

# About Me
st.header("About Me")
column1, column2 = st.columns(2)
with column1:
  st.write("Hi, my name is Elias I am a Senior at the University of Washington!")
  st.markdown("""
              #### Classes I am taking
              - cse154
              - cse154
              - cse154
              """)
  st.write(
    """
    Commodo sed egestas egestas fringilla phasellus faucibus scelerisque. Pulvinar mattis nunc sed
    blandit libero volutpat sed cras. Fringilla est ullamcorper eget nulla. Egestas sed tempus
    urna et pharetra pharetra massa massa. Nunc vel risus commodo viverra maecenas accumsan lacus.
    Justo donec enim diam vulputate ut pharetra. Metus aliquam eleifend mi in nulla posuere
    sollicitudin. Lobortis mattis aliquam faucibus purus. Massa tincidunt dui ut ornare lectus sit
    amet. Et molestie ac feugiat sed lectus vestibulum. Mattis ullamcorper velit sed ullamcorper.
    Quam adipiscing vitae proin sagittis nisl rhoncus mattis rhoncus. Pulvinar sapien et ligula
    ullamcorper malesuada. Orci phasellus egestas tellus rutrum tellus pellentesque. Ut venenatis
    tellus metus vulputate eu scelerisque felis imperdiet. Etiam erat velit scelerisque in dictum.
    """
  )

with column2:
  lottie_animation = lottie_request("https://lottie.host/063967a2-9475-494a-b25e-4be2af9e3d6f/z4iD50gHm8.json")
  st_lottie(lottie_animation, height=400)


# Projects
st.divider()
with st.container():
  st.header("Projects")
  img_column, text_column = st.columns((1,2))
  with img_column:
    st.image("https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fi.pinimg.com%2Foriginals%2Fd2%2Ffa%2F99%2Fd2fa99e4c66da9df17f40474b62864b1.jpg&f=1&nofb=1&ipt=775293a832086fafb85491ec1d083db04c1457f052fa56baaa88f50a1ff2834b&ipo=imagess")
  with text_column:
    st.subheader("My dubhacks project")
    st.write(
    """
    Commodo sed egestas egestas fringilla phasellus faucibus scelerisque. Pulvinar mattis nunc sed
    blandit libero volutpat sed cras. Fringilla est ullamcorper eget nulla. Egestas sed tempus
    urna et pharetra pharetra massa massa. Nunc vel risus commodo viverra maecenas accumsan lacus.
    Justo donec enim diam vulputate ut pharetra. Metus aliquam eleifend mi in nulla posuere
    sollicitudin. Lobortis mattis aliquam faucibus purus. Massa tincidunt dui ut ornare lectus sit
    amet. Et molestie ac feugiat sed lectus vestibulum. Mattis ullamcorper velit sed ullamcorper.
    Quam adipiscing vitae proin sagittis nisl rhoncus mattis rhoncus. Pulvinar sapien et ligula
    ullamcorper malesuada. Orci phasellus egestas tellus rutrum tellus pellentesque. Ut venenatis
    tellus metus vulputate eu scelerisque felis imperdiet. Etiam erat velit scelerisque in dictum.
    """
  )
    st.markdown("[Link](https:/www.example.com)")
with st.container():
  st.header("Projects")
  img_column, text_column = st.columns((1,2))
  with img_column:
    st.image("https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fi.pinimg.com%2Foriginals%2Fd2%2Ffa%2F99%2Fd2fa99e4c66da9df17f40474b62864b1.jpg&f=1&nofb=1&ipt=775293a832086fafb85491ec1d083db04c1457f052fa56baaa88f50a1ff2834b&ipo=imagess")
  with text_column:
    st.subheader("Cool project from cse154")
    st.write(
    """
    Commodo sed egestas egestas fringilla phasellus faucibus scelerisque. Pulvinar mattis nunc sed
    blandit libero volutpat sed cras. Fringilla est ullamcorper eget nulla. Egestas sed tempus
    urna et pharetra pharetra massa massa. Nunc vel risus commodo viverra maecenas accumsan lacus.
    Justo donec enim diam vulputate ut pharetra. Metus aliquam eleifend mi in nulla posuere
    sollicitudin. Lobortis mattis aliquam faucibus purus. Massa tincidunt dui ut ornare lectus sit
    amet. Et molestie ac feugiat sed lectus vestibulum. Mattis ullamcorper velit sed ullamcorper.
    Quam adipiscing vitae proin sagittis nisl rhoncus mattis rhoncus. Pulvinar sapien et ligula
    ullamcorper malesuada. Orci phasellus egestas tellus rutrum tellus pellentesque. Ut venenatis
    tellus metus vulputate eu scelerisque felis imperdiet. Etiam erat velit scelerisque in dictum.
    """
  )
    st.markdown("[Link](https:/www.example.com)")

# TODO: Interactions

st.divider()

with st.container():
  st.header("User interaction!")
  clicked = st.button("click me")
  if "clicked" not in st.session_state:
    st.session_state.clicked = 0
  if clicked:
    st.session_state.clicked += 1
    st.write(f"You clicked {st.session_state.clicked} times!")
    st.balloons()

st.sidebar.header("My website  :wave:")

st.sidebar.markdown("""
                    ## Contacts
                    Elias Belzberg
                    - ebelz@cs.washington.edu
                    - 206.xxx.xxxx
                    """)