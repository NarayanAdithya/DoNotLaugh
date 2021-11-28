FROM python:3.7.12-alpine3.14
WORKDIR /app
COPY config.py .
COPY laugh.py .
COPY requirements.txt .
COPY /app .
RUN apk add build-base
RUN pip install -r requirements.txt
CMD python laugh.py