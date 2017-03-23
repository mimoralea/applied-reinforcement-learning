FROM ubuntu:16.04
MAINTAINER Miguel Morales <mimoralea@gmail.com>

# update ubuntu installation
RUN apt-get update -y && apt-get upgrade -y && apt-get install apt-utils -y

# install dependencies
RUN apt-get install -y libav-tools python3 ipython3 python3-pip
RUN apt-get install -y python3-numpy
    python3-scipy \
    python3-pyglet \
    python3-setuptools \
    python3-pip \
    libpq-dev \
    libjpeg-dev \
    curl \
    cmake \
    swig \
    python3-opengl \
    libboost-all-dev \
    libsdl2-dev \
    wget \
    unzip \
    git \
    xpra
 
# install openai gym
WORKDIR /usr/local/gym
RUN mkdir -p gym && touch gym/__init__.py
COPY ./gym/version.py ./gym
COPY ./requirements.txt .
COPY ./setup.py .
RUN pip3 install -e .[all]
COPY . /usr/local/gym

# install packages for illustrations
RUN pip3 install asciinema

# clean up
RUN apt-get clean \
RUN rm -rf /var/lib/apt/lists/*

WORKDIR /root
ENTRYPOINT ["/usr/local/gym/bin/docker_entrypoint"]
