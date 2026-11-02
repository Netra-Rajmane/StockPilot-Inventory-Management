variable "aws_region" {
  description = "AWS region for the demo infrastructure"
  type        = string
  default     = "ap-south-1"
}

variable "project_name" {
  description = "Name used to tag resources"
  type        = string
  default     = "stockpilot-inventory"
}

variable "instance_type" {
  description = "EC2 instance type"
  type        = string
  default     = "t3.micro"
}

variable "allowed_ssh_cidr" {
  description = "Your public IP in CIDR format, for example 203.0.113.10/32. Keep the default to disable remote SSH access."
  type        = string
  default     = "127.0.0.1/32"
}
