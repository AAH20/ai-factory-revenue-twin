# AI Factory revenue and reliability decision

- Selected fabric: **Lossless Ethernet/RoCE 1:1**
- Monthly delivery cost: **$799,080.00**
- Contribution margin: **38.5%**
- Useful GPU equivalents: **140.80**
- Capacity gap: **38.40 GPU equivalents**
- Capacity deferral value: **$98,112.00/month**
- Cost per useful GPU-hour: **$7.77**
- Receipt: `2be35a054474df015d5fd1d4c17d4881c6d6902eec2b3676d70ec5977512b75e`

## Diagnosis

Signals: collective_bandwidth_regression, pfc_congestion, ecn_pressure, storage_starvation, inference_latency, nvlink_degradation, gpu_xid_errors

## Authority boundary

The remediation is a bounded proposal. Microbenchmarks, twin evaluation, canary, independent approval and rollback remain required. Automatic production execution is prohibited.

> Synthetic telemetry and reference economics are not DCGM, NCCL, InfiniBand, RoCE, NIM, GPU-cluster or customer measurements.
