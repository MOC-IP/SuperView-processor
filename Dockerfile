# source https://github.com/mingfang/docker-geekbench
FROM ubuntu:16.04

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update
RUN apt-get install --reinstall -y python3.5
RUN apt-get update && apt-get install -y \
    python-setuptools \
    python-pip \
	build-essential python-dev git \
	cython \
	python-numpy \
	python-scipy 
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
RUN python -m spacy download en_core_web_md
EXPOSE 5000
CMD ["python", "interface.py"]