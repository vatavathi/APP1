#!/bin/bash
docker build -t app3 .

docker run -d -p 5006:5000 app3 flask run --host=0.0.0.0 --port=5000

