# Hybrid IaaS foundation decision

- Selected: **Apache CloudStack / KVM**
- Class: `oss-iaas`
- Monthly reference cost: **$325,795.20**
- Cost per GPU-hour: **$2.49**
- Receipt: `abcb7300b7ebe37dea2ec8ac6db96000bdc48e83ae187fce1ece54117654f255`

## Stack boundaries

- **Iaas Foundation:** Apache CloudStack with KVM is the primary OSS reference; VMware is a licensed hypervisor option
- **Alternative Virtualization:** Proxmox VE is evaluated both independently and as a CloudStack 4.22 Extension contract; neither path is claimed validated here
- **Development Virtualization:** VirtualBox is restricted to developer contract tests and is prohibited for production GPU claims
- **Containers:** Docker/OCI images provide portable packaging; Kubernetes provides scheduling, services, policy and GitOps reconciliation
- **Network Automation:** Ansible inventories and validates switches, routing, BGP/EVPN, VLAN/VXLAN, QoS and rollback
- **Configuration Management:** Chef and Puppet are supported configuration-state contracts; neither is misrepresented as the primary network controller
- **Iac:** Terraform/OpenTofu plus Bicep/provider modules; immutable plan, review, apply and rollback receipts
- **Compliance As Code:** OPA/Rego and IaC scanning map deployed resources to identity, segmentation, encryption, logging, residency and change controls

> Reference catalog and synthetic demand; no CloudStack, VMware, Proxmox, VirtualBox, Azure, AWS, GCP, Docker, Kubernetes, Ansible, Chef or Puppet environment was operated by this compiler run.
