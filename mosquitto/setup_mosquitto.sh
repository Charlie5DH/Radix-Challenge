#!/bin/bash

#You can optionally create more users using the -b (batch) flag instead of -c , supplying the password on the command line:
docker-compose exec mosquitto mosquitto_passwd -c /mosquitto/config/password.txt radix
#docker-compose exec mosquitto mosquitto_passwd -b /mosquitto/conf/mosquitto.passwd seconduser shoaCh3ohnokeathal6eeH2marei2o
