package aifactory.infrastructure

default allow := false

allow if {
  input.change.reviewed == true
  input.change.rollback_tested == true
  input.network.encrypted == true
  input.identity.least_privilege == true
  input.telemetry.enabled == true
  input.residency.actual == input.residency.required
}

deny contains "VirtualBox is development-only" if input.platform.virtualization == "VirtualBox"
deny contains "Production changes require rollback evidence" if input.change.rollback_tested != true
deny contains "Residency mismatch" if input.residency.actual != input.residency.required
