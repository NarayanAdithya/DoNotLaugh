FROM python:3.7.12-alpine3.14
RUN apk update && apk add gcc libc-dev make git libffi-dev openssl-dev python3-dev libxml2-dev libxslt-dev 
WORKDIR /app
COPY config.py .
COPY laugh.py .
COPY requirements.txt .
COPY /app .
RUN pip install -r requirements.txt
CMD python laugh.py