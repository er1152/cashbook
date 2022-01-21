FROM python:3.9
RUN apt-get update
WORKDIR /src
RUN pip install -r requirements.txt