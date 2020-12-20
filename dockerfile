FROM ubuntu:16.04
RUN apt-get update &&\
    apt-get install -y python3 \
                python3-dev \
                wget &&\
    wget https://bootstrap.pypa.io/get-pip.py  &&\
    python3 get-pip.py &&\
    mkdir manhuaSpider
ADD ./ manhuaSpider
RUN pip3 install -r /manhuaSpider/requirements.txt
VOLUME [ "/manhuaSpider/manhuaSpider/images", "/manhuaSpider/out"]
