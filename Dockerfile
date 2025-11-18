FROM ubuntu:22.04

##file structure setup

COPY ./src ~/src

WORKDIR ~/src

## install base dependencies
RUN apt update -y \
    && apt upgrade -y  \
    && apt install -y python3 python3-pip \
    && pip install tensorflow  

WORKDIR ~/src/SIP-GUI

## install gui dependencies
RUN apt install -y nodejs npm

WORKDIR ~/src

ENTRYPOINT [ "./scripts/entrypoint.sh" ]
CMD ["bash"]