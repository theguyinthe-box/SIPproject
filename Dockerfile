FROM continuumio/anaconda3

##file structure setup

COPY ./src /src

WORKDIR /src

## setup adb keys
RUN mkdir -p ~/.android/ && cp /src/adbkey* ~/.android/

## install base dependencies
RUN apt update -y \
    && apt upgrade -y  \
    && apt install -y build-essential cmake wget adb

## install conda
RUN conda create -n sip python=3.8 -y
RUN echo "source activate sip" > ~/.bashrc
ENV PATH /opt/conda/envs/sip/bin:$PATH
RUN conda install pip
RUN pip install -r requirements.txt

## download models
RUN sh scripts/download_models.sh

## install gui dependencies
RUN sh scripts/install_gui_dependencies.sh

ENTRYPOINT [ "./scripts/entrypoint.sh" ]
CMD ["bash"]