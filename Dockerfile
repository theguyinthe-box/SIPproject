FROM ubuntu:22.04

##file structure setup

COPY ./src ~/src

WORKDIR ~/src

## install base dependencies
RUN apt update \
    && apt upgrade  \
    && abpt install python3 python3-pip tensorflow

WORKDIR ~/src/SIP-GUI

## install gui dependencies
RUN apt install nodejs npm

# copy necessary files and scripts    

ENTRYPOINT [ "~/src/scripts/entrypoint.sh" ]


