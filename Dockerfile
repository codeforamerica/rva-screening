FROM quay.io/aptible/ubuntu 
RUN apt-get update
RUN apt-get install -y python python-dev python-distribute python-pip
RUN pip install Flask
ENV PORT 3000
EXPOSE 3000