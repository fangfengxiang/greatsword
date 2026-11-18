#!/usr/bin/env python3
"""Try free OpenCode models in ranked order, requiring BOTH A/B runs to succeed."""
import json, os, pathlib, subprocess, sys
root=pathlib.Path("/workspace")
out=pathlib.Path("/reports")
out.mkdir(parents=True,exist_ok=True)
# Editorial priority for engineering/coding decisions, NOT measured leaderboard scores.
priority=[
"opencode/deepseek-v4.1-flash-free",
"opencode/glm-5.3-flash-free",
"opencode/mimo-v2.6-flash-free",
"opencode/nemotron-3.5-super-vl-free",
"opencode/nemotron-3.5-lightning-free",
"opencode/flint-40b-free",
"opencode/beam-free",
"opencode/longcat-2.5-free",
"opencode/hy4-flash-free",
"opencode/inkling-2-small-free",
"opencode/iceman-free",
"opencode/big-pickle",
"opencode/jev-1.13-free",
]
def run(cmd,timeout):
    try:
        p=subprocess.run(cmd,cwd=root,text=True,capture_output=True,timeout=timeout)
        return {"exit":p.returncode,"stdout":p.stdout[-12000:],"stderr":p.stderr[-4000:]}
    except subprocess.TimeoutExpired:
        return {"exit":124,"stdout":"","stderr":"timeout"}
catalog=run(["opencode","models"],90)
available=set(catalog["stdout"].splitlines()) if catalog["exit"]==0 else set()
# Only known free models. The live catalog is an availability filter, not proof of free pricing.
candidates=[m for m in priority if m in available]
# Append newly appearing free-suffixed Zen models after curated priorities.
# Do not guess whether non-suffixed unknown models are free.
candidates += sorted(m for m in available if m.startswith("opencode/") and m.endswith("-free") and m not in candidates)
result={"status":"not_run","catalog_exit":catalog["exit"],"available_free_candidates":candidates,
        "ranking_basis":"editorial preference for coding, not a verified numerical benchmark",
        "attempts":[],"selected_model":None}
limit=os.getenv("EVAL_LIMIT","3")
timeout=os.getenv("EVAL_TIMEOUT","180")
for model in candidates:
    attempt={"model":model}
    for condition in ("baseline","greatsword"):
        cmd=["python3","evals/opencode/run.py","--model",model,"--condition",condition,
             "--limit",limit,"--timeout",timeout,"--output",str(out)]
        r=run(cmd,int(timeout)*int(limit)+60)
        attempt[condition]={"exit":r["exit"],"stderr":r["stderr"][-1500:]}
        if r["exit"]!=0: break
    result["attempts"].append(attempt)
    if attempt.get("baseline",{}).get("exit")==0 and attempt.get("greatsword",{}).get("exit")==0:
        result["selected_model"]=model
        result["status"]="completed_ungraded"
        break
(out/"model-selection.json").write_text(json.dumps(result,indent=2,ensure_ascii=False))
print(json.dumps(result,indent=2,ensure_ascii=False))
if result["status"]!="completed_ungraded":
    sys.exit(1)
