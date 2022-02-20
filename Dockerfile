FROM python:3.9
RUN apt-get update
WORKDIR /src
COPY ./requirements.txt /src/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt