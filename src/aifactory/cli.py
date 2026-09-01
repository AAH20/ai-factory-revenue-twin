import argparse,json
from pathlib import Path
from .compiler import compile_factory
from .models import FactoryIntent,TelemetryReplay
from .render import write_artifacts


def main():
    parser=argparse.ArgumentParser(description="Compile an AI factory topology, incident and economic decision")
    parser.add_argument("input",type=Path);parser.add_argument("--output",type=Path,default=Path("generated/latest"));args=parser.parse_args()
    data=json.loads(args.input.read_text());report=compile_factory(FactoryIntent.from_dict(data["factory_intent"]),TelemetryReplay.from_dict(data["telemetry_replay"]),data.get("infrastructure_foundation"),data.get("kpi_observations"));write_artifacts(report,args.output)
    print(json.dumps({"selected":report["selected"]["topology"]["id"] if report["selected"] else None,"receipt":report["promotion"]["receipt_sha256"]},indent=2))


if __name__=="__main__":main()
