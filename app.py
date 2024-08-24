import streamlit as st
import requests
from dotenv import load_dotenv
import os

load_dotenv()

def ask_gpt(key, model, max_tokens, temperature, content):
    url = "https://api.openai.com/v1/chat/completions"

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + key
    }

    data = {
        "model": model,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "messages": content
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()

st.set_page_config(page_title="Chatbot Debugger", page_icon=":robot:")

def get_chatgpt_modellist():
    url = "https://api.openai.com/v1/models"
    hidden_key = os.getenv('API_KEY')
    headers = {"Authorization": f"Bearer {hidden_key}"}
    response = requests.get(url, headers=headers)

    model_list = [""]
    if response.status_code == 200:
        models = response.json()['data']
        models = sorted(models, key=lambda x: x['created'], reverse=True)
        model_list = [model['id'] for model in models][:10]

    return model_list

with st.sidebar:
    st.title('Chatbot Debugger')
    if 'API_TOKEN' in st.session_state and len(st.session_state['API_TOKEN']) > 1:
        st.success('API Token found', icon='✅')
        key = st.session_state['API_TOKEN']
    else:
        key = ""

    key = st.text_input('Input API Token:', type='password', value=key)

    st.session_state['API_TOKEN'] = key

    model_list = get_chatgpt_modellist()

    model = st.selectbox("model", model_list, index=0)
    max_tokens = st.slider("max_tokens", 0, 2000, value=512)
    temperature = st.slider("temperature", 0.0, 2.0, value=0.8)


def _init_messages():
    st.session_state.messages = [{"role": "assistant", "content": "Hello! How can I assist you today?"}]

# Initialize chat 
if "messages" not in st.session_state.keys():
    _init_messages()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

def clear_chat_history():
    _init_messages()

st.sidebar.button('empty chat history', on_click=clear_chat_history)

if len(key) > 1:
    if prompt := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Loading..."):
                full_response = ask_gpt(key, model, max_tokens, temperature, st.session_state.messages)['choices'][0]['message']['content']
                st.markdown(full_response)

                message = {"role": "assistant", "content": full_response}
                st.session_state.messages.append(message)