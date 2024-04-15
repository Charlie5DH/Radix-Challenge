#!/bin/bash

# Construir as imagens Docker
docker-compose build

# Iniciar os serviços
docker-compose up -d