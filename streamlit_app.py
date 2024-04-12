import streamlit as st
from openai import OpenAI
import pinecone
import os
import json
from dotenv import load_dotenv

DEBUG = False

#=====================================================#
#                      API SETUP                      #
#=====================================================#
load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')  # Replace with your api key
PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
PINECONE_API_ENV = "gcp-starter"
MAX_CONTEXT = 5 # conversational memory window. First index is system call
model_name = 'text-embedding-ada-002'

# Getting api keys for running locally/hosted on streamlit
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
dimension = 1536 # OpeanAI default

index = pinecone.Index(index_name)

client = OpenAI(api_key=OPENAI_API_KEY)

#=====================================================#
#                    Front-end                        #
#=====================================================#
st.set_page_config(page_title="Beanie Baby Bot", page_icon=":bug:")
st.title("Beans, the Beanie Baby chatbot")

with st.sidebar:
    st.markdown("# About 🙌")
    st.markdown("Beanie-GPT is your personal beanie baby curator!")
    st.markdown("With late 20th century knowledge of beanie babies, Beans can figure out which plush is just right for you!")
    st.markdown("Unlike chatGPT, Beanie-GPT will answer using injected knowledge from [www.angelfire.com/ar/bbcollector/poems.html](https://www.angelfire.com/ar/bbcollector/poems.html).")
    st.markdown("---")
    st.markdown("An instructional project by Elias Belzberg & Kathryn Koehler")
    st.markdown("ebelz@cs.washington.edu")
    st.markdown("kkoe@cs.washington.edu")
    # st.markdown("Code available here!\n"
    #             "[github.com/kathrynkoehler/cse154_Demo](https://github.com/kathrynkoehler/cse154_Demo)")
    st.markdown("---")
    st.markdown("Tech this project uses:\n"
                "- OpenAI gpt3.5 turbo LLM\n"
                "- Puppeteer web scraping\n"
                "- Pinecone vector database\n"
                "- Streamlit")
    st.markdown("---")

# Display chat messages from history on app rerun
if "messages" in st.session_state:
    i = 0
    for message in st.session_state.messages:
        role = message["role"]
        with st.chat_message(role):
            st.markdown(message["content"])
            if role == "assistant":
                st.image(st.session_state.images[i])
                st.markdown(st.session_state.poem[i])
                i+=1

#=====================================================#
#                     Chat Code                       #
#=====================================================#
# Search for beanie baby using Pinecone vector db
def beanie_search(query):
    # Embed question
    response = client.embeddings.create(input=query, model=model_name)
    xq = response.data[0].embedding;
    res = index.query([xq], top_k=1, include_metadata=True)
    beanies = ""
    for match in res['matches']:
        beanies+=(f"{match['metadata']['text']}")
    print(beanies)
    print(beanies.splitlines())
    return beanies

# Initialize chat history
if "bot_chat" not in st.session_state:
    st.session_state.bot_chat = []
    system_prompt = "You are Beans! A beanie baby chatbot meant to tell people which beanie baby\
        best matches their personality based on their input and the provided context.\
        Make responses fun and add lots of emojis."
    st.session_state.bot_chat.append({"role": "system", "content": system_prompt })

if "images" not in st.session_state:
    st.session_state.images = []

if "poem" not in st.session_state:
    st.session_state.poem = []

if "messages" not in st.session_state:
    st.session_state.messages = []

# communicating with the bot
if prompt := st.chat_input("Find your Beanie Baby!"):
    beanie_req = beanie_search(prompt)
    image = beanie_req.splitlines()[2].split(" ")[-1]
    # case where no image exists
    if image == "found":
        image = "img/ty.gif"
    poem = beanie_req.splitlines()[3].split(":")[-1]
    st.session_state.images.append(image)
    st.session_state.poem.append(poem)
    st.session_state.bot_chat.append({"role": "user", "content": prompt + "\n CONTEXT: " + beanie_req })
    st.session_state.messages.append({"role": "user", "content": prompt})
   # display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    # display bot's message
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.bot_chat
            ],
            stream=True,
        ):
            full_response += (response.choices[0].delta.content or "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
        st.image(image)
        st.markdown(poem)

    st.session_state.messages.append({"role": "assistant", "content": full_response})
    st.session_state.bot_chat.append({"role": "assistant", "content": full_response})
