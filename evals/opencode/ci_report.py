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
selection_path=root/"model-selection.json"
selection=json.loads(selection_path.read_text()) if selection_path.exists() else {}
selected=selection.get("selected_model")
has_both=bool(selected) and len(summaries)==2 and all(v.get("model")==selected and v.get("results") and all(x.get("exit_code")==0 for x in v["results"]) for v in summaries.values())
status="completed_ungraded" if has_both else ("failed" if selection.get("attempts") else "not_run")
report={"status":status,"timestamp":datetime.now(timezone.utc).isoformat(),
        "commit":os.getenv("GITHUB_SHA","unknown"),
        "docker_smoke":"passed" if os.getenv("DOCKER_SMOKE_PASSED")=="true" else "not_verified",
        "model_evaluation":status,
        "selected_model":selected if has_both else None,
        "attempted_models":[{"model":a.get("model"),"baseline_exit":a.get("baseline",{}).get("exit"),"greatsword_exit":a.get("greatsword",{}).get("exit")} for a in selection.get("attempts",[])],
        "conditions":{k:{"model":v.get("model"),"cases":len(v.get("results",[])),
            "cli_successes":sum(x.get("exit_code")==0 for x in v.get("results",[])),
            "behavior_score":"not_graded"} for k,v in summaries.items()},
        "note":"A successful Docker smoke test is not a model evaluation. CLI success is not engineering correctness."}
(root/"ci-report.json").write_text(json.dumps(report,indent=2,ensure_ascii=False))
rows="".join("<tr><td>"+html.escape(k)+"</td><td>"+str(v["cases"])+"</td><td>"+str(v["cli_successes"])+"</td><td>not graded</td></tr>" for k,v in report["conditions"].items())
page="<!doctype html><meta charset='utf-8'><title>Greatsword CI Evaluation Report</title><style>body{font:16px system-ui;max-width:920px;margin:50px auto;line-height:1.5}td,th{border:1px solid #aaa;padding:12px}table{border-collapse:collapse}code{background:#eee;padding:3px}</style>"
page+="<h1>Greatsword CI Evaluation Report</h1><p>Commit: <code>"+html.escape(report["commit"])+"</code></p>"
page+="<p><strong>Selected model:</strong> <code>"+html.escape(selected if has_both else "NONE (no successful same-model A/B)")+"</code></p>"
page+="<p>Docker smoke: <b>"+html.escape(report["docker_smoke"])+"</b></p><p>Model evaluation: <b>"+html.escape(status)+"</b></p>"
page+="<p>Engineering correctness: <b>not graded</b></p>"
page+="<table><tr><th>Condition</th><th>Cases</th><th>CLI successes</th><th>Quality</th></tr>"+rows+"</table>"
if report["attempted_models"]:
    page+="<h2>Model attempts (priority order)</h2><table><tr><th>Model</th><th>Baseline exit</th><th>Greatsword exit</th></tr>"
    for a in report["attempted_models"]:
        page+="<tr><td>"+html.escape(str(a["model"]))+"</td><td>"+html.escape(str(a["baseline_exit"]))+"</td><td>"+html.escape(str(a["greatsword_exit"]))+"</td></tr>"
    page+="</table>"
if not has_both: page+="<p>No complete model A/B run was available. Configure the model input or OPENCODE_EVAL_MODEL repository variable and, where needed, OPENCODE_API_KEY secret.</p>"
(root/"ci-report.html").write_text(page,encoding="utf-8")
print(json.dumps(report,indent=2))
