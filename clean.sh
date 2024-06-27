#!/bin/bash

IMAGE_NAME="evo_bio_image"
CONTAINER_NAME="evo_bio_container"

if [ $(sudo docker ps -a -q -f name=$CONTAINER_NAME) ]; then
    sudo docker stop $CONTAINER_NAME
    sudo docker rm $CONTAINER_NAME
fi

if [ $(sudo docker images -q $IMAGE_NAME) ]; then
    sudo docker rmi $IMAGE_NAME
fi

echo "All clean"
