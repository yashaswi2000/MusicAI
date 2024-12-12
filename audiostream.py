from streamlit_extras.switch_page_button import switch_page
import streamlit as st
import numpy as np
import boto3
from pymongo import MongoClient
from botocore.exceptions import NoCredentialsError
from sentence_transformers import SentenceTransformer, util
from elasticsearch import Elasticsearch
from datetime import datetime
from musicgen import generate_a_new_song
import glob
import os
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
slot = "home_page"
create_store(slot, [
    ("name", ''),
    ("age", 0),
    ("gender", 'Male'),
    ("country", ''),
    ("intro", ''),
    ("clip_name", ''),
    ("genre", ''),
    ("caption", '')
])

def get_image_name(name):
    name = name.split(".")
    return name[0]+name[1]+".png"

def submitted():
    st.session_state.submitted = True
def reset():
    st.session_state.submitted = False

def feed_back():
    with st.form("my_form"):
        rating = st.slider("Form slider")
        submitted = st.form_submit_button("Submit")

    if submitted:
        st.write("heyya!")
        # if st.session_state.submitted == True:
        #     print("into!")
        #     testdb = client.testdb
        #     userlogs = testdb.userlogs
        #     userlogs.insert_one({
        #         "name": name,
        #         "age": number,
        #         "gender": gender,
        #         "country": country,
        #         "query": intro,
        #         "output": music_clips_name,
        #         "rating": rating,
        #         "date": datetime.now(),
        #         "genre": music_clips_name.split(".")[0]
        #     })

def get_s3_file_stream(bucket_name, object_key, region='us-east-1', aws_access_key_id=None, aws_secret_access_key=None):
    """
    Get a stream of a file from an S3 bucket.

    :param bucket_name: Name of the S3 bucket
    :param object_key: Key (path) of the object in the S3 bucket
    :param region: AWS region where the bucket is located (default is 'us-east-1')
    :param aws_access_key_id: AWS access key ID
    :param aws_secret_access_key: AWS secret access key
    :return: A file stream (BytesIO) of the specified S3 object, or None if there was an error
    """
    try:
        # Create an S3 client with explicit access key and secret key
        s3 = boto3.client('s3', region_name=region, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

        # Get the object from S3
        response = s3.get_object(Bucket=bucket_name, Key=object_key)

        # Read the content of the object and return it as a stream
        file_stream = response['Body'].read()
        
        return file_stream

    except NoCredentialsError:
        print("Credentials not available.")
        return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Replace 'your-unique-bucket-name' with your S3 bucket name
bucket_name = 'musicstorage-3144'

# Replace 'path/to/your/file.txt' with the key (path) of the object in the S3 bucket
object_key_one = 'Data/genres_original/'
object_key_two = 'Data/images_original/'
# Replace 'your-access-key-id' and 'your-secret-access-key' with your AWS access key and secret key
access_key_id = 'your-access-key-id'
secret_access_key = 'your-secret-access-key'


st.write("# Sangeetham AI 🎵")
st.write("## welcome! please share the below info to get started ☺️")
name = st.text_input("Your name", key="name")
number = st.number_input("Your age",key="age",step=1)
gender = st.selectbox("Your gender",key="gender",options=['Male','Female','Other'])
country = st.text_input("Your country", key="country")
intro = st.text_area("Your music query",key="intro",max_chars=500) 

if st.button('Go!!! gurll',on_click=reset):
    set_state(slot, ("name", name))
    set_state(slot, ("age", number))
    set_state(slot, ("gender", gender))
    set_state(slot, ("country", country))
    set_state(slot, ("intro", intro))
        #set_state(slot, ("clip_name", music_clips_name))
        #set_state(slot, ("genre", music_clips_name.split(".")[0]))
    switch_page("feedback")
