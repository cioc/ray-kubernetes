FROM ubuntu:xenial
RUN apt-get update \
    && apt-get install -y vim git wget \
    && apt-get install -y cmake build-essential autoconf curl libtool libboost-all-dev unzip \
    && apt-get install -y python-pip
RUN pip install --upgrade pip
RUN git clone https://github.com/robertnishihara/ray.git
RUN git clone https://github.com/jhpenger/ray-kubernetes.git
RUN pip install numpy
#RUN cd /ray \
 #   && git checkout storeport

#install additional dependencies
RUN apt-get update \
    && apt-get -y install flex \
    && apt-get -y install bison \
    && apt-get install -y nano \
    && apt-get install -y openssh-server \
    && apt install -y python-opencv \
    && apt install pssh \
    && pip install cython \
    && pip install pyarrow \
    && apt-get install -y pkg-config \
    && pip install modin \
    && pip install tensorflow \
    && pip install gym \
    && pip install scipy \
    && pip install opencv-python \
    && pip install bokeh \
    && pip install ipywidgets==6.0.0 \
    && pip install jupyter \
    && pip install lz4


RUN ssh-keygen -f /root/.ssh/id_rsa -P "" \
    && echo "StrictHostKeyChecking no" >> /etc/ssh/ssh_config

#COPY start_ray.py /ray/scripts/start_ray.py
#COPY . ray-kubernetes-repo

RUN cd /ray \
    && ./build.sh \
    && cd python \
    && pip install -e .
