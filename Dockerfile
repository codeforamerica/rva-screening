FROM quay.io/aptible/ubuntu
ADD . /app
WORKDIR /app

RUN apt-get update
RUN apt-get install -y python python-dev python-distribute python-pip libpq-dev libffi-dev nodejs
RUN pip install Flask
RUN pip install -r ./requirements.txt
RUN npm install
RUN gulp build
RUN python ./upload_assets.py

ENV PORT 3000
EXPOSE 3000