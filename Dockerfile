FROM continuumio/anaconda3

##file structure setup

COPY ./src /src

WORKDIR /src

## install base dependencies
RUN apt update -y \
    && apt upgrade -y  \
    && apt install -y build-essential cmake wget adb

## download models
RUN sh scripts/download_models.sh

## install conda
RUN conda create -n sip python=3.8 -y
RUN echo "source activate sip" > ~/.bashrc
ENV PATH /opt/conda/envs/sip/bin:$PATH
RUN conda install pip
RUN pip install -r requirements.txt -f https://download.pytorch.org/whl/torch_stable.html


## install gui dependencies
RUN sh scripts/install_gui_dependencies.sh

## setup adb keys
RUN mkdir -p ~/.android/ && cp /src/adbkey* /root/.android/.