from pathlib import Path

p = Path('simulation.html')
s = p.read_text()

# 1) Add visible summary cards after the result intro.
old_html = '<p class="result-lead" id="resultProfileText"></p><div class="result-flow">'
new_html = '<p class="result-lead" id="resultProfileText"></p><div class="phase-summary" id="phaseSummary"></div><div class="result-flow">'
if old_html not in s:
    raise SystemExit('result intro target not found')
s = s.replace(old_html, new_html, 1)

# 2) Add dedicated styles for the visible four-card summary.
needle = '.result-lead{font-size:18px;line-height:1.65;color:#29445c;max-width:1080px;margin:0}'
insert = needle + '.phase-summary{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px;margin-top:32px}.phase-summary-card{border:1px solid rgba(16,36,58,.15);border-radius:18px;padding:20px;background:rgba(190,195,195,.18)}.phase-summary-card .summary-phase{display:block;color:#9b6c18;font-size:11px;font-weight:850;letter-spacing:1.2px;text-transform:uppercase;margin-bottom:5px}.phase-summary-card h3{font-size:22px;margin:0 0 16px}.phase-summary-row{padding:12px 0;border-top:1px solid rgba(16,36,58,.10)}.phase-summary-row:first-of-type{border-top:0;padding-top:0}.phase-summary-row h4{font-size:12px;line-height:1.35;margin:0 0 7px;color:#50677a;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;font-weight:800}.phase-summary-row ul{margin:0;padding-left:18px}.phase-summary-row li{font-size:13px;line-height:1.5;margin:3px 0}'
if needle not in s:
    raise SystemExit('result lead css target not found')
s = s.replace(needle, insert, 1)

# Responsive summary layout.
s = s.replace('@media(max-width:1100px){.grid{grid-template-columns:1fr}.map-card{position:relative;top:auto}.diagnostic-tree{grid-template-columns:repeat(2,minmax(0,1fr))}}', '@media(max-width:1100px){.grid{grid-template-columns:1fr}.map-card{position:relative;top:auto}.diagnostic-tree,.phase-summary{grid-template-columns:repeat(2,minmax(0,1fr))}}', 1)
s = s.replace('@media(max-width:600px){.question,.map-card,.result-card{padding:22px}.diagnostic-tree{grid-template-columns:1fr}', '@media(max-width:600px){.question,.map-card,.result-card{padding:22px}.diagnostic-tree,.phase-summary{grid-template-columns:1fr}', 1)

# 3) Render all answered questions in four visible phase cards.
marker = 'function diagnosticTreeData(){'
idx = s.index(marker)
render_fn = r'''function renderPhaseSummary(){const root=$('phaseSummary');if(!root)return;const phases=[{phase:1,title:'Parcours prospect'},{phase:2,title:'Qualification en client'},{phase:3,title:'Parcours client'},{phase:4,title:'Fidélisation client'}];root.innerHTML=phases.map(p=>{const rows=phaseAnswers(p.phase).map(a=>`<div class="phase-summary-row"><h4>${a.label}</h4><ul>${a.values.map(v=>`<li>${v}</li>`).join('')}</ul></div>`).join('');return `<article class="phase-summary-card"><span class="summary-phase">Phase ${p.phase}</span><h3>${p.title}</h3>${rows}</article>`}).join('')}
'''
s = s[:idx] + render_fn + s[idx:]

# 4) Make the visible summary render with the result.
old_show = "function showResult(){const r=buildResult();$('resultProfileTitle').textContent='Analyse de votre simulation';$('resultProfileText').textContent=r.process;"
new_show = "function showResult(){const r=buildResult();$('resultProfileTitle').textContent='Analyse de votre simulation';$('resultProfileText').textContent=r.process;renderPhaseSummary();"
if old_show not in s:
    raise SystemExit('showResult target not found')
s = s.replace(old_show, new_show, 1)

p.write_text(s)
