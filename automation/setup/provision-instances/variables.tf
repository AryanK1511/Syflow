variable "user_id" {
  type        = string
  description = "The ID of the user who requested the server."
}

variable "server_name" {
  type        = string
  default     = "MyMinecraftServer"
  description = "A descriptive name for the server."
}

variable "instance_type" {
  type        = string
  default     = "t2.micro"
  description = "AWS EC2 instance type."
}

variable "aws_region" {
  type        = string
  default     = "ca-central-1"
  description = "AWS region to deploy in."
}
