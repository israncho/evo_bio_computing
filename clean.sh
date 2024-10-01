#!/bin/bash

IMAGE_NAME="evo_bio_image"
CONTAINER_NAME="evo_bio_container"

if [ $(docker ps -a -q -f name=$CONTAINER_NAME) ]; then
    docker stop $CONTAINER_NAME
    docker rm $CONTAINER_NAME
fi

if [ $(docker images -q $IMAGE_NAME) ]; then
    docker rmi $IMAGE_NAME
fi

echo "All clean"
