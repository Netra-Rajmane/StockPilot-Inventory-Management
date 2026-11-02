
resource "local_file" "stockpilot_deployment" {
  filename = "${path.module}/stockpilot-deployment.txt"

  content = <<-EOT
    StockPilot Inventory Management System
    ---------------------------------------
    Project: ${var.project_name}
    Environment: ${var.environment}
    Application: Flask
    Database: SQLite
    Containerization: Docker
    CI/CD: Jenkins
    Application Port: ${var.application_port}

    Infrastructure provisioned using Terraform.
  EOT

  file_permission = "0644"
}
