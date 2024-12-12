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

def get_image_name(name):
    name = name.split(".")
    return name[0]+name[1]+".png"



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
client = MongoClient("mongodb://localhost:27017/?directConnection=true")

slot = "home_page"
with st.form("my_form"):
    QUERY = get_state(slot, "intro")
    K = 1
    VDB_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    query_embedding = VDB_model.encode(QUERY)
    es = Elasticsearch(['https://66d731f461bf42b09d7000cf2ade257b.us-central1.gcp.cloud.es.io'], http_auth=("username", "password"))
    res = es.knn_search(index="captions-index", knn={
        "field": "caption-vector",
        "query_vector": query_embedding,
        "k": 5,
        "num_candidates": 1000
    }, source=[ "file-name", "file-type" ])
    music_clips_name = res['hits']['hits'][0]["_source"]["file-name"]
    caption = client.testdb.captions.find_one({"file-name": music_clips_name})
    set_state(slot, ("caption", caption["caption"]))

    # Get a stream of the file from S3
    file_stream_image = get_s3_file_stream(bucket_name, object_key_two+music_clips_name.split(".")[0]+"/"+get_image_name(music_clips_name), aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key)
    file_stream = get_s3_file_stream(bucket_name, object_key_one+music_clips_name.split(".")[0]+"/"+music_clips_name, aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key)

    st.write("# Here is our recommendation!! hope you like it 🙏")
    # Example: Print the content of the file stream
    if file_stream_image is not None:
        image_bytes = file_stream
        st.image(object_key_two+music_clips_name.split(".")[0]+"/"+get_image_name(music_clips_name))

    # Example: Print the content of the file stream
    if file_stream is not None:
        audio_bytes = file_stream
        st.audio(audio_bytes, format='audio/wav')

        rating = st.slider("Review of how you felt about our Choice ☺️")
        submit = st.form_submit_button("Submit")

        if submit:
            testdb = client.testdb
            userlogs = testdb.userlogs
            userlogs.insert_one({
                "name": get_state(slot, "name"),
                "age": get_state(slot, "age"),
                "gender": get_state(slot, "gender"),
                "country": get_state(slot, "country"),
                "query": get_state(slot, "intro"),
                "output": music_clips_name,
                "rating": rating,
                "date": datetime.now().timestamp(),
                "genre": music_clips_name.split(".")[0]
            })
            switch_page("reasoning")
    
    # generate_a_new_song(QUERY, "music-gen.wav")
    # st.audio("./music-gen.wav", format='audio/wav')

