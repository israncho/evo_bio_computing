#!/bin/bash

if [ $(sudo docker ps -a -q -f name=evo_bio_container) ]; then
    sudo docker stop evo_bio_container
    sudo docker rm evo_bio_container
fi

sudo docker run --network=host -it --name evo_bio_container -v $(pwd):/home/appuser/evo_bio_computing evo_bio_image
