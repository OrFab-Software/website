from pathlib import Path
p=Path('simulation.html')
s=p.read_text()

# Compact labels validated phase by phase.
start=s.index('function compactSummaryLabel(')
end=s.index('function phaseAnswers(', start)
compact="""function compactSummaryLabel(id,fallback){const labels={channels:'Vos canaux d’entrée',volume:'Volume mensuel',centralized:'Centralisation',centralwhere:'Outil de suivi',centralmode:'Mode de centralisation',aftercontact:'Après le premier contact',remindertracking:'Suivi des relances',forgotreminder:'Risque d’oubli',conversion:'Déclencheur client',predocs:'Documents d’engagement',predoclist:'Documents utilisés',predocmode:'Préparation des documents',transitionactions:'Actions déclenchées',tracking:'Suivi de la prestation',recurring:'Actions récurrentes',reentry:'Double saisie',clientdocs:'Documents utilisés',forgotdoc:'Risque d’oubli documentaire',ordered:'Ordre des étapes',deadlines:'Échéances',afterservice:'Après la prestation',reviewauto:'Avis client',followuptime:'Suivi dans le temps',recallplan:'Relances après prestation',recalltime:'Échéance de relance',oldclients:'Nouvelles opportunités',newsletterfrequency:'Communication client'};return labels[id]||fallback}\n"""
s=s[:start]+compact+s[end:]

# Keep the phase cards concise and remove redundant yes/no information when the detail already says it.
start=s.index('function phaseAnswers(')
end=s.index('function renderPhaseSummary(', start)
phase_answers="""function phaseAnswers(phase){const rows=[];screens.filter(screen=>screen.phase===phase&&(!screen.when||screen.when(state))).forEach(screen=>{if(screen.fields){visibleFields(screen).forEach(field=>{const value=state[field.id];if(value===undefined||value===null||value===''||(Array.isArray(value)&&!value.length))return;if(field.id==='predocs'&&state.predocs==='yes'&&Array.isArray(state.predoclist)&&state.predoclist.length)return;let values=(Array.isArray(value)?value:[value]).map(v=>optionLabel(field,v));if(field.id==='reviewauto')values=values.map(v=>v==='Oui'?'Automatique':v==='Non'?'Manuelle':v);rows.push({label:compactSummaryLabel(field.id,field.title),values})})}else if(screen.custom==='servicesNaming'&&state.services){const names=[];for(let i=1;i<=serviceCount();i++)if((state.serviceNames?.[i]||'').trim())names.push(serviceName(i));if(names.length)rows.push({label:'Vos prestations',values:names})}else if(screen.custom==='servicesSimilarity'&&serviceCount()>1){const groups=(state.serviceGroups||[]).map((g,i)=>`Parcours ${i+1} : ${g.map(serviceName).join(' · ')}`);if(groups.length)rows.push({label:'Organisation des parcours',values:groups})}});return rows}\n"""
s=s[:start]+phase_answers+s[end:]

# OrFab blue background behind the phase cards, with silver cards.
old=".phase-summary{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px;margin-top:32px}"
new=".phase-summary{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px;margin-top:32px;padding:18px;background:var(--blue);border-radius:22px}"
if old not in s:
    raise SystemExit('phase-summary css target not found')
s=s.replace(old,new,1)
old=".phase-summary-card{border:1px solid rgba(16,36,58,.15);border-radius:18px;padding:20px;background:rgba(190,195,195,.18)}"
new=".phase-summary-card{border:1px solid rgba(16,36,58,.18);border-radius:18px;padding:20px;background:var(--silver);color:var(--blue)}"
if old not in s:
    raise SystemExit('phase-summary-card css target not found')
s=s.replace(old,new,1)
s=s.replace('.phase-summary-card h3{font-size:22px;margin:0 0 16px}', '.phase-summary-card h3{font-size:22px;margin:0 0 12px}', 1)
s=s.replace('.phase-summary-row{padding:12px 0;border-top:1px solid rgba(16,36,58,.10)}', '.phase-summary-row{padding:9px 0;border-top:1px solid rgba(16,36,58,.12)}', 1)
s=s.replace('.phase-summary-row li{font-size:13px;line-height:1.5;margin:3px 0}', '.phase-summary-row li{font-size:13px;line-height:1.4;margin:2px 0}', 1)

p.write_text(s)
