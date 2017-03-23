FROM ubuntu:16.04
MAINTAINER Miguel Morales <mimoralea@gmail.com>

# update ubuntu installation
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update -y
RUN apt-get install -y --no-install-recommends apt-utils
RUN apt-get upgrade -y

# install dependencies
RUN apt-get install -y libav-tools python3 ipython3 python3-pip python3-opengl
RUN apt-get install -y libpq-dev libjpeg-dev libboost-all-dev libsdl2-dev
RUN apt-get install -y curl cmake swig wget unzip git xpra
RUN pip3 install --upgrade pip
RUN pip3 install numpy scikit-learn scipy pyglet setuptools
RUN pip3 install gym tensorflow keras asciinema
 
WORKDIR /root
ENTRYPOINT ["/notebooks/docker_entrypoint"]
ENV DEBIAN_FRONTEND teletype