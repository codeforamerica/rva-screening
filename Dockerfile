FROM quay.io/aptible/autobuild
RUN apt-get install -y python python-dev python-distribute python-pip
RUN pip install Flask
pip install -r ./requirements.txt