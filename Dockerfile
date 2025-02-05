FROM python:3.10.12-alpine3.18
RUN mkdir /app
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "main.py"]
