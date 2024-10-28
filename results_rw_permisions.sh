#!/bin/bash

TARGET_DIR="results/"

find "$TARGET_DIR" -type d -exec chmod 777 {} \;
find "$TARGET_DIR" -type f -exec chmod 666 {} \;

echo "Read and write permissions given to '/results' directory."