from pathlib import Path
p=Path('simulation.html')
s=p.read_text()
old="function renderDiagnosticTree(){const tree=$('diagnosticTree');tree.innerHTML=diagnosticTreeData().map(n=>{const answers=n.answers.map(a=>`<div class=\"diagnostic-answer\"><h4>${a.label}</h4><ul>${a.values.map(v=>`<li>${v}</li>`).join('')}</ul></div>`).join('');const insights=[...n.good.map(x=>`<p><strong>Point fort :</strong> ${x.text}<br><span>${x.why}</span></p>`),...n.bad.map(x=>`<p><strong>Point à améliorer :</strong> ${x.text}<br><span>${x.why}</span></p>`)].join('');return `<article class=\"diagnostic-node\"><span class=\"diagnostic-phase\">Phase ${n.phase}</span><h3>${n.title}</h3>${answers}${insights?`<div class=\"diagnostic-insight\">${insights}</div>`:''}</article>`}).join('')}"
new="function renderDiagnosticTree(){const tree=$('diagnosticTree');tree.innerHTML=diagnosticTreeData().map(n=>{const answers=n.answers.map(a=>`<div class=\"diagnostic-answer\"><h4>${a.label}</h4><ul>${a.values.map(v=>`<li>${v}</li>`).join('')}</ul></div>`).join('');return `<article class=\"diagnostic-node\"><span class=\"diagnostic-phase\">Phase ${n.phase}</span><h3>${n.title}</h3>${answers}</article>`}).join('')}"
if old not in s:
    raise SystemExit('renderDiagnosticTree target not found')
s=s.replace(old,new,1)
p.write_text(s)
