FROM python:3.10-slim
WORKDIR /app
COPY . /app
<<<<<<< HEAD
RUN pip install flask pandas
=======
RUN pip install flask pandas PyPDF2
>>>>>>> cd121bb (app updated with any types of files)
EXPOSE 5000
ENV FLASK_RUN_HOST=0.0.0.0
CMD ["python", "app.py"]

