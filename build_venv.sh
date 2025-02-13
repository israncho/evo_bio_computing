#!/bin/bash

python3 -m venv evo_bio_comp_venv
source evo_bio_comp_venv/bin/activate
pip install -r requirements.txt
deactivate
echo "Virtual environment created successfully."