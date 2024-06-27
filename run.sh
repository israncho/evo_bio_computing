#!/bin/bash

if [ $(sudo docker ps -a -q -f name=evo_bio_container) ]; then
    sudo docker stop evo_bio_container
    sudo docker rm evo_bio_container
fi

sudo docker run -it --name evo_bio_container -v $(pwd)/src:/home/appuser/evo_bio_computing/src evo_bio_image
