FROM ubuntu:16.04
RUN apt-get update &&\
    apt-get install -y python3 \
                python3-dev \
                locales \
                wget &&\
    wget https://bootstrap.pypa.io/get-pip.py  &&\
    python3 get-pip.py &&\
    locale-gen zh_CN &&\
    locale-gen zh_CN.utf8 &&\
    mkdir manhuaSpider
ADD ./ manhuaSpider
RUN pip3 install -r /manhuaSpider/requirements.txt
ENV LANG=zh_CN.UTF-8
ENV LC_ALL=zh_CN.UTF-8
ENV LANGUAGE=zh_CN.UTF-8
VOLUME [ "/manhuaSpider/manhuaSpider/images", "/manhuaSpider/out"]
