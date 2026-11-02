
variable "project_name" {
  description = "Name of the StockPilot project"
  type        = string
  default     = "stockpilot-inventory"
}

variable "environment" {
  description = "Deployment environment"
  type        = string
  default     = "Local Development"
}

variable "application_port" {
  description = "Port used by the StockPilot application"
  type        = number
  default     = 5000
}
