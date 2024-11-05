#!/bin/bash
docker build -t test_app .

docker run -d -p 5004:5000 test_app flask run --host=0.0.0.0 --port=5000
