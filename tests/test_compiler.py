import unittest
from aifactory.compiler import compile_factory,diagnose
from aifactory.models import FactoryIntent,TelemetryReplay


def intent(**updates):
    value={"name":"factory","gpu_count":256,"gpu_hour_cost":3.5,"monthly_platform_revenue":1300000,"target_useful_utilization":.70,"minimum_contribution_margin":.30,"target_nccl_busbw_gbps":350,"target_inference_p95_ms":180,"target_storage_gbps":120};value.update(updates);return FactoryIntent.from_dict(value)
def replay(**updates):
    value={"useful_gpu_utilization":.55,"nccl_busbw_gbps":265,"inference_p95_ms":245,"storage_gbps":84,"roce_pfc_pause_rate":.071,"ecn_mark_rate":.13,"nvlink_degraded_links":1,"xid_errors":3,"cross_rack_job_fraction":.64};value.update(updates);return TelemetryReplay.from_dict(value)


class CompilerTests(unittest.TestCase):
    def test_selects_feasible_topology(self):
        report=compile_factory(intent(),replay());self.assertEqual(report["selected"]["topology"]["id"],"roce-1to1")
    def test_cross_stack_diagnosis(self):
        result=diagnose(intent(),replay());self.assertEqual(result["ranked_hypotheses"][0]["cause"],"roce_congestion_and_cross_rack_placement")
    def test_capacity_deferral_is_explicit(self):
        report=compile_factory(intent(),replay());self.assertEqual(report["selected"]["economics"]["capacity_deferral_value"],98112.0)
    def test_model_routing_keeps_authority_deterministic(self):
        report=compile_factory(intent(),replay());self.assertEqual(report["model_routes"][-1]["route"],"deterministic_code")
    def test_never_auto_executes(self):
        report=compile_factory(intent(),replay());self.assertFalse(report["remediation"]["automatic_execution"]);self.assertEqual(report["promotion"]["automatic_production_execution"],"prohibited")
    def test_receipt_deterministic(self):
        self.assertEqual(compile_factory(intent(),replay())["promotion"]["receipt_sha256"],compile_factory(intent(),replay())["promotion"]["receipt_sha256"])


if __name__=="__main__":unittest.main()
