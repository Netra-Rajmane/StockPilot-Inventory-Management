
output "project_name" {
  description = "StockPilot project name"
  value       = var.project_name
}

output "deployment_file" {
  description = "Path of the Terraform-created deployment file"
  value       = local_file.stockpilot_deployment.filename
}

output "application_port" {
  description = "Application port"
  value       = var.application_port
}

output "deployment_status" {
  description = "Local infrastructure deployment status"
  value       = "StockPilot local infrastructure provisioned successfully"
}
