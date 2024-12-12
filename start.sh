#!/bin/bash

# Start containers in background
docker-compose up -d

# Wait for containers to start
sleep 30

# Check if containers are ready 
docker ps --filter status=running 

if [ $? -ne 0 ]; then
  echo "Error: Some containers failed to start"
  exit 1
fi

echo "Containers started successfully!"

# Hit kafka connect endpoints
curl -X POST \
     -H "Content-Type: application/json" \
     --data '{
        "name": "MongoSource",
        "config": {
          "connector.class": "com.mongodb.kafka.connect.MongoSourceConnector",
          "connection.uri": "mongodb://mongo1:27017",
          "database": "testdb",
          "collection": "userlogs",
          "startup.mode":"copy_existing",
          "publish.full.document.only":"true",
          "output.format.value":"json",
          "key.converter.schemas.enable":"false",
          "value.converter.schemas.enable":"false",
          "value.converter":"org.apache.kafka.connect.storage.StringConverter",
          "key.projection.type":"none",
          "key.ignore": "false"
        }
}' \
     http://localhost:8083/connectors

curl -X POST \
     -H "Content-Type: application/json" \
     --data '{
        "name": "elasticConnect201",
        "config": {
          "connector.class": "io.confluent.connect.elasticsearch.ElasticsearchSinkConnector",
          "topics": "testdb.userlogs",
          "connection.url": "https://66d731f461bf42b09d7000cf2ade257b.us-central1.gcp.cloud.es.io",
          "connection.username": "username",
          "connection.password": "password",
          "key.ignore": "true",
          "schema.ignore": "true",
          "output.format.value":"json",
          "key.converter.schemas.enable":"false",
          "value.converter.schemas.enable":"false",
          "value.converter":"org.apache.kafka.connect.json.JsonConverter",
          "transforms": "ReplaceField",
          "transforms.ReplaceField.type": "org.apache.kafka.connect.transforms.ReplaceField$Value",
          "transforms.ReplaceField.exclude": "_id"
        }
}' \
     http://localhost:8083/connectors