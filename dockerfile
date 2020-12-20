FROM ubuntu:16.04
RUN echo  "deb http://security.ubuntu.com/ubuntu xenial-security main " >>/etc/apt/sources.list &&\
    apt-get update &&\
    apt-get install -y python3 \
                python3-dev &&\
    wget https://bootstrap.pypa.io/get-pip.py  &&\
    python3 get-pip.py &&\
    mkdir manhuaSpider
ADD ./ manhuaSpider
RUN pip3 install -r /manhuaSpider/requirements.txt

