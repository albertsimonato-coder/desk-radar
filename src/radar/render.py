"""Render docs/index.html (all openings) and docs/new.html (new only) from the store.

Both pages are one self-contained HTML file with the data embedded as JSON and share one
template; `mode` switches the default filters and the header copy.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime, timedelta
from pathlib import Path

from radar.models import Opening
from radar.store import Store


def _iso(dt: datetime | None) -> str | None:
    return dt.astimezone(UTC).isoformat(timespec="seconds") if dt else None


def is_new(o: Opening, now: datetime, window_days: int) -> bool:
    return (
        o.status == "open" and o.reopened == 0 and o.first_seen >= now - timedelta(days=window_days)
    )


def opening_to_row(o: Opening, last_run_id: int | None, now: datetime, window_days: int) -> dict:
    return {
        "k": o.dedup_key,
        "company": o.company_name,
        "slug": o.company_slug,
        "group": o.group,
        "priority": o.priority,
        "title": o.title,
        "city": o.city or "",
        "country": o.country or "",
        "loc": o.location_raw,
        "dept": o.department,
        "type": o.employment_type,
        "fn": o.function,
        "fit": o.fit_score,
        "bd": o.score_breakdown.model_dump(),
        "posted": _iso(o.posted_at),
        "first": _iso(o.first_seen),
        "last": _iso(o.last_seen),
        "status": o.status,
        "url": o.url,
        "new": is_new(o, now, window_days),
        "new_run": bool(last_run_id)
        and o.first_run_id == last_run_id
        and o.status == "open"
        and o.reopened == 0,
        "reopened": o.reopened,
        "by": o.classified_by,
    }


def build_payload(store: Store, profile: dict, now: datetime | None = None) -> dict:
    now = now or datetime.now(UTC)
    window = int(profile.get("new_window_days", 7))
    last = store.last_run()
    last_run_id = int(last["run_id"]) if last else None
    openings = store.all_openings()
    rows = [opening_to_row(o, last_run_id, now, window) for o in openings]
    counts = {
        "total": len(rows),
        "open": sum(1 for r in rows if r["status"] == "open"),
        "closed": sum(1 for r in rows if r["status"] == "closed"),
        "new": sum(1 for r in rows if r["new"]),
        "new_run": sum(1 for r in rows if r["new_run"]),
    }
    return {
        "generated_at": _iso(now),
        "last_run": dict(last) if last else None,
        "window_days": window,
        "counts": counts,
        "health": store.source_health(),
        "rows": rows,
    }


def render_pages(store: Store, profile: dict, docs_dir: str | Path = "docs") -> tuple[Path, Path]:
    docs = Path(docs_dir)
    docs.mkdir(parents=True, exist_ok=True)
    payload = build_payload(store, profile)
    all_page = docs / "index.html"
    new_page = docs / "new.html"
    all_page.write_text(render_html(payload, mode="all"), encoding="utf-8")
    new_payload = dict(payload)
    new_payload["rows"] = [r for r in payload["rows"] if r["new"] or r["new_run"]]
    new_page.write_text(render_html(new_payload, mode="new"), encoding="utf-8")
    return all_page, new_page


def render_html(payload: dict, mode: str) -> str:
    data = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    title = "Desk Radar · All openings" if mode == "all" else "Desk Radar · New openings"
    return TEMPLATE.replace("__TITLE__", title).replace("__MODE__", mode).replace("__DATA__", data)


TEMPLATE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__</title>
<style>
:root{--bg:#f7f7f8;--fg:#1b1b1f;--muted:#6b6b76;--card:#fff;--line:#e2e2e8;--accent:#0b57d0;--accent-fg:#fff;--chip:#eef0f4;--ok:#1a7f37;--warn:#b35c00;--bad:#c0392b;--closed:#9a9aa5}
@media (prefers-color-scheme:dark){:root{--bg:#121216;--fg:#e8e8ee;--muted:#9a9aa8;--card:#1b1b22;--line:#2b2b35;--accent:#7cacf8;--accent-fg:#0b1b36;--chip:#262632;--ok:#3fb950;--warn:#e3a008;--bad:#f05252;--closed:#6b6b78}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font:14px/1.45 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
a{color:var(--accent)}
header{padding:16px;border-bottom:1px solid var(--line);background:var(--card)}
.top{display:flex;flex-wrap:wrap;gap:12px;align-items:baseline;justify-content:space-between}
h1{font-size:20px;margin:0}
h1 small{font-weight:400;color:var(--muted);font-size:13px;margin-left:8px}
nav a{margin-left:10px;font-weight:600}
nav a.cur{color:var(--fg);text-decoration:none;border-bottom:2px solid var(--accent)}
.meta{color:var(--muted);font-size:13px;margin-top:6px;display:flex;flex-wrap:wrap;gap:14px}
.meta b{color:var(--fg)}
details.health{margin-top:8px;font-size:13px}
details.health summary{cursor:pointer;color:var(--muted)}
details.health table{margin-top:8px;font-size:12px}
.filters{display:flex;flex-wrap:wrap;gap:8px;padding:12px 16px;align-items:center}
.filters select,.filters input{font:inherit;padding:6px 8px;border:1px solid var(--line);border-radius:6px;background:var(--card);color:var(--fg);max-width:100%}
.filters input[type=search]{min-width:200px;flex:1}
.filters label{display:flex;align-items:center;gap:6px;color:var(--muted);font-size:13px}
.filters .seg{display:inline-flex;border:1px solid var(--line);border-radius:6px;overflow:hidden}
.filters .seg button{font:inherit;padding:6px 10px;border:0;background:var(--card);color:var(--fg);cursor:pointer}
.filters .seg button.on{background:var(--accent);color:var(--accent-fg)}
.filters button.reset{font:inherit;padding:6px 10px;border:1px solid var(--line);border-radius:6px;background:var(--card);color:var(--fg);cursor:pointer}
.count{padding:0 16px 8px;color:var(--muted);font-size:13px}
.wrap{overflow-x:auto;padding:0 16px 32px}
table{border-collapse:collapse;width:100%;background:var(--card);border:1px solid var(--line);border-radius:8px}
th,td{padding:8px 10px;text-align:left;border-bottom:1px solid var(--line);vertical-align:top}
th{position:sticky;top:0;background:var(--card);cursor:pointer;user-select:none;white-space:nowrap;font-size:12px;color:var(--muted);text-transform:uppercase;letter-spacing:.03em}
th.sorted{color:var(--fg)}
tr.closed td{color:var(--closed)}
tr.closed td a{color:var(--closed)}
td.title{min-width:260px}
td.title .dept{display:block;color:var(--muted);font-size:12px}
.chip{display:inline-block;padding:2px 7px;border-radius:999px;background:var(--chip);font-size:12px;white-space:nowrap}
.chip.new{background:var(--ok);color:#fff}
.chip.run{background:var(--accent);color:var(--accent-fg)}
.chip.closed{background:var(--closed);color:#fff}
.chip.re{background:var(--warn);color:#fff}
.fit{font-weight:700;font-variant-numeric:tabular-nums;cursor:help}
.fit.hi{color:var(--ok)}.fit.mid{color:var(--warn)}.fit.lo{color:var(--muted)}
td.num{font-variant-numeric:tabular-nums;white-space:nowrap}
.empty{padding:40px;text-align:center;color:var(--muted)}
.ok{color:var(--ok)}.bad{color:var(--bad)}
@media (max-width:720px){
  .wrap{padding:0 8px 32px}
  table,thead,tbody,tr,td{display:block}
  thead{display:none}
  tr{border-bottom:1px solid var(--line);padding:8px 4px}
  td{border:0;padding:2px 4px}
  td:before{content:attr(data-l);color:var(--muted);font-size:11px;text-transform:uppercase;margin-right:6px}
  td.title:before{display:none}
  td.title{font-weight:600}
}
</style>
</head>
<body>
<header>
  <div class="top">
    <h1>Desk Radar <small id="pagename"></small></h1>
    <nav><a href="index.html" id="nav-all">All openings</a><a href="new.html" id="nav-new">New openings</a></nav>
  </div>
  <div class="meta" id="meta"></div>
  <details class="health"><summary>Source health</summary><div id="health"></div></details>
</header>
<div class="filters" id="filters">
  <input type="search" id="q" placeholder="Search title, company, location…">
  <select id="f-country"><option value="">Country</option></select>
  <select id="f-city"><option value="">City</option></select>
  <select id="f-type"><option value="">Type</option></select>
  <select id="f-fn"><option value="">Function</option></select>
  <select id="f-group"><option value="">Group</option></select>
  <select id="f-prio"><option value="">Priority</option><option value="1">P1</option><option value="2">P2</option></select>
  <label>Min fit <input type="number" id="f-fit" min="0" max="100" step="5" value="0" style="width:64px"></label>
  <span id="mode-controls"></span>
  <button class="reset" id="reset">Reset</button>
</div>
<div class="count" id="count"></div>
<div class="wrap"><table id="t"><thead><tr>
  <th data-k="company">Company</th><th data-k="title">Title</th><th data-k="city">City</th>
  <th data-k="type">Type</th><th data-k="fn">Function</th><th data-k="fit">Fit</th>
  <th data-k="posted">Posted</th><th data-k="first">First seen</th><th data-k="status">Status</th><th>Link</th>
</tr></thead><tbody id="tb"></tbody></table><div class="empty" id="empty" hidden>No openings match.</div></div>
<script id="data" type="application/json">__DATA__</script>
<script>
(function(){
const MODE="__MODE__";
const D=JSON.parse(document.getElementById('data').textContent);
const $=s=>document.querySelector(s);
const esc=s=>String(s==null?'':s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const fmtD=s=>s?s.slice(0,10):'';
const fmtT=s=>s?s.replace('T',' ').slice(0,16)+' UTC':'—';
const LBL={type:{graduate:'Graduate',internship:'Internship',offcycle:'Off-cycle',analyst_junior:'Analyst / Junior',experienced:'Experienced',other:'Other'},
 fn:{sales_trading:'Sales & Trading',commodities:'Commodities',market_making:'Market making',quant:'Quant',market_risk:'Market risk',treasury:'Treasury',ibd:'IBD',advisory_valuation:'Advisory / Valuation',asset_management:'Asset mgmt',operations:'Operations',technology:'Technology',other:'Other'}};
const lbl=(k,v)=>(LBL[k]&&LBL[k][v])||v;
$('#pagename').textContent=MODE==='all'?'All openings':'New openings';
$('#nav-'+MODE).classList.add('cur');
const lr=D.last_run;
$('#meta').innerHTML=`<span>Last run: <b>${lr?fmtT(lr.finished_at):'never'}</b>${lr?` (run #${lr.run_id}, ${lr.tier}, ${lr.sources_ok}/${lr.sources_total} sources ok)`:''}</span>
 <span>Total <b>${D.counts.total}</b></span><span>Open <b>${D.counts.open}</b></span><span>Closed <b>${D.counts.closed}</b></span>
 <span>New (${D.window_days}d) <b>${D.counts.new}</b></span><span>New since last run <b>${D.counts.new_run}</b></span>`;
$('#health').innerHTML=D.health.length?`<table><thead><tr><th>Source</th><th>ATS</th><th>Last success</th><th>Count</th><th>Last error</th></tr></thead><tbody>`+
 D.health.map(h=>`<tr><td>${esc(h.company_name)}</td><td>${esc(h.ats)}</td><td class="${h.consecutive_failures?'bad':'ok'}">${esc(fmtT(h.last_success))}</td><td>${h.last_count??''}</td><td>${h.consecutive_failures?esc((h.last_error||'').slice(0,120))+' ('+esc(fmtT(h.last_error_at))+')':''}</td></tr>`).join('')+'</tbody></table>':'<p>No sources recorded yet.</p>';
// mode-specific controls
let includeClosed=false, newMode='window';
const mc=$('#mode-controls');
if(MODE==='all'){mc.innerHTML=`<label><input type="checkbox" id="closed"> include closed</label>`;mc.querySelector('#closed').onchange=e=>{includeClosed=e.target.checked;draw()};}
else{mc.innerHTML=`<span class="seg"><button data-m="window" class="on">New in last ${D.window_days} days</button><button data-m="run">New since last run</button></span>`;
 mc.querySelectorAll('button').forEach(b=>b.onclick=()=>{newMode=b.dataset.m;mc.querySelectorAll('button').forEach(x=>x.classList.toggle('on',x===b));draw()});}
// filters
const uniq=(k)=>[...new Set(D.rows.map(r=>r[k]).filter(Boolean))].sort();
function fill(sel,vals,k){const s=$(sel);vals.forEach(v=>{const o=document.createElement('option');o.value=v;o.textContent=k?lbl(k,v):v;s.appendChild(o)})}
fill('#f-country',uniq('country'));fill('#f-city',uniq('city'));fill('#f-type',uniq('type'),'type');fill('#f-fn',uniq('fn'),'fn');fill('#f-group',uniq('group'));
let sort={k:'fit',dir:-1};
document.querySelectorAll('th[data-k]').forEach(th=>th.onclick=()=>{const k=th.dataset.k;if(sort.k===k)sort.dir=-sort.dir;else sort={k,dir:(k==='fit'||k==='posted'||k==='first')?-1:1};draw()});
document.querySelectorAll('#filters input,#filters select').forEach(el=>el.addEventListener('input',draw));
$('#reset').onclick=()=>{document.querySelectorAll('#filters select').forEach(s=>s.value='');$('#q').value='';$('#f-fit').value=0;draw()};
function bdTitle(r){const b=r.bd||{};return `city ${b.city} · type ${b.employment_type} · function ${b.function} · keywords ${b.keywords}${(b.keyword_hits||[]).length?' ['+b.keyword_hits.join(', ')+']':''} · recency ${b.recency}`}
function draw(){
 const q=$('#q').value.trim().toLowerCase(),co=$('#f-country').value,ci=$('#f-city').value,ty=$('#f-type').value,fn=$('#f-fn').value,gr=$('#f-group').value,pr=$('#f-prio').value,mf=+$('#f-fit').value||0;
 let rows=D.rows.filter(r=>{
  if(MODE==='all'){if(!includeClosed&&r.status!=='open')return false;}
  else{if(newMode==='window'?!r.new:!r.new_run)return false;}
  if(co&&r.country!==co)return false;if(ci&&r.city!==ci)return false;if(ty&&r.type!==ty)return false;if(fn&&r.fn!==fn)return false;if(gr&&r.group!==gr)return false;if(pr&&String(r.priority)!==pr)return false;
  if(r.fit<mf)return false;
  if(q){const hay=(r.title+' '+r.company+' '+r.loc+' '+r.dept+' '+r.city).toLowerCase();if(!hay.includes(q))return false;}
  return true;});
 rows.sort((a,b)=>{const k=sort.k;let va=a[k]??'',vb=b[k]??'';if(typeof va==='string'){va=va.toLowerCase();vb=vb.toLowerCase();}
  let c=va<vb?-1:va>vb?1:0;if(c===0&&k!=='fit'){c=b.fit-a.fit;}if(c===0&&k!=='first'){c=(b.first||'')<(a.first||'')?-1:(b.first||'')>(a.first||'')?1:0;}return c*sort.dir;});
 document.querySelectorAll('th[data-k]').forEach(th=>{th.classList.toggle('sorted',th.dataset.k===sort.k);th.textContent=th.textContent.replace(/ [▲▼]$/,'')+(th.dataset.k===sort.k?(sort.dir<0?' ▼':' ▲'):'')});
 $('#count').textContent=`${rows.length} of ${D.rows.length} shown`;
 $('#empty').hidden=rows.length>0;
 $('#tb').innerHTML=rows.map(r=>`<tr class="${r.status}">
  <td data-l="Company">${esc(r.company)} <span class="chip">P${r.priority}</span></td>
  <td class="title" data-l="Title">${esc(r.title)}${r.new_run?' <span class="chip run">new</span>':r.new?' <span class="chip new">new</span>':''}${r.reopened?' <span class="chip re">reopened</span>':''}<span class="dept">${esc(r.dept||r.loc)}</span></td>
  <td data-l="City" title="${esc(r.loc)}">${esc(r.city||r.loc||'—')}${r.country?' <span class="chip">'+esc(r.country)+'</span>':''}</td>
  <td data-l="Type">${esc(lbl('type',r.type))}</td>
  <td data-l="Function">${esc(lbl('fn',r.fn))}</td>
  <td data-l="Fit" class="num"><span class="fit ${r.fit>=70?'hi':r.fit>=45?'mid':'lo'}" title="${esc(bdTitle(r))}">${Math.round(r.fit)}</span></td>
  <td data-l="Posted" class="num">${fmtD(r.posted)||'—'}</td>
  <td data-l="First seen" class="num">${fmtD(r.first)}</td>
  <td data-l="Status"><span class="chip ${r.status}">${r.status}</span></td>
  <td data-l="Link"><a href="${esc(r.url)}" target="_blank" rel="noopener">open ↗</a></td></tr>`).join('');
}
draw();
})();
</script>
</body>
</html>
"""
