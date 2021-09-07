# Build stage
FROM python:3.9-slim-buster

# set working directory
WORKDIR /usr/src/app

# system dependencies for sqlserver
RUN apt-get update \
  && apt-get -y install gcc \
  && apt-get -y install g++ \
  && apt-get -y install unixodbc unixodbc-dev \
  && apt-get clean

# install git for adding dependecies from git
RUN apt-get -y install git

# copy project file
COPY requirements.txt .

# install dependencies
RUN pip install -r requirements.txt

# copy all project
COPY . .

# Set the required environment variables
ENV HTTP_PORT=8080
ENV MONGO_SERVICE_HOST=mongo
ENV MONGO_SERVICE_PORT=27017

# Expose the HTTP port
EXPOSE "8080:8080"

# run test
CMD python ./bin/main.py
