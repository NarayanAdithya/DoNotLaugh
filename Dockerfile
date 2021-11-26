FROM python:3.7.12-alpine3.14
COPY . /app
WORKDIR /app
RUN apk add build-base
RUN pip install -r requirements.txt
CMD python laugh.py