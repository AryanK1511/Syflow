#!/bin/bash

# Variables
REMOTE_USER=$1       # SSH username
REMOTE_HOST=$2       # Remote machine IP or hostname
REMOTE_PASSWORD=$3   # SSH password (optional if using key-based auth)
MC_PORT=25565        # Minecraft default port
DOCKER_IMAGE="itzg/minecraft-server"
VOLUME_NAME="mc-data"

echo "Start"

# Ensure SSH credentials are provided
if [ -z "$REMOTE_USER" ] || [ -z "$REMOTE_HOST" ]; then
  echo "Usage: $0 <remote_user> <remote_host> [remote_password]"
  exit 1
fi 

# Install Docker and Start Minecraft Server
ssh "$REMOTE_USER@$REMOTE_HOST" bash << EOF
  set -e

  echo "Checking for Docker..."
  if ! command -v docker &> /dev/null; then
    echo "Docker not found. Installing..."
    sudo apt update -y
    sudo apt install -y apt-transport-https ca-certificates curl software-properties-common
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
    sudo apt update -y
    sudo apt install -y docker-ce
    sudo systemctl start docker
    sudo systemctl enable docker
  fi

  echo "Docker is ready!"

  echo "Creating Docker volume for persistent storage..."
  sudo docker volume create $VOLUME_NAME

  echo "Running Minecraft server container..."
  sudo docker run -d -p $MC_PORT:25565 --name mc -v $VOLUME_NAME:/data $DOCKER_IMAGE

  echo "Minecraft server setup complete!"
EOF

# Return the server link
SERVER_IP=$(ssh "$REMOTE_USER@$REMOTE_HOST" "hostname -I | awk '{print \$1}'")
echo "Minecraft server is running! Connect using: ${SERVER_IP}:${MC_PORT}"
