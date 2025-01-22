terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
  backend "local" {}
}

provider "aws" {
  region = var.aws_region
}

# ------------------------------------------------------------------------------
# SECURITY GROUP
# ------------------------------------------------------------------------------
resource "aws_security_group" "minecraft_sg" {
  # Construct the name "userid_servername_server-sg"
  name        = "${var.user_id}_${var.server_name}_server-sg"
  description = "Security group for Minecraft server"

  ingress {
    description      = "Allow Minecraft traffic"
    from_port        = 25565
    to_port          = 25565
    protocol         = "tcp"
    cidr_blocks      = ["0.0.0.0/0"]
  }

  egress {
    description      = "Allow all outbound traffic"
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
  }
}

# ------------------------------------------------------------------------------
# EC2 INSTANCE
# ------------------------------------------------------------------------------
resource "aws_instance" "minecraft" {
  ami                    = "ami-0956b8dc6ddc445ec"
  instance_type          = var.instance_type
  vpc_security_group_ids = [aws_security_group.minecraft_sg.id]

  user_data = <<-EOF
    #!/bin/bash
    yum update -y
    # Install Java
    yum install -y java-1.8.0-openjdk

    # Create minecraft user and directories
    useradd minecraft
    mkdir /minecraft
    cd /minecraft

    # Download minecraft server jar
    wget https://launcher.mojang.com/v1/objects/66af10ecdf4bedebc3d31256f5d3bb3ac8ab5f3a/server.jar -O minecraft_server.jar
    
    # Accept EULA for Minecraft automatically
    echo "eula=true" > eula.txt
    
    # Start Minecraft server in the background
    nohup java -Xmx1G -Xms1G -jar minecraft_server.jar nogui > /minecraft/server.log 2>&1 &
  EOF

  # Construct the "Name" tag as "userid_servername_server"
  tags = {
    Name        = "${var.user_id}_${var.server_name}_server"
    User        = var.user_id
    Environment = "minecraft"
  }
}

# ------------------------------------------------------------------------------
# OUTPUTS
# ------------------------------------------------------------------------------
output "public_dns" {
  description = "The public DNS of the Minecraft server."
  value       = aws_instance.minecraft.public_dns
}

output "public_ip" {
  description = "The public IP of the Minecraft server."
  value       = aws_instance.minecraft.public_ip
}
