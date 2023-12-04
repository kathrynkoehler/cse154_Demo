import streamlit as st
from openai import OpenAI
import pinecone
import os
import json
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')  # Replace with your api key
PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
PINECONE_API_ENV = "gcp-starter"
MAX_CONTEXT = 5 # conversational memory window. First index is system call
model_name = 'text-embedding-ada-002'

if (not (OPENAI_API_KEY and PINECONE_API_ENV)):
    OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
    PINECONE_API_KEY = st.secrets["PINECONE_API_KEY"]

# initialize pinecone
pinecone.init(
    api_key=PINECONE_API_KEY,  # find at app.pinecone.io
    environment=PINECONE_API_ENV  # next to api key in console
)

# Define the name of the index and the dimensionality of the embeddings
index_name = "beanie-data"
dimension = 1536 # opeanAI default

index = pinecone.Index(index_name)

client = OpenAI(api_key=OPENAI_API_KEY)

# Search for beanie baby using Pinecone vector db
def beanie_search(query):
    # Embed question
    response = client.embeddings.create(input=query, model=model_name)
    xq = response.data[0].embedding;
    res = index.query([xq], top_k=3, include_metadata=True)
    beanies = ""
    for match in res['matches']:
        beanies+=(f"{match['metadata']['text']}")

    print(beanies)
    return beanies

st.title("Beanie Baby Bot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# communicating with the bot
if prompt := st.chat_input("What is up?"):
    beanie_req = beanie_search(prompt)
    print(beanie_req)
    st.session_state.messages.append({"role": "user", "content": prompt + "\n" + beanie_req })
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        ):
            full_response += (response.choices[0].delta.content or "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
