#!/usr/bin/env python3
"""Build a zero-dependency GitHub Pages landing page and per-run evidence pages."""
import html, json, os
from pathlib import Path
site=Path("public")
site.mkdir(exist_ok=True)
run=os.getenv("GITHUB_RUN_ID","local")
sha=os.getenv("GITHUB_SHA","unknown")
def read(path):
    p=Path(path)
    if not p.exists(): return None
    try: return json.loads(p.read_text())
    except (ValueError,OSError): return None
quality=read("build/quality-report.json") or {"status":"not_run"}
dataset=read("build/dataset-report.json") or {"status":"not_run"}
model=read("build/opencode/ci-report.json") or {"status":"not_run","selected_model":None}
attempts=model.get("attempted_models",[])
esc=lambda x:html.escape(str(x))
css="""<style>
:root{color-scheme:dark;--ink:#f1efe8;--muted:#a5adbb;--line:#30384a;--gold:#d6ad68;--bg:#080e19}
*{box-sizing:border-box}body{margin:0;background:radial-gradient(ellipse at 65% 0%,#1d2b44 0%,#080e19 60%);color:var(--ink);font:16px/1.7 system-ui,-apple-system,'PingFang SC',sans-serif}
a{color:#e7bf7d;text-decoration:none}a:hover{text-decoration:underline}.wrap{max-width:1100px;margin:auto;padding:30px 24px}
nav{display:flex;justify-content:space-between;align-items:center;gap:15px;border-bottom:1px solid var(--line);padding:0 0 22px}
.logo{font-size:20px;font-weight:900;letter-spacing:3px}.links{display:flex;gap:20px;flex-wrap:wrap}
.hero{padding:90px 0 70px;position:relative}.eyebrow{color:var(--gold);font-size:12px;letter-spacing:5px;font-weight:700}
h1{font-size:clamp(44px,8vw,94px);line-height:1.16;letter-spacing:3px;margin:22px 0;background:linear-gradient(120deg,#fff5d8,#d7a760 70%,#9a7144);color:transparent;background-clip:text}
.subtitle{font-size:clamp(19px,3vw,28px);font-weight:500;color:#e6e9f2;margin:0 0 24px}
.lead{max-width:740px;color:var(--muted);font-size:18px}
.actions{display:flex;gap:14px;flex-wrap:wrap;margin-top:32px}.btn{padding:12px 22px;border:1px solid #b38c54;border-radius:8px;background:#d8ae6b;color:#111827;font-weight:750}.btn.alt{background:transparent;color:#e7bf7d}
.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px;margin:28px 0 72px}
.panel{border:1px solid var(--line);background:#121b2bba;padding:26px;border-radius:14px}.panel h3{margin:0 0 12px;color:#f6d6a1}.panel p{margin:0;color:var(--muted)}
section{margin:70px 0}h2{font-size:28px;margin-bottom:18px}.muted,small{color:var(--muted)}
table{width:100%;border-collapse:collapse;display:block;overflow-x:auto}th,td{text-align:left;border-bottom:1px solid var(--line);padding:13px;white-space:nowrap}th{color:#d6ad68}
code{font:13px ui-monospace,SFMono-Regular,monospace;color:#efcb95}pre{background:#0a1220;padding:20px;overflow:auto;border:1px solid var(--line);border-radius:12px}
footer{border-top:1px solid var(--line);padding:35px 0;color:var(--muted)}
@media(max-width:700px){.grid{grid-template-columns:1fr}.hero{padding-top:55px}nav{align-items:flex-start;flex-direction:column}}
</style>"""
def page(title,body):
    return "<!doctype html><html lang='zh-CN'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>"+esc(title)+" · Greatsword</title><meta name='description' content='Greatsword — 重剑无锋，大巧不工。Evidence-grounded engineering judgment.'>"+css+"</head><body><div class='wrap'><nav><a class='logo' href='/greatsword/'>⚔ GREATSWORD</a><div class='links'><a href='/greatsword/'>首页</a><a href='/greatsword/reports/'>CI 测评报告</a><a href='https://github.com/fangfengxiang/greatsword'>GitHub</a></div></nav>"+body+"<footer>GREATSWORD · 重剑无锋，大巧不工。<br><small>Engineering decisions grounded in constraints, invariants, and evidence.</small></footer></div></body></html>"
landing="""<header class='hero'><div class='eyebrow'>AN ENGINEERING JUDGMENT SKILL</div><h1>重剑无锋，<br>大巧不工。</h1><p class='subtitle'>Greatsword · Engineering judgment, sharpened.</p><p class='lead'>不为复杂而复杂。让 Coding Agent 在架构设计、边界划分、正确性、兼容性与工程取舍中，先理解约束，再选择机制，最后用证据说话。</p><div class='actions'><a class='btn' href='https://github.com/fangfengxiang/greatsword/tree/main/skills/greatsword'>探索 Skill</a><a class='btn alt' href='/greatsword/reports/'>查看真实 CI 报告</a></div></header>
<div class='grid'><article class='panel'><h3>01 · 识其本</h3><p>问题、业务约束与真实瓶颈先于框架、算法和模式。</p></article><article class='panel'><h3>02 · 守其界</h3><p>明确职责归属、系统不变量、故障域和兼容契约。</p></article><article class='panel'><h3>03 · 证其行</h3><p>以最小充分的实验与回归验证决策，不以报告替代事实。</p></article></div>
<section><h2>一把重剑，六步决策</h2><p class='muted'>Problem → Constraints → Boundary → Mechanism → Failure → Evidence</p><div class='panel'>从需求与约束出发，定位权威边界，选择最小机制，审视失败路径，并给出与风险相称的验证。</div></section>
<section><h2>从工程实践中蒸馏</h2><p class='muted'>Greatsword 提炼架构、生命周期、协议兼容和受控变更等判断方式。公开 Skill 保持精炼，研究证据与评测场景分层维护。</p></section>
<section><h2>可检验，而不只可展示</h2><p class='muted'>每次 CI 区分静态检查、数据集检查、Docker 环境检查和同模型 A/B。尚未评分的行为质量不会被标记为通过。</p><a class='btn alt' href='/greatsword/reports/'>浏览每次 CI 证据</a></section>"""
(site/"index.html").write_text(page("重剑无锋，大巧不工",landing),encoding="utf-8")
(site/".nojekyll").write_text("")
reports=site/"reports";reports.mkdir(exist_ok=True)
# Public GitHub API lists workflow runs; published run files persist on gh-pages branch.
history="""<section><h1 style='font-size:clamp(35px,6vw,60px)'>CI · 测评档案</h1><p class='lead'>每次提交保留独立报告。静态质量、运行环境与同模型 A/B 分阶段展示；未执行与未评分如实标记。</p></section><section><h2>历史运行</h2><div id='history' class='panel'>正在从 GitHub Actions 读取运行记录…</div><p class='muted'>报告按 run ID 永久路径发布。GitHub Pages 首次启用前，链接可能尚不可访问。</p></section>
<script>
fetch('https://api.github.com/repos/fangfengxiang/greatsword/actions/workflows/quality.yml/runs?per_page=60')
.then(r=>{if(!r.ok)throw Error('GitHub API '+r.status);return r.json()})
.then(d=>{const rows=(d.workflow_runs||[]).map(r=>'<tr><td><a href="/greatsword/reports/'+r.id+'/">'+r.id+'</a></td><td>'+r.head_sha.slice(0,8)+'</td><td>'+r.created_at.slice(0,16).replace('T',' ')+'</td><td>'+r.status+' / '+(r.conclusion||'pending')+'</td><td><a href="'+r.html_url+'">Actions</a></td></tr>').join('');document.getElementById('history').innerHTML='<table><thead><tr><th>Run</th><th>Commit</th><th>UTC</th><th>Workflow</th><th>GitHub</th></tr></thead><tbody>'+rows+'</tbody></table>'})
.catch(e=>{document.getElementById('history').textContent='无法获取历史列表：'+e.message+'。可在 GitHub Actions 查看运行记录。'})
</script>"""
# A/B is published asynchronously on a separate branch. Fetch it at runtime with graceful fallback.
ab_widget="""<section><h2>最新模型 A/B（异步）</h2><div id='latest-ab' class='panel'><p>正在读取最新 A/B 结果…</p></div><p class='muted'>A/B 与静态站发布解耦；缺失、失败或未评分不会影响站点访问。</p></section>
<script>
(function(){
 const el=document.getElementById('latest-ab');
 const fallback='尚无可用 A/B 结果。静态质量报告仍可独立查看。';
 fetch('https://raw.githubusercontent.com/fangfengxiang/greatsword/ab-results/latest/ci-report.json',{cache:'no-store'})
 .then(r=>{if(!r.ok)throw Error('unavailable');return r.json()})
 .then(d=>{if(!d || typeof d.status!=='string')throw Error('invalid');const p=document.createElement('p');p.textContent='状态：'+d.status+' · 模型：'+(d.selected_model||'未选择')+' · 尝试：'+(Array.isArray(d.attempted_models)?d.attempted_models.length:0);el.replaceChildren(p);})
 .catch(()=>{el.textContent=fallback;});
})();
</script>"""
history=history.replace("</section><section><h2>历史运行</h2>","</section>"+ab_widget+"<section><h2>历史运行</h2>")
(reports/"index.html").write_text(page("CI 测评档案",history),encoding="utf-8")
current=reports/run;current.mkdir(parents=True,exist_ok=True)
rows=[("Skill 静态验证",quality.get("status")),("数据集验证",dataset.get("status")),("OpenCode Docker",model.get("docker_smoke","not_verified")),("同模型 A/B（异步，详见报告首页）",model.get("status")),("工程判断质量","not_graded")]
stages="".join("<tr><td>"+esc(k)+"</td><td>"+esc(v)+"</td></tr>" for k,v in rows)
tries="".join("<tr><td>"+esc(a.get("model"))+"</td><td>"+esc(a.get("baseline_exit"))+"</td><td>"+esc(a.get("greatsword_exit"))+"</td></tr>" for a in attempts)
body="<section><p class='eyebrow'>RUN "+esc(run)+"</p><h1 style='font-size:clamp(35px,6vw,62px)'>CI Evidence</h1><p class='lead'>Commit <code>"+esc(sha)+"</code></p><div class='panel'><h3>Selected Model</h3><p><code>"+esc(model.get("selected_model") or "NONE — no successful A/B")+" </code></p></div></section>"
body+="<section><h2>分阶段质量门禁</h2><table><tr><th>Stage</th><th>Status</th></tr>"+stages+"</table></section>"
body+="<section><h2>模型回退记录</h2><table><tr><th>Model</th><th>Baseline exit</th><th>Greatsword exit</th></tr>"+tries+"</table></section>"
body+="<section><h2>原始报告与可追溯数据</h2><p><a href='quality-report.json'>静态质量 JSON</a> · <a href='dataset-report.json'>数据集 JSON</a> · <a href='ci-report.json'>A/B JSON</a> · <a href='ci-report.html'>A/B HTML</a> · <a href='model-selection.json'>模型尝试 JSON</a></p><p class='muted'>CLI 成功只证明执行完成，不代表架构判断正确。行为评分未实施时明确标为 not_graded。</p></section>"
(current/"index.html").write_text(page("Run "+run,body),encoding="utf-8")
for source,target in [("build/quality-report.json","quality-report.json"),("build/dataset-report.json","dataset-report.json"),("build/opencode/ci-report.json","ci-report.json"),("build/opencode/ci-report.html","ci-report.html"),("build/opencode/model-selection.json","model-selection.json")]:
    p=Path(source)
    if p.exists(): (current/target).write_bytes(p.read_bytes())
print("Generated",current)
