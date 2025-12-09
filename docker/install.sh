#!/bin/bash -e

# Optional: be stricter
set -u

echo "[1] Purging old Ubuntu docker packages (docker.io etc)..."
sudo apt-get remove --purge -y docker.io docker-compose docker-doc podman-docker || true

echo "[2] Installing Docker CE (engine + compose plugin)..."
sudo apt-get update
sudo apt-get install -y ca-certificates curl gnupg

sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
  sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update
sudo apt-get install -y \
  docker-ce docker-ce-cli containerd.io \
  docker-buildx-plugin docker-compose-plugin

echo "[3] Verifying Docker + Compose..."
sudo docker --version
sudo docker compose version

# NOTE: look for errors you might need to install some missing nvidia toolkit etc

echo "[4] GPU support (NVIDIA container toolkit)..."
sudo apt-get install -y nvidia-container-toolkit
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker

which nvidia-ctk
ls /usr/bin/nvidia-ctk

echo "[5] Testing GPU in container..."
sudo docker run --rm --gpus all nvidia/cuda:12.4.1-base-ubuntu22.04 nvidia-smi || {
  echo "GPU test failed – check drivers / nvidia-smi on host."
}

echo "[6] Adding current user to 'docker' group (needs logout/login)..."
sudo usermod -aG docker "$USER"

echo "Done. Log out and back in, then run:"
echo "  docker --version"
echo "  docker compose version"
echo "  docker run --rm hello-world"


