#!/bin/bash
set -e

# 1. Update system
sudo dnf update -y

# 2. Install Docker
sudo dnf install -y docker

# 3. Start Docker service
sudo service docker start

# 4. Add user to docker group
sudo usermod -a -G docker ec2-user

# 5. Activate docker group
newgrp docker