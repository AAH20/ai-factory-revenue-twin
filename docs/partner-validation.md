# Partner validation ladder

1. **Deterministic public proof:** run synthetic telemetry and economics locally.
2. **Collector dry-run:** validate schema, redaction and hashing against non-sensitive fixtures.
3. **Partner benchmark:** an authorized operator runs DCGM, NCCL and fabric collectors and returns a signed receipt.
4. **Digital-twin comparison:** compare predicted and partner-measured behavior without publishing topology secrets.
5. **Lab canary:** test the bounded change and rollback in a non-production cluster.
6. **Customer pilot:** operate only under explicit target scope, change authority and evidence-retention terms.

No stage inherits the claims of a later stage. A partner run must include hardware profile,
software versions, collector version, timestamps, metrics and artifact hashes.
