#!/bin/bash
<<<<<<< HEAD
docker build -t test_app .

docker run -d -p 5004:5000 test_app flask run --host=0.0.0.0 --port=5000
=======
docker build -t app3 .

docker run -d -p 5006:5000 app3 flask run --host=0.0.0.0 --port=5000
>>>>>>> cd121bb (app updated with any types of files)
