from streamlit_extras.switch_page_button import switch_page
import streamlit as st
import numpy as np
import boto3
from pymongo import MongoClient
from botocore.exceptions import NoCredentialsError
from sentence_transformers import SentenceTransformer, util
from elasticsearch import Elasticsearch
from datetime import datetime
import glob
import os
import requests
from fire_state import create_store, get_state, set_state

st.set_page_config(initial_sidebar_state="collapsed")
st.markdown(
    """
<style>
    [data-testid="collapsedControl"] {
        display: none
    }
</style>
""",
    unsafe_allow_html=True,
)

# API keys and tokens
API_URL_Z = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
headers_Z = {"Authorization": "Bearer _token"}

slot = "home_page"
    
def Zephyr_overall_opinion(Clips_descriptions, query):
    Z_Query_Final = f"""<|system|>
        ROLE: song suggestion reasoner. You matched the my REQUEST for song with another song having the following DESCRIPTION. Tell me why you matched these in 20 words?</s>
        <|user|>
        DESCRIPTION: {Clips_descriptions}
        REQUEST: {query}</s>
        <|assistant|>"""
    Zephyr_B_Beta_Final_Generated_Response = requests.post(API_URL_Z, headers=headers_Z, json={"inputs": Z_Query_Final}).json()
    return Zephyr_B_Beta_Final_Generated_Response[0]["generated_text"][len(Z_Query_Final):]


reason = Zephyr_overall_opinion(get_state(slot, "caption"), get_state(slot, "intro"))
st.write("# Here is our suggestion and why we think its a good one 🥳")
st.write(reason)
if st.button("Go Back"):
    switch_page("audiostream")