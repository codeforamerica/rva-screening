FROM quay.io/aptible/ubuntu
ADD . /app
WORKDIR /app

RUN apt-get update
RUN apt-get install -y python python-dev python-distribute python-pip
RUN pip install Flask
pip install -r ./requirements.txt

ENV PORT 3000
EXPOSE 3000