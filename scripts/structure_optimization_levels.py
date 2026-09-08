from pathlib import Path
import re

p=Path('simulation.html')
s=p.read_text()

# 1) Donner aux optimisations une justification issue du point faible qui les déclenche.
s=s.replace("if(improve)improvements.push({priority,text:improve})};","if(improve)improvements.push({priority,text:improve,why})};",1)

# 2) Conserver les optimisations sous forme structurée et les répartir en 3 niveaux.
old="const sortedWeak=weaknesses.sort((a,b)=>b.priority-a.priority);const sortedImp=[...new Map(improvements.sort((a,b)=>b.priority-a.priority).map(x=>[x.text,x])).values()];const complexityScore="
new="const sortedWeak=weaknesses.sort((a,b)=>b.priority-a.priority);const sortedImp=[...new Map(improvements.sort((a,b)=>b.priority-a.priority).map(x=>[x.text,x])).values()];const optimizationItems=sortedImp.slice(0,6);const optimizationLevels={critical:optimizationItems.filter(x=>x.priority>=85),structuring:optimizationItems.filter(x=>x.priority>=70&&x.priority<85),advanced:optimizationItems.filter(x=>x.priority<70)};const complexityScore="
if old not in s:
    raise SystemExit('sortedImp target not found')
s=s.replace(old,new,1)

old_return="improvements:sortedImp.slice(0,4).map(x=>x.text),advancedEligible};}"
new_return="improvements:optimizationItems.map(x=>x.text),optimizationLevels,advancedEligible};}"
if old_return not in s:
    raise SystemExit('buildResult return target not found')
s=s.replace(old_return,new_return,1)

# 3) Remplacer l'ancienne section unique d'optimisations par les trois niveaux.
pattern=r'<section class="analysis-section" id="analysisOptimizationsSection" hidden>\s*<h3>Optimisations possibles</h3>\s*<div class="analysis-items" id="analysisOptimizations"></div>\s*</section>'
replacement='''<section class="analysis-section analysis-optimizations-section" id="analysisOptimizationsSection" hidden>
      <h3 class="analysis-subtitle">Optimisations à envisager</h3>
      <p class="analysis-intro">Les optimisations sont classées selon leur niveau de priorité afin de distinguer ce qu’il faut sécuriser d’abord, ce qui structure votre fonctionnement et ce qui permet d’aller plus loin.</p>
      <div class="optimization-levels">
        <section class="optimization-level optimization-level-critical" id="optimizationCriticalSection" hidden>
          <div class="optimization-level-head"><span class="optimization-level-label">Priorité 1</span><h4>Critiques</h4><p>À traiter en priorité pour sécuriser votre fonctionnement.</p></div>
          <div class="analysis-items" id="optimizationCritical"></div>
        </section>
        <section class="optimization-level optimization-level-structuring" id="optimizationStructuringSection" hidden>
          <div class="optimization-level-head"><span class="optimization-level-label">Priorité 2</span><h4>Structurantes</h4><p>Pour rendre votre organisation plus fiable, plus claire et plus fluide.</p></div>
          <div class="analysis-items" id="optimizationStructuring"></div>
        </section>
        <section class="optimization-level optimization-level-advanced" id="optimizationAdvancedSection" hidden>
          <div class="optimization-level-head"><span class="optimization-level-label">Priorité 3</span><h4>Avancées</h4><p>Pour aller plus loin dans l’automatisation, la personnalisation et la fidélisation.</p></div>
          <div class="analysis-items" id="optimizationAdvanced"></div>
        </section>
      </div>
    </section>'''
s2,n=re.subn(pattern,replacement,s,count=1)
if n!=1:
    raise SystemExit('analysis optimization HTML target not found')
s=s2

# 4) Remplacer le rendu de l'ancienne liste par le rendu des 3 niveaux.
old_call="render('analysisOptimizationsSection','analysisOptimizations',(r.improvements||[]).map(x=>({text:x,why:''})));"
new_call="""const levels=r.optimizationLevels||{critical:[],structuring:[],advanced:[]};const renderLevel=(sectionId,rootId,items)=>{const section=$(sectionId),root=$(rootId);if(!section||!root)return;const clean=(items||[]).filter(x=>x&&x.text);section.hidden=!clean.length;root.innerHTML=clean.map(x=>`<article class=\"analysis-item\"><strong>${esc(x.text)}</strong>${x.why?`<p>${esc(x.why)}</p>`:''}</article>`).join('')};renderLevel('optimizationCriticalSection','optimizationCritical',levels.critical);renderLevel('optimizationStructuringSection','optimizationStructuring',levels.structuring);renderLevel('optimizationAdvancedSection','optimizationAdvanced',levels.advanced);const optimizationSection=$('analysisOptimizationsSection');if(optimizationSection)optimizationSection.hidden=!(levels.critical.length||levels.structuring.length||levels.advanced.length);"""
if old_call not in s:
    raise SystemExit('render optimization call target not found')
s=s.replace(old_call,new_call,1)

# 5) Styles : séparation nette diagnostic / optimisations et hiérarchie visuelle.
css_anchor='.analysis-section#analysisWeaknessesSection .analysis-item{background:linear-gradient(180deg,#d8dcdd,var(--silver))}'
css_add='''.analysis-optimizations-section{margin-top:10px;padding-top:32px!important;border-top:2px solid rgba(16,36,58,.28)!important}.analysis-subtitle{font-size:28px!important;margin-bottom:8px!important}.analysis-intro{max-width:900px;font-size:15px!important;line-height:1.6!important;color:#29445c;margin:0 0 22px!important}.optimization-levels{display:grid;gap:18px}.optimization-level{border-radius:16px;padding:18px;border:1px solid rgba(16,36,58,.15);background:rgba(242,238,229,.16)}.optimization-level[hidden]{display:none}.optimization-level-head{margin-bottom:14px}.optimization-level-label{display:block;font-size:10px;font-weight:900;letter-spacing:1.2px;text-transform:uppercase;color:#50677a;margin-bottom:4px}.optimization-level h4{font-family:\"Iowan Old Style\",\"Palatino Linotype\",Palatino,Georgia,serif;font-size:23px;line-height:1.1;margin:0 0 5px;color:var(--blue)}.optimization-level-head p{font-size:13px!important;line-height:1.45!important;margin:0!important;color:#29445c}.optimization-level-critical{border-left:5px solid #10243a}.optimization-level-structuring{border-left:5px solid #50677a}.optimization-level-advanced{border-left:5px solid rgba(16,36,58,.28)}.optimization-level .analysis-item{background:rgba(242,238,229,.34)}'''
if css_anchor not in s:
    raise SystemExit('CSS anchor not found')
s=s.replace(css_anchor,css_anchor+css_add,1)

p.write_text(s)
