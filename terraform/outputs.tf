output "instance_public_ip" {
  description = "Public IP of the demo EC2 instance"
  value       = aws_instance.app.public_ip
}

output "application_url" {
  description = "Application URL after you deploy the Docker container"
  value       = "http://${aws_instance.app.public_ip}:5000"
}

output "security_group_id" {
  value = aws_security_group.app.id
}
