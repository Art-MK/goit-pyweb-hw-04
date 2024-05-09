#!/bin/sh
tag="flask-app"
storage_path=$HOME
docker build -t $tag .
docker run -d -p 3000:3000 -v $storage_path/$tag:/app/storage $tag