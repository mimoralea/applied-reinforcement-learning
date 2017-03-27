FROM jupyter/tensorflow-notebook
MAINTAINER Miguel Morales <mimoralea@gmail.com>
USER root

# update ubuntu installation
RUN apt-get update -y
RUN apt-get install -y --no-install-recommends apt-utils
RUN apt-get upgrade -y

# install dependencies
RUN apt-get install -y libav-tools python3 ipython3 python3-pip python3-dev python3-opengl
RUN apt-get install -y libpq-dev libjpeg-dev libboost-all-dev libsdl2-dev
RUN apt-get install -y curl cmake swig wget unzip git xpra xvfb
RUN apt-get install -y libav-tools fluidsynth build-essential

# clean up
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# jupyter notebook
EXPOSE 8888

# tensorboard
EXPOSE 6006

# switch back to user
USER $NB_USER

# install necessary packages
RUN pip3 install --upgrade pip
RUN pip3 install numpy scikit-learn scipy pyglet setuptools
RUN pip3 install gym tensorflow keras asciinema

# move notebooks into container
# ADD notebooks /mnt/notebooks

# make the dir with notebooks the working dir
WORKDIR /mnt/notebooks

# create a script to start the notebook with xvfb on the back
# this allows screen display to work well
RUN echo '#!/bin/bash' > /tmp/run.sh && \
    echo "nohup sh -c 'tensorboard --logdir=/mnt/notebooks/logs' > /dev/null 2>&1 &" >> /tmp/run.sh && \
    echo 'xvfb-run -s "-screen 0 1280x720x24" /usr/local/bin/start-notebook.sh' >> /tmp/run.sh && \
    chmod +x /tmp/run.sh

# run the script to start the notebook
CMD ["/tmp/run.sh"]
