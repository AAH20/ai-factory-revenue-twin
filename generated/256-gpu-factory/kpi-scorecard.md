# AI Fabric Autopilot KPI scorecard

**Decision:** `improve-before-hardware-validation`  
**Attainment:** `20/30` (`66.67%`)

> KPIs combine deterministic synthetic telemetry, reference catalog prices and disclosed modeled observations; they are not physical-cluster measurements.

## Business

| KPI | Value | Target | Result |
|---|---:|---:|---|
| monthly contribution | 500920.0 USD | ≥ 500000 USD | PASS |
| contribution margin | 38.53 % | ≥ 30 % | PASS |
| revenue per useful GPU hour | 12.6479 USD | ≥ 8 USD | PASS |
| capacity deferral value | 98112.0 USD/month | ≥ 50000 USD/month | PASS |

## Capacity

| KPI | Value | Target | Result |
|---|---:|---:|---|
| useful GPU utilization | 55.0 % | ≥ 70.0 % | GAP |
| idle GPU capacity | 45.0 % | ≤ 20 % | GAP |
| GPU queue p95 | 18 minutes | ≤ 10 minutes | GAP |
| capacity forecast error | 12 % | ≤ 10 % | GAP |

## Network

| KPI | Value | Target | Result |
|---|---:|---:|---|
| NCCL bus bandwidth | 265 Gbps | ≥ 350.0 Gbps | GAP |
| inference latency p95 | 245 ms | ≤ 180.0 ms | GAP |
| packet loss | 0.18 % | ≤ 0.1 % | GAP |
| cross-rack workload fraction | 64.0 % | ≤ 30 % | GAP |

## Ai

| KPI | Value | Target | Result |
|---|---:|---:|---|
| inference success | 99.7 % | ≥ 99.9 % | GAP |
| quality evaluation pass | 96 % | ≥ 95 % | PASS |
| cost per successful inference | 0.008 USD | ≤ 0.01 USD | PASS |

## Reliability

| KPI | Value | Target | Result |
|---|---:|---:|---|
| availability | 99.93 % | ≥ 99.9 % | PASS |
| MTTR | 26 minutes | ≤ 30 minutes | PASS |
| automated recovery success | 92 % | ≥ 90 % | PASS |

## Finops

| KPI | Value | Target | Result |
|---|---:|---:|---|
| foundation monthly cost | 325795.2 USD | ≤ 400000 USD | PASS |
| cost per useful GPU hour | 7.77 USD | ≤ 8 USD | PASS |

## Delivery

| KPI | Value | Target | Result |
|---|---:|---:|---|
| deployment frequency | 6 per week | ≥ 5 per week | PASS |
| change failure rate | 8 % | ≤ 10 % | PASS |
| environment provisioning p95 | 24 minutes | ≤ 30 minutes | PASS |

## Automation

| KPI | Value | Target | Result |
|---|---:|---:|---|
| IaC coverage | 100 % | ≥ 100 % | PASS |
| network automation coverage | 96 % | ≥ 95 % | PASS |
| configuration compliance | 98.5 % | ≥ 99 % | GAP |

## Compliance

| KPI | Value | Target | Result |
|---|---:|---:|---|
| policy coverage | 100 % | ≥ 100 % | PASS |
| evidence completeness | 100 % | ≥ 100 % | PASS |
| critical drift remediation | 48 minutes | ≤ 60 minutes | PASS |

## Sustainability

| KPI | Value | Target | Result |
|---|---:|---:|---|
| energy per successful outcome | 4.6 Wh | ≤ 5 Wh | PASS |
