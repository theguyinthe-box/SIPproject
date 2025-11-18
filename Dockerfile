FROM ubuntu:22.04

##file structure setup

COPY ./src /src

WORKDIR /src

## install base dependencies
RUN apt update -y \
    && apt upgrade -y  \
    && apt install -y python3 python3-pip build-essential cmake \
    && pip install tensorflow face-recognition

WORKDIR /src/SIP-GUI

## install gui dependencies
RUN apt install -y curl unzip
RUN curl -fsSL https://fnm.vercel.app/install | bash
RUN ~/.local/share/fnm/fnm install 24

WORKDIR /src

ENTRYPOINT [ "./scripts/entrypoint.sh" ]
CMD ["bash"]