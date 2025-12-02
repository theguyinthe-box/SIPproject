#! /bin/bash

SCRIPT_PATH=$(readlink -f "$0")
SCRIPT_DIR=$(dirname "$SCRIPT_PATH")
# model_194.pth is the model that the program is exepcting to find
#wget -P model/training_artifacts/ffhq/ https://alaeweights.s3.us-east-2.amazonaws.com/ffhq/model_submitted.pth
echo "searching for model at ${SCRIPT_DIR}/../model/training_artifacts/ffhq/model_194.pth"
if [ ! -f "${SCRIPT_DIR}/../model/training_artifacts/ffhq/model_194.pth" ]; then
    echo "We didnt find the model, downloading..."
    wget -P ${SCRIPT_DIR}/../model/training_artifacts/ffhq/ https://alaeweights.s3.us-east-2.amazonaws.com/ffhq/model_194.pth
else
    echo "We found the model! Skipping!"
fi