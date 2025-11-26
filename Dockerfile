FROM ubuntu:22.04

##file structure setup

COPY ./src /src

WORKDIR /src

## install base dependencies
RUN apt update -y \
    && apt upgrade -y  \
    && apt install -y python3 python3-pip build-essential cmake wget \
    && pip install tensorflow face-recognition

## download models
RUN sh scripts/download_models.sh

RUN pip install -r requirements.txt

## install gui dependencies
RUN sh scripts/install_gui_dependencies.sh


ENTRYPOINT [ "./scripts/entrypoint.sh" ]
CMD ["bash"]