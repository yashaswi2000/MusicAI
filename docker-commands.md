docker network create elastic
docker pull docker.elastic.co/elasticsearch/elasticsearch:8.11.3
docker run --name elasticsearch --net elastic -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" -t docker.elastic.co/elasticsearch/elasticsearch:8.11.3

docker pull docker.elastic.co/kibana/kibana:8.11.3
docker run --name kibana --net elastic -p 5601:5601 docker.elastic.co/kibana/kibana:8.11.3


docker run -d --rm -p 27017:27017 --name mongo1 --network kafka-test_default mongo:6 mongod --replSet myReplicaSet --bind_ip localhost,mongo1
