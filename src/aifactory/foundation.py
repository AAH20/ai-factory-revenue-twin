from __future__ import annotations

import hashlib
import json
from typing import Any


PLATFORMS = [
    {"id":"cloudstack-kvm","control_plane":"Apache CloudStack","virtualization":"KVM","class":"oss-iaas","fixed_monthly":38000,"gpu_hour":2.20,"network_score":.88,"availability":.9995,"residency":"customer-controlled","automation":"Ansible + Terraform/OpenTofu"},
    {"id":"cloudstack-vmware","control_plane":"Apache CloudStack","virtualization":"VMware vSphere","class":"hybrid-iaas","fixed_monthly":69000,"gpu_hour":2.35,"network_score":.91,"availability":.9997,"residency":"customer-controlled","automation":"Ansible + Terraform"},
    {"id":"cloudstack-proxmox-extension","control_plane":"Apache CloudStack 4.22 Extension","virtualization":"Proxmox VE","class":"oss-extension-contract","fixed_monthly":35000,"gpu_hour":2.18,"network_score":.84,"availability":.9990,"residency":"customer-controlled","automation":"Ansible + Terraform/OpenTofu"},
    {"id":"proxmox-kvm","control_plane":"Proxmox VE","virtualization":"KVM/LXC","class":"oss-virtualization","fixed_monthly":31000,"gpu_hour":2.15,"network_score":.84,"availability":.9990,"residency":"customer-controlled","automation":"Ansible + OpenTofu"},
    {"id":"azure-aks","control_plane":"Microsoft Azure / AKS","virtualization":"managed cloud","class":"proprietary-cloud","fixed_monthly":12000,"gpu_hour":3.50,"network_score":.93,"availability":.9999,"residency":"provider-region","automation":"Bicep + Terraform + GitOps"},
    {"id":"aws-eks","control_plane":"AWS / EKS","virtualization":"managed cloud","class":"proprietary-cloud","fixed_monthly":13000,"gpu_hour":3.65,"network_score":.92,"availability":.9999,"residency":"provider-region","automation":"CloudFormation + Terraform + GitOps"},
    {"id":"gcp-gke","control_plane":"Google Cloud / GKE","virtualization":"managed cloud","class":"proprietary-cloud","fixed_monthly":12500,"gpu_hour":3.45,"network_score":.92,"availability":.9999,"residency":"provider-region","automation":"Terraform + Config Connector + GitOps"},
]


def compile_foundation(spec: dict[str, Any]) -> dict[str, Any]:
    required = {"gpu_count","monthly_gpu_hours","minimum_availability","minimum_network_score","maximum_monthly_cost","required_residency"}
    missing = required - spec.keys()
    if missing: raise ValueError("missing foundation fields: " + ", ".join(sorted(missing)))
    options=[]
    for platform in PLATFORMS:
        cost=platform["fixed_monthly"] + spec["monthly_gpu_hours"] * platform["gpu_hour"]
        violations=[]
        if platform["availability"] < spec["minimum_availability"]: violations.append("availability")
        if platform["network_score"] < spec["minimum_network_score"]: violations.append("network_score")
        if cost > spec["maximum_monthly_cost"]: violations.append("monthly_cost")
        if spec["required_residency"] == "customer-controlled" and platform["residency"] != "customer-controlled": violations.append("residency")
        score=platform["network_score"]*35 + platform["availability"]*20 + max(0,1-cost/spec["maximum_monthly_cost"])*45 - len(violations)*40
        options.append({"platform":platform,"monthly_cost_usd":round(cost,2),"cost_per_gpu_hour_usd":round(cost/spec["monthly_gpu_hours"],2),"feasible":not violations,"violations":violations,"score":round(score,2)})
    options.sort(key=lambda x:(x["feasible"],x["score"]),reverse=True)
    selected=options[0]
    stack={
        "iaas_foundation":"Apache CloudStack with KVM is the primary OSS reference; VMware is a licensed hypervisor option",
        "alternative_virtualization":"Proxmox VE is evaluated both independently and as a CloudStack 4.22 Extension contract; neither path is claimed validated here",
        "development_virtualization":"VirtualBox is restricted to developer contract tests and is prohibited for production GPU claims",
        "containers":"Docker/OCI images provide portable packaging; Kubernetes provides scheduling, services, policy and GitOps reconciliation",
        "network_automation":"Ansible inventories and validates switches, routing, BGP/EVPN, VLAN/VXLAN, QoS and rollback",
        "configuration_management":"Chef and Puppet are supported configuration-state contracts; neither is misrepresented as the primary network controller",
        "iac":"Terraform/OpenTofu plus Bicep/provider modules; immutable plan, review, apply and rollback receipts",
        "compliance_as_code":"OPA/Rego and IaC scanning map deployed resources to identity, segmentation, encryption, logging, residency and change controls",
    }
    result={"schema_version":"aifactory/foundation/v1","selected":selected,"options":options,"stack":stack,
            "production_execution":"disabled","evidence_boundary":"Reference catalog and synthetic demand; no CloudStack, VMware, Proxmox, VirtualBox, Azure, AWS, GCP, Docker, Kubernetes, Ansible, Chef or Puppet environment was operated by this compiler run."}
    result["receipt_sha256"]=hashlib.sha256(json.dumps(result,sort_keys=True,separators=(",",":")).encode()).hexdigest()
    return result
