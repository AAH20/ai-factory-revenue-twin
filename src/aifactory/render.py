import json
from pathlib import Path


def write_artifacts(report, output: Path):
    output.mkdir(parents=True,exist_ok=True)
    (output/"factory-decision.json").write_text(json.dumps(report,indent=2)+"\n")
    selected=report["selected"]; econ=selected["economics"] if selected else {}
    text=f"""# AI Factory revenue and reliability decision

- Selected fabric: **{selected['topology']['name'] if selected else 'none'}**
- Monthly delivery cost: **${econ.get('monthly_delivery_cost',0):,.2f}**
- Contribution margin: **{econ.get('contribution_margin',0):.1%}**
- Useful GPU equivalents: **{econ.get('useful_gpu_equivalents',0):,.2f}**
- Capacity gap: **{econ.get('capacity_gap_gpu_equivalents',0):,.2f} GPU equivalents**
- Capacity deferral value: **${econ.get('capacity_deferral_value',0):,.2f}/month**
- Cost per useful GPU-hour: **${econ.get('cost_per_useful_gpu_hour',0):,.2f}**
- Receipt: `{report['promotion']['receipt_sha256']}`

## Diagnosis

Signals: {', '.join(report['diagnosis']['signals'])}

## Authority boundary

The remediation is a bounded proposal. Microbenchmarks, twin evaluation, canary, independent approval and rollback remain required. Automatic production execution is prohibited.

> {report['evidence_boundary']}
"""
    (output/"factory-decision.md").write_text(text)
    (output/"promotion-receipt.json").write_text(json.dumps({"receipt_sha256":report["promotion"]["receipt_sha256"],"promotion":report["promotion"]},indent=2)+"\n")
    if "infrastructure_foundation" in report:
        foundation=report["infrastructure_foundation"]
        (output/"infrastructure-foundation.json").write_text(json.dumps(foundation,indent=2)+"\n")
        f=foundation["selected"]
        lines=["# Hybrid IaaS foundation decision","",f"- Selected: **{f['platform']['control_plane']} / {f['platform']['virtualization']}**",f"- Class: `{f['platform']['class']}`",f"- Monthly reference cost: **${f['monthly_cost_usd']:,.2f}**",f"- Cost per GPU-hour: **${f['cost_per_gpu_hour_usd']:,.2f}**",f"- Receipt: `{foundation['receipt_sha256']}`","","## Stack boundaries",""]
        lines += [f"- **{key.replace('_',' ').title()}:** {value}" for key,value in foundation["stack"].items()]
        lines += ["","> "+foundation["evidence_boundary"],""]
        (output/"infrastructure-foundation.md").write_text("\n".join(lines))
        kpis=report["kpi_scorecard"]
        (output/"kpi-scorecard.json").write_text(json.dumps(kpis,indent=2)+"\n")
        k=["# AI Fabric Autopilot KPI scorecard","",f"**Decision:** `{kpis['decision']}`  ",f"**Attainment:** `{kpis['summary']['passed']}/{kpis['summary']['total']}` (`{kpis['summary']['attainment_pct']}%`)","","> "+kpis["claim_boundary"],""]
        for category in dict.fromkeys(x["category"] for x in kpis["metrics"]):
            k += [f"## {category.title()}","","| KPI | Value | Target | Result |","|---|---:|---:|---|"]
            for metric in (x for x in kpis["metrics"] if x["category"]==category):
                sign="≥" if metric["direction"]=="higher" else "≤"
                k.append(f"| {metric['name']} | {metric['value']} {metric['unit']} | {sign} {metric['target']} {metric['unit']} | {'PASS' if metric['passed'] else 'GAP'} |")
            k.append("")
        (output/"kpi-scorecard.md").write_text("\n".join(k))
