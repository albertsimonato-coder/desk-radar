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
[hidden]{display:none!important}
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
nav a .n{display:inline-block;min-width:18px;padding:0 5px;border-radius:999px;background:var(--accent);color:var(--accent-fg);font-size:11px;text-align:center;vertical-align:1px}
button.star{font:inherit;font-size:12px;padding:3px 8px;border:1px solid var(--line);border-radius:999px;background:var(--card);color:var(--fg);cursor:pointer;white-space:nowrap}
button.star.on{background:var(--accent);color:var(--accent-fg);border-color:var(--accent)}
tr.saved td:first-child{box-shadow:inset 3px 0 0 var(--accent)}
tr.swiping{background:color-mix(in srgb,var(--accent) 12%,var(--card));transition:none}
tr.will{background:color-mix(in srgb,var(--accent) 28%,var(--card))}
#savedwrap{padding:0 16px 32px}
.sbar{display:flex;flex-wrap:wrap;gap:8px;align-items:center;padding:12px 0;color:var(--muted);font-size:13px}
.sbar button,.card button{font:inherit;font-size:13px;padding:6px 10px;border:1px solid var(--line);border-radius:6px;background:var(--card);color:var(--fg);cursor:pointer}
.sbar .sp{flex:1}
.card{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:10px 12px;margin-bottom:8px;display:grid;grid-template-columns:150px 1fr auto;gap:6px 12px;align-items:start}
.card .sub{color:var(--muted);font-size:12px;margin-top:2px}
.card .fields{display:flex;flex-wrap:wrap;gap:8px;margin-top:8px;align-items:center}
.card .fields label{display:flex;align-items:center;gap:6px;color:var(--muted);font-size:12px}
.card input,.card select{font:inherit;font-size:13px;padding:5px 8px;border:1px solid var(--line);border-radius:6px;background:var(--bg);color:var(--fg)}
.card input[type=text]{flex:1;min-width:180px}
.card.applied,.card.interview,.card.offer{box-shadow:inset 3px 0 0 var(--ok)}
.card.rejected,.card.dropped{opacity:.6}
.card .fit{cursor:default}
.shead{margin:16px 0 8px;font-size:13px;color:var(--muted);text-transform:uppercase;letter-spacing:.03em}
#toast{position:fixed;left:50%;bottom:24px;transform:translateX(-50%);background:var(--fg);color:var(--bg);padding:8px 14px;border-radius:999px;font-size:13px;opacity:0;transition:opacity .2s;pointer-events:none;z-index:9}
#toast.show{opacity:1}
@media (max-width:720px){
  .card{grid-template-columns:1fr}
  #savedwrap{padding:0 8px 32px}
  td.save:before{display:none}
  td.save{padding-top:6px}
  .wrap{padding:0 8px 32px}
  table,thead,tbody,tr,td{display:block}
  thead{display:none}
  tr{border-bottom:1px solid var(--line);padding:8px 4px;position:relative;transition:transform .15s;touch-action:pan-y}
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
    <nav><a href="index.html" id="nav-all">All openings</a><a href="new.html" id="nav-new">New openings</a><a href="#saved" id="nav-saved">Saved <span class="n" id="saved-n">0</span></a></nav>
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
  <th data-k="posted">Posted</th><th data-k="first">First seen</th><th data-k="status">Status</th><th>Link</th><th>Save</th>
</tr></thead><tbody id="tb"></tbody></table><div class="empty" id="empty" hidden>No openings match.</div></div>
<div id="savedwrap" hidden>
  <div class="sbar" id="sbar"></div>
  <div id="savedlist"></div>
  <div class="empty" id="sempty" hidden>Nothing saved yet. Use the <b>Save</b> button on a row (or swipe a row to the right on your phone) to build your applications checklist.</div>
</div>
<div id="toast"></div>
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
 $('#count').textContent=`${rows.length} of ${D.rows.length} shown`+($('#count').dataset.hint||'');
 $('#empty').hidden=rows.length>0;
 $('#tb').innerHTML=rows.map(r=>`<tr class="${r.status}${saved[r.k]?' saved':''}" data-k="${esc(r.k)}">
  <td data-l="Company">${esc(r.company)} <span class="chip">P${r.priority}</span></td>
  <td class="title" data-l="Title">${esc(r.title)}${r.new_run?' <span class="chip run">new</span>':r.new?' <span class="chip new">new</span>':''}${r.reopened?' <span class="chip re">reopened</span>':''}<span class="dept">${esc(r.dept||r.loc)}</span></td>
  <td data-l="City" title="${esc(r.loc)}">${esc(r.city||r.loc||'—')}${r.country?' <span class="chip">'+esc(r.country)+'</span>':''}</td>
  <td data-l="Type">${esc(lbl('type',r.type))}</td>
  <td data-l="Function">${esc(lbl('fn',r.fn))}</td>
  <td data-l="Fit" class="num"><span class="fit ${r.fit>=70?'hi':r.fit>=45?'mid':'lo'}" title="${esc(bdTitle(r))}">${Math.round(r.fit)}</span></td>
  <td data-l="Posted" class="num">${fmtD(r.posted)||'—'}</td>
  <td data-l="First seen" class="num">${fmtD(r.first)}</td>
  <td data-l="Status"><span class="chip ${r.status}">${r.status}</span></td>
  <td data-l="Link"><a href="${esc(r.url)}" target="_blank" rel="noopener">open ↗</a></td>
  <td data-l="Save" class="save"><button class="star ${saved[r.k]?'on':''}" data-k="${esc(r.k)}" title="Save to the applications checklist">${saved[r.k]?'★ Saved':'☆ Save'}</button></td></tr>`).join('');
}

// ---- Saved applications checklist -------------------------------------------------
// Stored in this browser (localStorage), shared by index.html and new.html. A snapshot of
// each saved row is kept so the checklist survives the opening being closed or dropped.
// "Copy sync link" moves the list to another device (phone <-> computer) without a server.
const SKEY='deskradar.saved.v1';
const STATUSES=[['to_apply','To apply'],['applied','Applied'],['interview','Interview'],['offer','Offer'],['rejected','Rejected'],['dropped','Dropped']];
const SLBL=Object.fromEntries(STATUSES);
let saved={};
try{saved=JSON.parse(localStorage.getItem(SKEY)||'{}')||{};}catch(e){saved={};}
function persist(){try{localStorage.setItem(SKEY,JSON.stringify(saved));}catch(e){}}
let toastT=null;
function toast(msg){const t=$('#toast');t.textContent=msg;t.classList.add('show');clearTimeout(toastT);toastT=setTimeout(()=>t.classList.remove('show'),1500);}
function snap(r){return {k:r.k,company:r.company,title:r.title,url:r.url,city:r.city||r.loc||'',country:r.country||'',type:r.type,fn:r.fn,fit:Math.round(r.fit),posted:r.posted,savedAt:new Date().toISOString(),status:'to_apply',deadline:'',note:''};}
function toggleSave(k){
 if(saved[k]){delete saved[k];toast('Removed from saved');}
 else{const r=D.rows.find(x=>x.k===k);if(!r)return;saved[k]=snap(r);toast('Saved ★ — see the Saved tab');}
 persist();refreshSaved();
}
function refreshSaved(){
 $('#saved-n').textContent=Object.keys(saved).length;
 if(view==='saved')drawSaved();else draw();
}
const tb=$('#tb');
tb.addEventListener('click',e=>{const b=e.target.closest('button.star');if(b){e.preventDefault();toggleSave(b.dataset.k);}});
// Swipe a row to the right on a phone to save it (swipe again to remove).
let sw=null;
tb.addEventListener('touchstart',e=>{const tr=e.target.closest('tr');if(!tr||!matchMedia('(max-width:720px)').matches)return;const t=e.touches[0];sw={tr,x:t.clientX,y:t.clientY,dx:0,on:false};},{passive:true});
tb.addEventListener('touchmove',e=>{if(!sw)return;const t=e.touches[0];const dx=t.clientX-sw.x,dy=t.clientY-sw.y;
 if(!sw.on){if(dx>12&&Math.abs(dx)>Math.abs(dy)*1.5)sw.on=true;else if(Math.abs(dy)>12||dx<-12){sw=null;return;}}
 if(sw.on){sw.dx=Math.max(0,Math.min(dx,140));sw.tr.style.transform=`translateX(${sw.dx}px)`;sw.tr.classList.add('swiping');sw.tr.classList.toggle('will',sw.dx>80);}},{passive:true});
function endSwipe(){if(!sw)return;const {tr,dx,on}=sw;tr.style.transform='';tr.classList.remove('swiping','will');sw=null;if(on&&dx>80&&tr.dataset.k)toggleSave(tr.dataset.k);}
tb.addEventListener('touchend',endSwipe);tb.addEventListener('touchcancel',endSwipe);
if('ontouchstart' in window){$('#count').dataset.hint=' · swipe a row to the right to save it';}

function b64e(str){return btoa(unescape(encodeURIComponent(str))).replace(/\+/g,'-').replace(/\//g,'_').replace(/=+$/,'');}
function b64d(str){str=str.replace(/-/g,'+').replace(/_/g,'/');while(str.length%4)str+='=';return decodeURIComponent(escape(atob(str)));}
function copyText(text,what){
 const done=()=>toast(what+' copied to the clipboard');
 if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(text).then(done,()=>fallbackCopy(text,done));}else fallbackCopy(text,done);
}
function fallbackCopy(text,done){const ta=document.createElement('textarea');ta.value=text;ta.style.position='fixed';ta.style.opacity='0';document.body.appendChild(ta);ta.select();try{document.execCommand('copy');done();}catch(e){toast('Copy failed');}document.body.removeChild(ta);}
function mergeSaved(items){let n=0;for(const it of items){if(!it||!it.k)continue;if(!saved[it.k]){saved[it.k]=it;n++;}else{const cur=saved[it.k];if((it.savedAt||'')>(cur.savedAt||'')||cur.status==='to_apply'&&it.status!=='to_apply'){saved[it.k]={...cur,...it};}}}persist();return n;}
function markdown(){
 const items=Object.values(saved);const d=new Date().toISOString().slice(0,10);
 let out=`# Desk Radar applications checklist (${d})\n`;
 for(const [st,name] of STATUSES){const grp=items.filter(i=>(i.status||'to_apply')===st);if(!grp.length)continue;out+=`\n## ${name}\n`;
  grp.sort((a,b)=>(a.deadline||'9')<(b.deadline||'9')?-1:(a.deadline||'9')>(b.deadline||'9')?1:b.fit-a.fit);
  for(const i of grp)out+=`- [${st==='to_apply'?' ':'x'}] ${i.company} — [${i.title}](${i.url}) · ${i.city||'—'} · ${lbl('type',i.type)} · fit ${i.fit}${i.deadline?' · deadline '+i.deadline:''}${i.note?' · '+i.note:''}\n`;}
 return out;
}
function drawSaved(){
 const items=Object.values(saved);
 const by={};for(const i of items){by[i.status||'to_apply']=(by[i.status||'to_apply']||0)+1;}
 $('#sbar').innerHTML=`<span><b>${items.length}</b> saved${STATUSES.filter(([k])=>by[k]).map(([k,n])=>` · ${n} ${by[k]}`).join('')}</span><span class="sp"></span>
  <button id="s-md" title="Copy the checklist as Markdown">Copy as Markdown</button>
  <button id="s-link" title="Copy a link that imports this list on another device (open it on your phone)">Copy sync link</button>
  <button id="s-json" title="Download the list as a JSON file">Export</button>
  <label><input type="file" id="s-imp" accept="application/json,.json" hidden><button id="s-imp-b">Import</button></label>
  <button id="s-clear" title="Remove rejected and dropped applications">Clear rejected</button>`;
 $('#s-md').onclick=()=>copyText(markdown(),'Checklist');
 $('#s-link').onclick=()=>copyText(location.origin+location.pathname+'#import='+b64e(JSON.stringify(items)),'Sync link');
 $('#s-json').onclick=()=>{const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([JSON.stringify(items,null,1)],{type:'application/json'}));a.download='desk-radar-saved.json';a.click();URL.revokeObjectURL(a.href);};
 $('#s-imp-b').onclick=()=>$('#s-imp').click();
 $('#s-imp').onchange=e=>{const f=e.target.files[0];if(!f)return;f.text().then(t=>{try{const n=mergeSaved(JSON.parse(t));toast(`Imported ${n} new item${n===1?'':'s'}`);drawSaved();$('#saved-n').textContent=Object.keys(saved).length;}catch(err){toast('Not a valid export file');}});};
 $('#s-clear').onclick=()=>{let n=0;for(const i of items){if(i.status==='rejected'||i.status==='dropped'){delete saved[i.k];n++;}}persist();toast(n?`Removed ${n}`:'Nothing to clear');refreshSaved();};
 $('#sempty').hidden=items.length>0;
 const order=Object.fromEntries(STATUSES.map(([k],i)=>[k,i]));
 items.sort((a,b)=>(order[a.status]??0)-(order[b.status]??0)||((a.deadline||'9')<(b.deadline||'9')?-1:(a.deadline||'9')>(b.deadline||'9')?1:0)||b.fit-a.fit);
 let html='',cur=null;
 for(const i of items){
  const st=i.status||'to_apply';if(st!==cur){cur=st;html+=`<div class="shead">${SLBL[st]||st}</div>`;}
  const live=D.rows.find(r=>r.k===i.k);const gone=MODE==='all'&&(!live||live.status!=='open');
  html+=`<div class="card ${st}" data-k="${esc(i.k)}">
   <div><select data-f="status">${STATUSES.map(([k,n])=>`<option value="${k}"${k===st?' selected':''}>${n}</option>`).join('')}</select></div>
   <div><b>${esc(i.company)}</b> · <a href="${esc(i.url)}" target="_blank" rel="noopener">${esc(i.title)} ↗</a>
    <div class="sub">${esc(i.city||'—')}${i.country?' · '+esc(i.country):''} · ${esc(lbl('type',i.type))} · ${esc(lbl('fn',i.fn))} · fit <span class="fit ${i.fit>=70?'hi':i.fit>=45?'mid':'lo'}">${i.fit}</span> · saved ${fmtD(i.savedAt)}${gone?' · <span class="chip closed">no longer listed</span>':''}</div>
    <div class="fields"><label>Deadline <input type="date" data-f="deadline" value="${esc(i.deadline||'')}"></label><input type="text" data-f="note" placeholder="Notes (contact, referral, next step…)" value="${esc(i.note||'')}"></div></div>
   <div><button data-act="rm" title="Remove from the checklist">Remove</button></div></div>`;
 }
 $('#savedlist').innerHTML=html;
}
const sl=$('#savedlist');
sl.addEventListener('change',e=>{const card=e.target.closest('.card');const f=e.target.dataset.f;if(!card||!f||!saved[card.dataset.k])return;saved[card.dataset.k][f]=e.target.value;persist();if(f==='status')drawSaved();});
sl.addEventListener('input',e=>{const card=e.target.closest('.card');const f=e.target.dataset.f;if(card&&f==='note'&&saved[card.dataset.k]){saved[card.dataset.k].note=e.target.value;persist();}});
sl.addEventListener('click',e=>{const b=e.target.closest('button[data-act=rm]');if(!b)return;const card=b.closest('.card');delete saved[card.dataset.k];persist();toast('Removed');refreshSaved();});

// ---- views: table (default) or saved checklist, driven by the URL hash --------------
let view='table';
function setView(v){
 view=v;const sv=v==='saved';
 $('#filters').hidden=sv;$('#count').hidden=sv;document.querySelector('.wrap').hidden=sv;$('#savedwrap').hidden=!sv;
 $('#nav-saved').classList.toggle('cur',sv);$('#nav-'+MODE).classList.toggle('cur',!sv);
 if(sv)drawSaved();else draw();
}
function route(){
 const h=location.hash||'';
 if(h.startsWith('#import=')){try{const n=mergeSaved(JSON.parse(b64d(h.slice(8))));toast(`Imported ${n} new item${n===1?'':'s'}`);}catch(e){toast('Could not read the sync link');}
  history.replaceState(null,'',location.pathname+'#saved');}
 $('#saved-n').textContent=Object.keys(saved).length;
 setView((location.hash||'')==='#saved'?'saved':'table');
}
window.addEventListener('hashchange',route);
route();
})();
</script>
</body>
</html>
"""
