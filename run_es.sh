#!/usr/bin/env bash

# starts an elastic search container
# https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html

# docker run --name es01 --net elastic -p 9200:9200 -it -m 1GB docker.elastic.co/elasticsearch/elasticsearch:8.14.3
docker run -d --name elasticsearch -p 9200:9200 -p 9300:9300 -m 1GB -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:8.14.3

