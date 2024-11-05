FROM python:3.10-slim
WORKDIR /app
COPY . /app
RUN pip install flask pandas
EXPOSE 5000
ENV FLASK_RUN_HOST=0.0.0.0
CMD ["python", "app.py"]

