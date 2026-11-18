#!/usr/bin/env python3
"""Run isolated OpenCode CLI A/B scenarios; emit inspectable JSON and HTML reports.

This is a real CLI runner, not an Inspect AI adapter. Agent results are not
automatically certified correct: rubrics require separate evaluation.
"""
import argparse, html, json, os, pathlib, shutil, subprocess, tempfile, time, hashlib
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parents[2]
DATA = ROOT / "evals/datasets/development.jsonl"
SKILL = ROOT / "skills/greatsword"
def main():
    p = argparse.ArgumentParser()
    p.add_argument("--model", required=True)
    p.add_argument("--condition", choices=["baseline", "greatsword"], required=True)
    p.add_argument("--limit", type=int, default=3)
    p.add_argument("--timeout", type=int, default=180)
    p.add_argument("--output", default="build/opencode")
    a = p.parse_args()
    if a.limit < 1 or a.limit > 12: p.error("--limit must be 1..12")
    if not shutil.which("opencode"): p.error("OpenCode CLI not installed")
    cases = [json.loads(x) for x in DATA.read_text().splitlines() if x.strip()][:a.limit]
    out = pathlib.Path(a.output).resolve() / a.condition
    out.mkdir(parents=True, exist_ok=True)
    records = []
    for case in cases:
        with tempfile.TemporaryDirectory(prefix="greatsword-eval-") as tmp:
            work = pathlib.Path(tmp)
            # No repository-root AGENTS.md or evaluation answers are present.
            if a.condition == "greatsword":
                dest = work / ".agents/skills/greatsword"
                shutil.copytree(SKILL, dest)
            prompt = case["prompt"] + "\n\nRespond with a concise engineering decision and proportionate verification. Do not modify files."
            cmd = ["opencode", "run", "--model", a.model, prompt]
            started = time.monotonic()
            try:
                cp = subprocess.run(cmd, cwd=work, text=True, capture_output=True, timeout=a.timeout,
                                    env={**os.environ, "CI": "true"})
                code, stdout, stderr = cp.returncode, cp.stdout, cp.stderr
            except subprocess.TimeoutExpired as e:
                code, stdout, stderr = 124, str(e.stdout or ""), "timeout"
            elapsed = round(time.monotonic() - started, 3)
            # No fake score: this is a transcript + execution metadata only.
            record = {"id":case["id"],"condition":a.condition,"model":a.model,
                      "exit_code":code,"elapsed_seconds":elapsed,
                      "response":stdout[-30000:],"stderr":stderr[-4000:],
                      "behavior_score":"not_graded"}
            records.append(record)
            (out / (case["id"]+".json")).write_text(json.dumps(record,ensure_ascii=False,indent=2))
    result={"schema_version":1,"timestamp":datetime.now(timezone.utc).isoformat(),
            "dataset_sha256":hashlib.sha256(DATA.read_bytes()).hexdigest(),
            "skill_sha256":hashlib.sha256((SKILL/"SKILL.md").read_bytes()).hexdigest(),
            "model":a.model,"condition":a.condition,"results":records}
    (out/"summary.json").write_text(json.dumps(result,ensure_ascii=False,indent=2))
    rows="".join("<tr><td>"+html.escape(r["id"])+"</td><td>"+str(r["exit_code"])+
        "</td><td>"+str(r["elapsed_seconds"])+"</td><td><pre>"+
        html.escape(r["response"][:5000])+"</pre></td></tr>" for r in records)
    (out/"report.html").write_text("<!doctype html><meta charset='utf-8'><title>Greatsword OpenCode Eval</title>"
        "<style>body{font:14px system-ui;max-width:1100px;margin:40px auto}table{border-collapse:collapse}"
        "td,th{border:1px solid #aaa;padding:8px;vertical-align:top}pre{white-space:pre-wrap;max-width:680px}</style>"
        "<h1>Greatsword OpenCode "+html.escape(a.condition)+"</h1><p>Model: "+html.escape(a.model)+
        " · Quality score: NOT GRADED</p><table><tr><th>Case</th><th>Exit</th><th>Seconds</th><th>Response</th></tr>"+
        rows+"</table>",encoding="utf-8")
    print(json.dumps({"condition":a.condition,"cases":len(records),"successful_cli_runs":sum(r["exit_code"]==0 for r in records),
                      "behavior_score":"not_graded","report":str(out/"report.html")}))
    if any(r["exit_code"] != 0 for r in records): raise SystemExit(1)
if __name__=="__main__": main()
