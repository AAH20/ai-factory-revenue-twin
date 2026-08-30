from dataclasses import dataclass
from typing import Any


def positive(name: str, value: Any) -> float:
    number = float(value)
    if number <= 0:
        raise ValueError(f"{name} must be positive")
    return number


@dataclass(frozen=True)
class FactoryIntent:
    name: str
    gpu_count: int
    gpu_hour_cost: float
    monthly_platform_revenue: float
    target_useful_utilization: float
    minimum_contribution_margin: float
    target_nccl_busbw_gbps: float
    target_inference_p95_ms: float
    target_storage_gbps: float
    human_approval_required: bool = True

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> "FactoryIntent":
        utilization = float(value["target_useful_utilization"])
        margin = float(value["minimum_contribution_margin"])
        if not 0 < utilization <= 1 or not 0 < margin < 1:
            raise ValueError("utilization and margin must be fractional")
        return cls(
            name=str(value["name"]), gpu_count=int(positive("gpu_count", value["gpu_count"])),
            gpu_hour_cost=positive("gpu_hour_cost", value["gpu_hour_cost"]),
            monthly_platform_revenue=positive("monthly_platform_revenue", value["monthly_platform_revenue"]),
            target_useful_utilization=utilization, minimum_contribution_margin=margin,
            target_nccl_busbw_gbps=positive("target_nccl_busbw_gbps", value["target_nccl_busbw_gbps"]),
            target_inference_p95_ms=positive("target_inference_p95_ms", value["target_inference_p95_ms"]),
            target_storage_gbps=positive("target_storage_gbps", value["target_storage_gbps"]),
            human_approval_required=bool(value.get("human_approval_required", True)),
        )


@dataclass(frozen=True)
class TelemetryReplay:
    useful_gpu_utilization: float
    nccl_busbw_gbps: float
    inference_p95_ms: float
    storage_gbps: float
    roce_pfc_pause_rate: float
    ecn_mark_rate: float
    nvlink_degraded_links: int
    xid_errors: int
    cross_rack_job_fraction: float

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> "TelemetryReplay":
        return cls(**value)
