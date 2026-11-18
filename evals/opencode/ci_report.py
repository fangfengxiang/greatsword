#!/usr/bin/env python3
"""Generate a truthful, standalone CI report even if no model evaluation ran."""
import html, json, os
from pathlib import Path
from datetime import datetime, timezone
root=Path("build/opencode")
root.mkdir(parents=True,exist_ok=True)
summaries={}
for condition in ("baseline","greatsword"):
    path=root/condition/"summary.json"
    if path.exists():
        summaries[condition]=json.loads(path.read_text())
has_both=len(summaries)==2
status="completed_ungraded" if has_both else "not_run"
report={"status":status,"timestamp":datetime.now(timezone.utc).isoformat(),
        "commit":os.getenv("GITHUB_SHA","unknown"),
        "docker_smoke":"passed" if os.getenv("DOCKER_SMOKE_PASSED")=="true" else "not_verified",
        "model_evaluation":status,
        "conditions":{k:{"model":v.get("model"),"cases":len(v.get("results",[])),
            "cli_successes":sum(x.get("exit_code")==0 for x in v.get("results",[])),
            "behavior_score":"not_graded"} for k,v in summaries.items()},
        "note":"A successful Docker smoke test is not a model evaluation. CLI success is not engineering correctness."}
(root/"ci-report.json").write_text(json.dumps(report,indent=2,ensure_ascii=False))
rows="".join("<tr><td>"+html.escape(k)+"</td><td>"+str(v["cases"])+"</td><td>"+str(v["cli_successes"])+"</td><td>not graded</td></tr>" for k,v in report["conditions"].items())
page="<!doctype html><meta charset='utf-8'><title>Greatsword CI Evaluation Report</title><style>body{font:16px system-ui;max-width:920px;margin:50px auto;line-height:1.5}td,th{border:1px solid #aaa;padding:12px}table{border-collapse:collapse}code{background:#eee;padding:3px}</style>"
page+="<h1>Greatsword CI Evaluation Report</h1><p>Commit: <code>"+html.escape(report["commit"])+"</code></p>"
page+="<p>Docker smoke: <b>"+html.escape(report["docker_smoke"])+"</b></p><p>Model evaluation: <b>"+html.escape(status)+"</b></p>"
page+="<p>Engineering correctness: <b>not graded</b></p>"
page+="<table><tr><th>Condition</th><th>Cases</th><th>CLI successes</th><th>Quality</th></tr>"+rows+"</table>"
if not has_both: page+="<p>No complete model A/B run was available. Configure the model input or OPENCODE_EVAL_MODEL repository variable and, where needed, OPENCODE_API_KEY secret.</p>"
(root/"ci-report.html").write_text(page,encoding="utf-8")
print(json.dumps(report,indent=2))
