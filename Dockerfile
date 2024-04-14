# pull official base image
FROM python:3.10.12

# set work directory
WORKDIR /home

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update 
RUN apt-get install -y libreoffice
COPY requirements.txt .

RUN pip install -r requirements.txt 
