FROM python:3.10.12-alpine3.18
RUN adduser -D -h /app -s /bin/sh app_user
USER app_user
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
ENTRYPOINT ["python", "src/main.py"]
