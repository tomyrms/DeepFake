#!/usr/bin/env bash
# A lancer DANS Ubuntu (WSL2) :  bash /mnt/c/Users/robin/Downloads/3_lancer_demo_webcam.sh
set -e
source "$HOME/miniconda3/etc/profile.d/conda.sh"
conda activate streamdiffusionv2
export NVM_DIR="$HOME/.nvm"; . "$NVM_DIR/nvm.sh"; nvm use 18

cd "$HOME/StreamDiffusionV2/demo"

# Decodeur leger TAEHV (utile avec 8 Go de VRAM)
[ -f ../ckpts/taew2_1.pth ] || curl -L https://github.com/madebyollin/taehv/raw/main/taew2_1.pth -o ../ckpts/taew2_1.pth

# Frontend (une seule fois)
if [ ! -d frontend/build ] && [ ! -d frontend/dist ]; then
  (cd frontend && npm install && npm run build)
fi

chmod +x start.sh
# Tue les restes d'un lancement precedent (ils gardent la memoire GPU)
pkill -f "StreamDiffusionV2/demo" 2>/dev/null || true
pkill -f "main.py" 2>/dev/null || true
sleep 3
nvidia-smi --query-gpu=memory.used,memory.total --format=csv
echo "Ouvre http://localhost:7860 dans le navigateur de WINDOWS (pas 0.0.0.0)."
HOST=0.0.0.0 PORT=7860 GPU_IDS=0 STEP=2 USE_TAEHV=1 ./start.sh 2>&1 | tee "$HOME/demo.log"
