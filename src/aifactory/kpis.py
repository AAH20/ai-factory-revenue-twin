from __future__ import annotations

from typing import Any


def _k(name,category,value,unit,target,direction,evidence="synthetic replay"):
    passed=value>=target if direction=="higher" else value<=target
    return {"name":name,"category":category,"value":round(value,4),"unit":unit,"target":target,"direction":direction,"passed":passed,"evidence":evidence}


def scorecard(factory: dict[str,Any], foundation: dict[str,Any], observations: dict[str,Any]) -> dict[str,Any]:
    selected=factory["selected"]["economics"]; platform=foundation["selected"]
    metrics=[
      _k("monthly contribution","business",selected["monthly_contribution"],"USD",500000,"higher","modeled economics"),
      _k("contribution margin","business",selected["contribution_margin"]*100,"%",30,"higher","modeled economics"),
      _k("revenue per useful GPU hour","business",factory["intent"]["monthly_platform_revenue"]/(selected["useful_gpu_equivalents"]*730),"USD",8,"higher","modeled economics"),
      _k("capacity deferral value","business",selected["capacity_deferral_value"],"USD/month",50000,"higher","modeled economics"),
      _k("useful GPU utilization","capacity",factory["telemetry"]["useful_gpu_utilization"]*100,"%",factory["intent"]["target_useful_utilization"]*100,"higher"),
      _k("idle GPU capacity","capacity",100-factory["telemetry"]["useful_gpu_utilization"]*100,"%",20,"lower"),
      _k("GPU queue p95", "capacity",observations["gpu_queue_p95_minutes"],"minutes",10,"lower"),
      _k("capacity forecast error","capacity",observations["capacity_forecast_error_pct"],"%",10,"lower"),
      _k("NCCL bus bandwidth","network",factory["telemetry"]["nccl_busbw_gbps"],"Gbps",factory["intent"]["target_nccl_busbw_gbps"],"higher"),
      _k("inference latency p95","network",factory["telemetry"]["inference_p95_ms"],"ms",factory["intent"]["target_inference_p95_ms"],"lower"),
      _k("packet loss","network",observations["packet_loss_pct"],"%",.1,"lower"),
      _k("cross-rack workload fraction","network",factory["telemetry"]["cross_rack_job_fraction"]*100,"%",30,"lower"),
      _k("inference success","ai",observations["inference_success_pct"],"%",99.9,"higher"),
      _k("quality evaluation pass","ai",observations["quality_eval_pass_pct"],"%",95,"higher"),
      _k("cost per successful inference","ai",observations["cost_per_successful_inference_usd"],"USD",.01,"lower"),
      _k("availability","reliability",observations["availability_pct"],"%",99.9,"higher"),
      _k("MTTR","reliability",observations["mttr_minutes"],"minutes",30,"lower"),
      _k("automated recovery success","reliability",observations["automated_recovery_pct"],"%",90,"higher"),
      _k("foundation monthly cost","finops",platform["monthly_cost_usd"],"USD",observations["foundation_budget_usd"],"lower","reference catalog"),
      _k("cost per useful GPU hour","finops",selected["cost_per_useful_gpu_hour"],"USD",8,"lower","modeled economics"),
      _k("deployment frequency","delivery",observations["deployments_per_week"],"per week",5,"higher"),
      _k("change failure rate","delivery",observations["change_failure_pct"],"%",10,"lower"),
      _k("environment provisioning p95","delivery",observations["provisioning_p95_minutes"],"minutes",30,"lower"),
      _k("IaC coverage","automation",observations["iac_coverage_pct"],"%",100,"higher"),
      _k("network automation coverage","automation",observations["network_automation_pct"],"%",95,"higher"),
      _k("configuration compliance","automation",observations["configuration_compliance_pct"],"%",99,"higher"),
      _k("policy coverage","compliance",observations["policy_coverage_pct"],"%",100,"higher"),
      _k("evidence completeness","compliance",observations["evidence_completeness_pct"],"%",100,"higher"),
      _k("critical drift remediation","compliance",observations["critical_drift_mttr_minutes"],"minutes",60,"lower"),
      _k("energy per successful outcome","sustainability",observations["wh_per_successful_outcome"],"Wh",5,"lower"),
    ]
    hard={"no_autonomous_production":factory["promotion"]["automatic_production_execution"]=="prohibited",
          "evidence_complete":next(x for x in metrics if x["name"]=="evidence completeness")["passed"],
          "policy_complete":next(x for x in metrics if x["name"]=="policy coverage")["passed"]}
    attainment=sum(x["passed"] for x in metrics)/len(metrics)*100
    return {"schema_version":"aifactory/kpi/v1","summary":{"passed":sum(x["passed"] for x in metrics),"total":len(metrics),"attainment_pct":round(attainment,2)},
            "hard_gates":hard,"decision":"eligible-for-hardware-validation" if attainment>=80 and all(hard.values()) else "improve-before-hardware-validation",
            "metrics":metrics,"claim_boundary":"KPIs combine deterministic synthetic telemetry, reference catalog prices and disclosed modeled observations; they are not physical-cluster measurements."}
