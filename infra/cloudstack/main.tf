terraform {
  required_version = ">= 1.6"
  required_providers {
    cloudstack = { source = "cloudstack/cloudstack", version = "~> 0.6" }
  }
}

variable "zone" { type = string }
variable "network_offering" { type = string }
variable "cidr" { type = string; default = "10.42.0.0/20" }

resource "cloudstack_network" "ai_fabric" {
  name             = "ai-fabric-workload-network"
  cidr             = var.cidr
  network_offering = var.network_offering
  zone             = var.zone
}

output "ai_fabric_network_id" { value = cloudstack_network.ai_fabric.id }
