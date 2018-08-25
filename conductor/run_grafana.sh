#!/bin/bash

docker run \
    -p 3000:3000 \
    -v $PWD/grafana:/var/lib/grafana \
    -e "GF_INSTALL_PLUGINS=grafana-clock-panel" \
    fg2it/grafana-armhf:v5.0.4



# mkdir data # creates a folder for your data
# ID=$(id -u) # saves your user id in the ID variable

# # starts grafana with your user id and using the data folder
# docker run -d --user $ID --volume "$PWD/data:/var/lib/grafana" -p 3000:3000 grafana/grafana:5.1.0
