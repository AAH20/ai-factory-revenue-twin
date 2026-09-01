# Apache CloudStack and hybrid-cloud foundation

The platform separates portable decision logic from infrastructure-specific execution. Apache CloudStack with KVM is the primary open-source IaaS reference because it provides zones, pods, clusters, hosts, networks, storage and tenant APIs without requiring a proprietary public cloud.

## Platform boundaries

| Technology | Correct role | Evidence in this repository |
|---|---|---|
| Apache CloudStack | OSS IaaS control plane | placement catalog and Terraform network contract |
| KVM | production hypervisor for the OSS reference | CloudStack-KVM placement profile |
| VMware vSphere | licensed enterprise hypervisor option | CloudStack-VMware cost and placement profile |
| Proxmox VE | independent OSS virtualization or CloudStack 4.22 Extension target | both profiles evaluated; neither integration is claimed executed |
| VirtualBox | desktop development and contract testing | explicitly prohibited for production GPU claims |
| Docker / OCI | portable application packaging | non-root container image |
| Kubernetes | scheduling, services, quotas, disruption policy and GitOps | priority, quota and availability policies |
| Azure / AKS | proprietary managed-cloud option | placement profile and existing Azure evidence plane |
| AWS / EKS | proprietary managed-cloud option | provider-neutral placement profile |
| Google Cloud / GKE | proprietary managed-cloud option | provider-neutral placement profile |

## Automation layers

- Terraform/OpenTofu compiles CloudStack and multicloud infrastructure plans.
- Bicep remains the native Azure evidence-plane contract.
- Ansible captures network state and validates BGP/EVPN readiness before changes.
- Chef and Puppet demonstrate mutually selectable node configuration contracts; using both simultaneously on the same resource is not recommended.
- OPA/Rego blocks unreviewed changes, missing rollback evidence, residency mismatches and development virtualization in production.

## Production work still required

The Terraform contract needs a real zone and network offering. Network commands must be adapted and tested for each authorized vendor platform. Chef/Puppet packages and kernel settings need supported operating-system matrices. CloudStack, vSphere and Proxmox need API integration tests, secrets management and failure drills. Kubernetes GPU scheduling requires NVIDIA GPU Operator/DCGM plus a physical or authorized hosted GPU environment.

## Versioned source anchors

- Apache CloudStack 4.22.1 documents KVM host requirements and homogeneous host clusters: <https://docs.cloudstack.apache.org/en/4.22.1.0/installguide/hypervisor/kvm.html>
- CloudStack 4.22.1 release notes include configurable Proxmox Extension settings: <https://docs.cloudstack.apache.org/en/4.22.1.0/releasenotes/about.html>
- The current CloudStack Terraform provider is version 0.6.0: <https://registry.terraform.io/providers/cloudstack/cloudstack/latest>
- `ansible.netcommon.cli_command` requires the separately installed `ansible.netcommon` collection: <https://docs.ansible.com/projects/ansible/latest/collections/ansible/netcommon/cli_command_module.html>

Validated on 2026-09-01. Revalidate versions before deployment.
