from pathlib import Path
import re

p=Path('simulation.html')
s=p.read_text()

# Style du bloc d'analyse pleine largeur
anchor='.result-flow strong{color:var(--blue)}'
extra='''.result-flow strong{color:var(--blue)}.analysis-title{font-size:clamp(34px,4vw,52px);line-height:1.05;margin:0 0 26px;color:var(--blue)}.analysis-sections{display:grid;gap:24px}.analysis-section{padding-top:22px;border-top:1px solid rgba(16,36,58,.2)}.analysis-section:first-child{padding-top:0;border-top:0}.analysis-section[hidden]{display:none}.analysis-section h3{font-size:22px;margin:0 0 14px;color:var(--blue)}.analysis-items{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px}.analysis-item{background:rgba(242,238,229,.28);border:1px solid rgba(16,36,58,.14);border-radius:14px;padding:16px 18px}.analysis-item strong{display:block;font-size:15px;line-height:1.4;margin-bottom:6px}.analysis-item p{font-size:14px;line-height:1.55;margin:0;color:#29445c}.analysis-legacy{display:none!important}'''
if anchor not in s:
    raise SystemExit('CSS anchor not found')
s=s.replace(anchor, extra, 1)

# Mobile
mobile_anchor='.result-flow{width:calc(100% + 44px);margin-left:-22px;margin-right:-22px;padding:30px 22px 14px}'
mobile_new=mobile_anchor+'.analysis-items{grid-template-columns:1fr}'
if mobile_anchor not in s:
    raise SystemExit('mobile anchor not found')
s=s.replace(mobile_anchor,mobile_new,1)

# Remplace le contenu du bloc or sans toucher aux actions qui suivent
pattern=r'<div class="result-flow">.*?</div><div class="result-actions">'
replacement='''<div class="result-flow">
  <h2 class="analysis-title">L’analyse</h2>
  <div class="analysis-sections">
    <section class="analysis-section" id="analysisStrengthsSection" hidden>
      <h3>Points forts</h3>
      <div class="analysis-items" id="analysisStrengths"></div>
    </section>
    <section class="analysis-section" id="analysisWeaknessesSection" hidden>
      <h3>Points faibles</h3>
      <div class="analysis-items" id="analysisWeaknesses"></div>
    </section>
    <section class="analysis-section" id="analysisOptimizationsSection" hidden>
      <h3>Optimisations possibles</h3>
      <div class="analysis-items" id="analysisOptimizations"></div>
    </section>
  </div>
  <p class="analysis-legacy" id="resultAnalysisText"></p>
  <p class="analysis-legacy" id="resultSolutionText"></p>
  <p class="analysis-legacy" id="resultOfferText"></p>
  <p class="analysis-legacy offer-note" id="resultOfferNote"></p>
</div><div class="result-actions">'''
s2,n=re.subn(pattern,replacement,s,count=1,flags=re.S)
if n!=1:
    raise SystemExit(f'result-flow replacement count={n}')
s=s2

helper='''function renderAnalysisSections(r){
  const esc=v=>String(v??'').replace(/[&<>\"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
  const render=(sectionId,rootId,items)=>{
    const section=$(sectionId),root=$(rootId);
    if(!section||!root)return;
    const clean=(items||[]).filter(x=>x&&(x.text||x.why));
    section.hidden=!clean.length;
    root.innerHTML=clean.map(x=>`<article class="analysis-item"><strong>${esc(x.text||'')}</strong>${x.why?`<p>${esc(x.why)}</p>`:''}</article>`).join('');
  };
  render('analysisStrengthsSection','analysisStrengths',r.strengths);
  render('analysisWeaknessesSection','analysisWeaknesses',r.weaknesses);
  render('analysisOptimizationsSection','analysisOptimizations',r.axes);
}

'''
if 'function renderAnalysisSections(r)' not in s:
    idx=s.find('function showResult(){')
    if idx<0:
        raise SystemExit('showResult not found')
    s=s[:idx]+helper+s[idx:]

# Appel du renderer après la synthèse des phases
needle='renderPhaseSummary();'
if needle not in s:
    raise SystemExit('renderPhaseSummary call not found')
s=s.replace(needle,needle+'renderAnalysisSections(r);',1)

p.write_text(s)
