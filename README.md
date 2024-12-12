# Music AI - Sangeetham AI

A interactive music search AI which can help you search for song based on a quick description on how you would like the song to be. Apart from that it also has various other functionalities like music generation and music search over third party platforms.

## How to run it?

#### set up the audio files in a file store or AWS S3:
```
python S3ObjectLoader.py
```
this file deals with reading the data and loading the audio data files into S3.

#### seting up vectorDB for vector search
* assuming you have a elastic search cluster running in local or cloud
```
run vectorembed.ipynb 
```
to parallely build vector embeddings and index into elastic search
this also deals with storing the data in mongoDB where we store captions of the audio files.

#### setting up MongoDb and Kafka cluster
```
run ./start.sh
```
this basically does docker compose up -d which brings up the kafka containers and mongodb with setting up  replication, and then does curl calls to configure kafka connect connectors for source and sink.

#### setting up Sangeetham AI UI
```
streamlit run audiostream.py
```
we use streamlit for our UI library, and this basically launches the python server which serves the UI. files related to this are :
- audiostream.py
- Pages/feedback.py
- Pages/reasoning.py


### description of Ipynb we have built for this project:

- 001: Produces YouTube link to the clip most - closely aligned with the query prompt
- 002: Uses Spotify API to access the repository of albums and tracks
- 003: Matches queries with songs from the captioned dataset (GTZAN) and provides reason for the matching
- 004: NA
- 005: Mood descriptor 
- 006: Music generator using a query from the user
- 007: Automated pipeline to invoke generator or search-retrieval (in progress)
- 008: Given an audio input, we search and retrieve the most similar sounding song using ACR cloud API and Spotify


#### elastic search queries config:

```
GET /testdb.userlogs/_search

PUT /testdb.userlogs/_settings
{
 "settings": {
 "index.default_pipeline": "add-timestamp" 
 }
}

PUT /_ingest/pipeline/add-timestamp
{
 "processors": [
 {
 "set": {
 "field": "timestamp",
 "value": "{{_ingest.timestamp}}"
 }
 }
 ]
}

PUT /testdb.userlogs
{
  "mappings": {
      "properties": {
        "age": {
          "type": "long"
        },
        "country": {
          "type": "text",
          "fields": {
            "keyword": {
              "type": "keyword",
              "ignore_above": 256
            }
          }
        },
        "date": {
          "type": "float"
        },
        "gender": {
          "type": "text",
          "fields": {
            "keyword": {
              "type": "keyword",
              "ignore_above": 256
            }
          }
        },
        "genre": {
          "type": "text",
          "fields": {
            "keyword": {
              "type": "keyword",
              "ignore_above": 256
            }
          }
        },
        "name": {
          "type": "text",
          "fields": {
            "keyword": {
              "type": "keyword",
              "ignore_above": 256
            }
          }
        },
        "output": {
          "type": "text",
          "fields": {
            "keyword": {
              "type": "keyword",
              "ignore_above": 256
            }
          }
        },
        "query": {
          "type": "text",
          "fields": {
            "keyword": {
              "type": "keyword",
              "ignore_above": 256
            }
          }
        },
        "rating": {
          "type": "long"
        }
      }
    }
}


POST /captions-index/_search
{
  "knn": {
    "field": "caption-vector",
    "query_vector": [1, 2],
    "k": 5,
    "num_candidates": 100
  },
  "fields": [ "file-name", "file-type" ]
}


GET /captions-index/_search

PUT /captions-index
{
  "mappings": {
    "properties": {
      "caption-vector": {
        "type": "dense_vector",
        "dims": 384,
        "index": true,
        "similarity": "l2_norm"
      },
      "file-name": {
        "type": "text"
      },
      "file-type": {
        "type": "keyword"
      }
    }
  }
}
```

