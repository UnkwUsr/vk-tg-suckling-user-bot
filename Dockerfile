FROM python:3.10.12-alpine3.18
RUN adduser -D -h /appuser -s /bin/sh appuser
USER appuser
RUN mkdir /appuser/app
WORKDIR /appuser/app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
ENTRYPOINT ["python", "src/main.py"]
