from pathlib import Path

p = Path('simulation.html')
s = p.read_text()

old_css = ".diagnostic-node h3{font-size:19px;margin:0 0 12px}.diagnostic-node p{font-size:13px;line-height:1.5;margin:8px 0}.diagnostic-node strong{color:#9b6c18}.diagnostic-empty{color:#667989}"
new_css = ".diagnostic-node .diagnostic-phase{display:block;color:#9b6c18;font-size:11px;font-weight:850;letter-spacing:1.2px;text-transform:uppercase;margin-bottom:4px}.diagnostic-node h3{font-size:21px;margin:0 0 16px}.diagnostic-answer{padding:12px 0;border-top:1px solid rgba(16,36,58,.10)}.diagnostic-answer:first-of-type{border-top:0;padding-top:0}.diagnostic-answer h4{font-size:12px;line-height:1.35;margin:0 0 7px;color:#50677a;font-family:-apple-system,BlinkMacSystemFont,\"Segoe UI\",sans-serif;font-weight:800}.diagnostic-answer ul{margin:0;padding-left:18px}.diagnostic-answer li{font-size:13px;line-height:1.5;margin:3px 0}.diagnostic-insight{margin-top:14px;padding-top:12px;border-top:1px solid rgba(16,36,58,.12)}.diagnostic-insight p{font-size:13px;line-height:1.5;margin:8px 0}.diagnostic-node strong{color:#9b6c18}"
if old_css not in s:
    raise SystemExit('CSS target not found')
s = s.replace(old_css, new_css, 1)

start = s.index('function diagnosticTreeData(){')
end = s.index('function showResult(){', start)
new = r'''function optionLabel(field,value){const found=(field.options||[]).find(o=>o.value===value);return found?found.label:String(value)}
function phaseAnswers(phase){const rows=[];screens.filter(screen=>screen.phase===phase&&(!screen.when||screen.when(state))).forEach(screen=>{if(screen.fields){visibleFields(screen).forEach(field=>{const value=state[field.id];if(value===undefined||value===null||value===''||(Array.isArray(value)&&!value.length))return;const values=(Array.isArray(value)?value:[value]).map(v=>optionLabel(field,v));rows.push({label:field.title,values})})}else if(screen.custom==='servicesNaming'&&state.services){const names=[];for(let i=1;i<=serviceCount();i++)if((state.serviceNames?.[i]||'').trim())names.push(serviceName(i));if(names.length)rows.push({label:'Prestations proposées',values:names})}else if(screen.custom==='servicesSimilarity'&&serviceCount()>1){const groups=(state.serviceGroups||[]).map((g,i)=>`Parcours ${i+1} : ${g.map(serviceName).join(' · ')}`);if(groups.length)rows.push({label:'Organisation des parcours',values:groups})}});return rows}
function diagnosticTreeData(){const r=buildResult();const byPhase=[{phase:1,title:'Parcours prospect',keys:['demandes','relances','mémoire','centralisation','prospect']},{phase:2,title:'Qualification en client',keys:['passage','déclencheur','documents','client']},{phase:3,title:'Parcours client',keys:['parcours','saisie','échéance','prestations','actions','documentaire']},{phase:4,title:'Fidélisation client',keys:['après','anciens clients','avis','relances après','fidélisation']}];return byPhase.map(p=>({phase:p.phase,title:p.title,answers:phaseAnswers(p.phase),good:r.strengths.filter(x=>p.keys.some(k=>(x.text+' '+x.why).toLowerCase().includes(k))),bad:r.weaknesses.filter(x=>p.keys.some(k=>(x.text+' '+x.why).toLowerCase().includes(k)))}))}
function renderDiagnosticTree(){const tree=$('diagnosticTree');tree.innerHTML=diagnosticTreeData().map(n=>{const answers=n.answers.map(a=>`<div class="diagnostic-answer"><h4>${a.label}</h4><ul>${a.values.map(v=>`<li>${v}</li>`).join('')}</ul></div>`).join('');const insights=[...n.good.map(x=>`<p><strong>Point fort :</strong> ${x.text}<br><span>${x.why}</span></p>`),...n.bad.map(x=>`<p><strong>Point à améliorer :</strong> ${x.text}<br><span>${x.why}</span></p>`)].join('');return `<article class="diagnostic-node"><span class="diagnostic-phase">Phase ${n.phase}</span><h3>${n.title}</h3>${answers}${insights?`<div class="diagnostic-insight">${insights}</div>`:''}</article>`}).join('')}
'''
s = s[:start] + new + s[end:]
p.write_text(s)
