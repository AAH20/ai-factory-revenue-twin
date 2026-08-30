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
