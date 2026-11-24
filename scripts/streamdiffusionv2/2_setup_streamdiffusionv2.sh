#!/usr/bin/env bash
# A lancer DANS Ubuntu (WSL2) :  bash /mnt/c/Users/robin/Downloads/2_setup_streamdiffusionv2.sh
set -e

echo "== GPU =="
nvidia-smi | head -12 || { echo "GPU non visible : mets a jour le pilote NVIDIA sous Windows."; exit 1; }

sudo apt-get update && sudo apt-get install -y git curl wget build-essential

# Miniconda
if [ ! -d "$HOME/miniconda3" ]; then
  wget -q https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /tmp/mc.sh
  bash /tmp/mc.sh -b -p "$HOME/miniconda3"
fi
source "$HOME/miniconda3/etc/profile.d/conda.sh"
conda tos accept 2>/dev/null || true

# Environnement + paquet
conda env list | grep -q "^streamdiffusionv2 " || conda create -n streamdiffusionv2 python=3.10 -y
conda activate streamdiffusionv2
cd "$HOME"
[ -d StreamDiffusionV2 ] || git clone https://github.com/chenfengxu714/StreamDiffusionV2.git
cd StreamDiffusionV2
pip install .
pip install "huggingface_hub[cli]>=0.34,<1.0"

# Modeles 1.3B
huggingface-cli download --resume-download Wan-AI/Wan2.1-T2V-1.3B --local-dir wan_models/Wan2.1-T2V-1.3B
huggingface-cli download --resume-download jerryfeng/StreamDiffusionV2 --local-dir ./ckpts --include "wan_causal_dmd_v2v/*"

# Node.js 18 pour le frontend de la demo
export NVM_DIR="$HOME/.nvm"
if [ ! -d "$NVM_DIR" ]; then curl -so- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash; fi
. "$NVM_DIR/nvm.sh"
nvm install 18

echo
echo "== Installation terminee. Etapes de la demo (demo/README.md) =="
cat demo/README.md
