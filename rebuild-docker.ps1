#!/bin/bash

docker-compose down

docker build -t api-gustavo-rinha-2024:latest .

docker-compose up --build -d
