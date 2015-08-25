FROM quay.io/aptible/autobuild
RUN apt-get install -y python python-dev python-distribute python-pip
RUN pip install Flask
RUN pip install -r app/requirements.txt