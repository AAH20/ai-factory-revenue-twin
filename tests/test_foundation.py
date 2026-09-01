import json
import unittest
from pathlib import Path

from aifactory.compiler import compile_factory
from aifactory.foundation import compile_foundation
from aifactory.models import FactoryIntent, TelemetryReplay


def fixture():
    raw=json.loads(Path("examples/256-gpu-factory.json").read_text())
    return raw,compile_factory(FactoryIntent.from_dict(raw["factory_intent"]),TelemetryReplay.from_dict(raw["telemetry_replay"]),raw["infrastructure_foundation"],raw["kpi_observations"])


class FoundationTests(unittest.TestCase):
    def test_selects_cloudstack_kvm_for_customer_controlled_constraint(self):
        _,report=fixture();self.assertEqual(report["infrastructure_foundation"]["selected"]["platform"]["id"],"cloudstack-kvm")

    def test_proprietary_cloud_fails_customer_residency_gate(self):
        raw,_=fixture();result=compile_foundation(raw["infrastructure_foundation"])
        azure=next(x for x in result["options"] if x["platform"]["id"]=="azure-aks")
        self.assertIn("residency",azure["violations"])

    def test_virtualbox_is_development_only(self):
        _,report=fixture();self.assertIn("prohibited for production",report["infrastructure_foundation"]["stack"]["development_virtualization"])

    def test_kpis_cover_ten_categories_and_retain_gaps(self):
        _,report=fixture();score=report["kpi_scorecard"]
        self.assertEqual(len(score["metrics"]),30)
        self.assertGreaterEqual(len({x["category"] for x in score["metrics"]}),10)
        self.assertTrue(any(not x["passed"] for x in score["metrics"]))

    def test_hard_gates_do_not_average_away(self):
        raw,_=fixture();raw["kpi_observations"]["evidence_completeness_pct"]=99
        report=compile_factory(FactoryIntent.from_dict(raw["factory_intent"]),TelemetryReplay.from_dict(raw["telemetry_replay"]),raw["infrastructure_foundation"],raw["kpi_observations"])
        self.assertEqual(report["kpi_scorecard"]["decision"],"improve-before-hardware-validation")


if __name__=="__main__": unittest.main()
