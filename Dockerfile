
# Dockerfile for stylegan3-editing
# - Base image uses NVIDIA CUDA runtime to allow GPU-enabled PyTorch installs.
# - Installs system deps (git, ffmpeg, build tools), Python 3.9 and pip.
# - Copies and installs Python dependencies from requirements.txt before copying the full repo to leverage Docker layer cache.
# - Default command drops to a shell; override with your own command (training / inference scripts / jupyter).

#############################
# Build-time arguments
#############################
# You can change PYTHON_VERSION or the CUDA base image tag as needed for your platform
ARG BASE_IMAGE=nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04
ARG PYTHON_VERSION=3.9

FROM ${BASE_IMAGE}

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# Minimal set of packages required by this repository (adjust as needed)
RUN apt update -y && \
	apt upgrade -y && \
	apt install -y --no-install-recommends \
		ca-certificates \
		wget \
		curl \
		adb \
		unzip \
		npm \
		cmake \
		git \
		build-essential \
		ffmpeg \
		libsm6 \
		libxext6 \
		software-properties-common \
		locales \
	&& locale-gen en_US.UTF-8 \
	&& rm -rf /var/lib/apt/lists/*

WORKDIR /workspace
# Create workspace dir; do NOT copy the repository to avoid large images and rebuilds.
# Mount your local repo into /workspace when running the container (see run example below).
# Install Miniforge (small, conda-forge-backed conda) and create the conda env from
# environment/sg3_env.yaml. We copy only that YAML so the image doesn't include the
# whole working tree and doesn't require rebuilds when sources change.

# Install Miniforge (miniforge3 from conda-forge)
ENV CONDA_DIR=/opt/conda
RUN curl -fsSL -o /tmp/miniforge.sh https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh \
	&& bash /tmp/miniforge.sh -b -p ${CONDA_DIR} \
	&& rm /tmp/miniforge.sh \
	&& ${CONDA_DIR}/bin/conda clean -afy

ENV PATH="${CONDA_DIR}/bin:${PATH}"

# Copy only the environment YAML used to create the conda env
COPY model/environment/sg3_env.yaml /workspace/environment/sg3_env.yaml

# Remove any `prefix:` from the YAML (it hard-codes a user path) and create the
# environment under the name `sg3_env`. Clean cache afterwards to keep the image small.
RUN mkdir -p /workspace \
	&& sed '/^prefix:/d' /workspace/environment/sg3_env.yaml > /workspace/sg3_env_no_prefix.yaml \
	&& conda env create -f /workspace/sg3_env_no_prefix.yaml -n sg3_env -y \
	&& conda clean -afy \
	&& echo "source activate sg3_env" > ~/.bashrc

RUN curl "https://download.pytorch.org/models/alexnet-owt-7be5be79.pth" --create-dirs -o /root/.cache/torch/hub/checkpoints/alexnet-owt-7be5be79.pth
RUN curl "https://raw.githubusercontent.com/richzhang/PerceptualSimilarity/master/lpips/weights/v0.1/alex.pth" --create-dirs -o /root/.cache/torch/hub/checkpoints/alex.pth

# Put the new conda env's bin directory first so the environment is used by default.
ENV PATH="${CONDA_DIR}/envs/sg3_env/bin:${PATH}"

# Install fnm (Fast Node Manager) and Node.js 24 for the SIP-GUI frontend
RUN curl -fsSL https://fnm.vercel.app/install | bash ; \
	~/.local/share/fnm/fnm install 24

CMD ["bash"]