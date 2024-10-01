#!/bin/bash

if [ $(docker ps -a -q -f name=evo_bio_container) ]; then
    docker stop evo_bio_container
    docker rm evo_bio_container
fi

docker run --network=host -it --name evo_bio_container --hostname my_container -v $(pwd):/home/appuser/evo_bio_computing evo_bio_image
