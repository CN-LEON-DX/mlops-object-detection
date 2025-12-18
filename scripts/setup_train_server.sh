#!/bin/bash

if [ ! -d "$HOME/miniconda3" ]; then
    echo "Installing Miniconda..."
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh
    bash miniconda.sh -b -u -p $HOME/miniconda3
    rm miniconda.sh
else
    echo "miniconda already installed."
fi

source "$HOME/miniconda3/etc/profile.d/conda.sh"
conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main
conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r

if { conda env list | grep 'mlops-cicd'; } >/dev/null 2>&1; then
    echo "Env mlops-cicd already exists.Updating dep..."
else
    echo "Creating env mlops-cicd..."
    conda create -n mlops-cicd python=3.11 -y
fi

conda activate mlops-cicd
python -m pip install --upgrade pip
python -m pip install dvc[s3]

echo "setup server env successfully!"