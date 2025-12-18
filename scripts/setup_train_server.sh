#!/bin/bash
set -e

if [ ! -d "$HOME/miniconda3" ]; then
    echo "Installing Miniconda..."
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh
    bash miniconda.sh -b -u -p $HOME/miniconda3
    rm miniconda.sh
else
    echo "miniconda already installed."
fi

source "$HOME/miniconda3/etc/profile.d/conda.sh"

if { conda env list | grep 'mlops-cicd'; } >/dev/null 2>&1; then
    echo "Env mlops-cicd already exists.Updating dep..."
else
    echo "Creating env mlops-cicd..."
    conda create -n mlops-cicd python=3.11 -y
fi

conda activate mlops-cicd
python -m pip install -q --upgrade pip
python -m pip install -q dvc[s3] torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
python -m pip install -q -r requirements.txt
python -m pip uninstall -y -q opencv-python || true
python -m pip install -q opencv-python-headless --force-reinstall

python -c "import torch; print(f'Torch version: {torch.__version__}')"
python -c "import cv2; print(f'OpenCV version: {cv2.__version__}')"

echo "setup server env successfully!"