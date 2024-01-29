#!/bin/bash

# Update and Upgrade system
apt update -y
apt upgrade -y

# Install Docker Dependencies
apt install ca-certificates curl gnupg -y

# Add Docker official APT Repository
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
chmod a+r /etc/apt/keyrings/docker.gpg

# Add the Docker repository to the system’s package sources
echo \
"deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
"$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker
apt update -y
apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y

# Install Docker Compose
mkdir -p ~/.docker/cli-plugins/
curl -SL https://github.com/docker/compose/releases/download/v2.3.3/docker-compose-linux-x86_64 -o ~/.docker/cli-plugins/docker-compose
chmod +x ~/.docker/cli-plugins/docker-compose


# Install wg-easy
DOCKER_COMPOSE_FILE="docker-compose.yml"
WG_HOST=$(ip -4 address show eth0 | grep -oP '(?<=inet\s)\d+(\.\d+){3}')
WG_WEB_PORT="80"
WORKING_FOLDER="wg-easy"

# Create a new directory for the Docker Compose file
mkdir -p ~/$WORKING_FOLDER

# Generate the Docker Compose file
cat > ~/$WORKING_FOLDER/docker-compose.yml << EOF
version: "3.8"

services:
  wg-easy:
    environment:
      - WG_HOST=$WG_HOST
      - PASSWORD=$WG_PASSWORD
    image: ghcr.io/wg-easy/wg-easy
    container_name: wg-easy
    hostname: wg-easy
    volumes:
      - ~/.wg-easy:/etc/wireguard
    ports:
      - "51820:51820/udp"
      - "$WG_WEB_PORT:51821/tcp"
    restart: unless-stopped
    cap_add:
      - NET_ADMIN
      - SYS_MODULE
    sysctls:
      - net.ipv4.ip_forward=1
      - net.ipv4.conf.all.src_valid_mark=1
EOF

# Run the generated Docker Compose file
cd $WORKING_FOLDER
docker compose up -d
echo -e "wg-easy web starting on http://$WG_HOST:$WG_WEB_PORT"
