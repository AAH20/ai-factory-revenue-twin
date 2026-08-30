import hashlib
import json
from dataclasses import asdict
from typing import Any

from .catalog import TOPOLOGIES
from .models import FactoryIntent, TelemetryReplay

HOURS_PER_MONTH = 730


def diagnose(intent: FactoryIntent, telemetry: TelemetryReplay) -> dict[str, Any]:
    signals = []
    if telemetry.nccl_busbw_gbps < intent.target_nccl_busbw_gbps: signals.append("collective_bandwidth_regression")
    if telemetry.roce_pfc_pause_rate > 0.02: signals.append("pfc_congestion")
    if telemetry.ecn_mark_rate > 0.05: signals.append("ecn_pressure")
    if telemetry.storage_gbps < intent.target_storage_gbps: signals.append("storage_starvation")
    if telemetry.inference_p95_ms > intent.target_inference_p95_ms: signals.append("inference_latency")
    if telemetry.nvlink_degraded_links: signals.append("nvlink_degradation")
    if telemetry.xid_errors: signals.append("gpu_xid_errors")
    hypotheses = []
    if {"collective_bandwidth_regression", "pfc_congestion"}.issubset(signals): hypotheses.append({"cause":"roce_congestion_and_cross_rack_placement","confidence":0.86})
    if "storage_starvation" in signals: hypotheses.append({"cause":"checkpoint_and_dataset_io_contention","confidence":0.72})
    if "nvlink_degradation" in signals or "gpu_xid_errors" in signals: hypotheses.append({"cause":"host_or_gpu_fabric_fault","confidence":0.68})
    return {"signals": signals, "ranked_hypotheses": hypotheses, "evidence_source":"versioned synthetic replay"}


def economics(intent: FactoryIntent, telemetry: TelemetryReplay, topology: dict[str, Any]) -> dict[str, Any]:
    gpu_capacity_cost = intent.gpu_count * intent.gpu_hour_cost * HOURS_PER_MONTH
    effective_gpu_equivalents = intent.gpu_count * telemetry.useful_gpu_utilization
    target_equivalents = intent.gpu_count * intent.target_useful_utilization
    capacity_gap = max(0.0, target_equivalents - effective_gpu_equivalents)
    capacity_deferral_value = capacity_gap * intent.gpu_hour_cost * HOURS_PER_MONTH
    monthly_delivery_cost = gpu_capacity_cost + topology["monthly_fabric_cost"]
    contribution = intent.monthly_platform_revenue - monthly_delivery_cost
    margin = contribution / intent.monthly_platform_revenue
    cost_per_useful_gpu_hour = monthly_delivery_cost / max(1, effective_gpu_equivalents * HOURS_PER_MONTH)
    return {
        "gpu_capacity_cost": round(gpu_capacity_cost,2), "fabric_cost": topology["monthly_fabric_cost"],
        "monthly_delivery_cost": round(monthly_delivery_cost,2), "monthly_contribution": round(contribution,2),
        "contribution_margin": round(margin,4), "useful_gpu_equivalents": round(effective_gpu_equivalents,2),
        "capacity_gap_gpu_equivalents": round(capacity_gap,2), "capacity_deferral_value": round(capacity_deferral_value,2),
        "cost_per_useful_gpu_hour": round(cost_per_useful_gpu_hour,2),
    }


def evaluate_topology(intent: FactoryIntent, telemetry: TelemetryReplay, topology: dict[str, Any]) -> dict[str, Any]:
    values = economics(intent, telemetry, topology)
    violations = []
    if topology["efficiency"] < intent.target_useful_utilization: violations.append("fabric_efficiency")
    if topology["estimated_nccl_busbw_gbps"] < intent.target_nccl_busbw_gbps: violations.append("collective_bandwidth")
    if values["contribution_margin"] < intent.minimum_contribution_margin: violations.append("contribution_margin")
    return {"topology": topology, "feasible": not violations, "violations": violations, "economics": values}


def route_models(diagnosis: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {"workflow":"telemetry_classification","route":"nemotron_nim","reason":"high-volume bounded private workload","status":"contract_only"},
        {"workflow":"cross_stack_diagnosis","route":"frontier_reasoning_escalation","reason":"ambiguous multi-system investigation","status":"provider-neutral contract"},
        {"workflow":"iac_and_collector_changes","route":"codex_class_engineering_agent","reason":"testable repository work","status":"provider-neutral contract"},
        {"workflow":"financial_and_promotion_decision","route":"deterministic_code","reason":"authority boundary","status":"executed"},
    ]


def compile_factory(intent: FactoryIntent, telemetry: TelemetryReplay) -> dict[str, Any]:
    diagnosis_result = diagnose(intent, telemetry)
    options = [evaluate_topology(intent, telemetry, topology) for topology in TOPOLOGIES]
    feasible = [item for item in options if item["feasible"]]
    selected = max(feasible, key=lambda item: (item["economics"]["contribution_margin"], item["topology"]["efficiency"])) if feasible else None
    remediation = {
        "actions":["reschedule_collective_workload_with_rack_affinity","validate_ecn_pfc_thresholds","isolate_checkpoint_io_window"],
        "blast_radius":"one workload queue and one leaf pair", "automatic_execution":False,
        "required_scenarios":["nccl_regression","leaf_failure","storage_contention","rollback"],
        "rollback":"restore scheduler policy and switch configuration revision",
        "expected_capacity_deferral_value": selected["economics"]["capacity_deferral_value"] if selected else 0,
    }
    payload = {"intent":asdict(intent),"telemetry":asdict(telemetry),"diagnosis":diagnosis_result,"topology_options":options,"selected":selected,"model_routes":route_models(diagnosis_result),"remediation":remediation}
    receipt = hashlib.sha256(json.dumps(payload,sort_keys=True,separators=(",",":")).encode()).hexdigest()
    return {"schema_version":"1.0",**payload,"promotion":{"receipt_sha256":receipt,"microbenchmarks":"required","digital_twin":"required","canary":"required","independent_approval":"required","automatic_production_execution":"prohibited"},"evidence_boundary":"Synthetic telemetry and reference economics are not DCGM, NCCL, InfiniBand, RoCE, NIM, GPU-cluster or customer measurements."}
