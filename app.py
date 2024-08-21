import streamlit as st
import requests
from dotenv import load_dotenv
import os
import json 

load_dotenv()

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

