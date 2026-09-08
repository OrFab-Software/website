from pathlib import Path
import re
p=Path('simulation.html')
s=p.read_text()
# Dynamic columns + badges
s=s.replace('grid-template-columns:minmax(320px,1.8fr) repeat(3,minmax(120px,.55fr))','grid-template-columns:minmax(320px,1.8fr) repeat(var(--offer-count,3),minmax(120px,.55fr))',1)
s=s.replace('grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;margin-top:18px','grid-template-columns:repeat(var(--offer-count,3),minmax(0,1fr));gap:12px;margin-top:18px',1)
css_anchor='.offers-fit-opt small{display:block;color:#50677a;margin-top:4px}'
css_add='''.offers-fit-badge{display:inline-flex!important;width:max-content;margin-top:6px!important;padding:4px 8px;border-radius:999px;font-size:10px!important;font-weight:850;line-height:1!important}.offers-fit-badge.critical{background:#f2c7c7;color:#692626}.offers-fit-badge.structuring{background:#c8dcf2;color:#174d78}.offers-fit-badge.advanced{background:#cce9d2;color:#1d6840}.offers-fit-plan.recommended{outline:3px solid var(--blue);outline-offset:-3px}.offers-fit-plan .fit-status{display:block;margin:0 auto 10px;width:max-content;padding:5px 10px;border-radius:999px;background:rgba(16,36,58,.1);font-size:10px;font-weight:900;letter-spacing:.7px;text-transform:uppercase}.offers-fit-plan.signature .fit-status{background:rgba(242,238,229,.18);color:var(--cream)}'''
if css_anchor in s and '.offers-fit-badge{' not in s:
    s=s.replace(css_anchor,css_anchor+css_add,1)
s=s.replace('grid-template-columns:minmax(190px,1.5fr) repeat(3,minmax(82px,.5fr))','grid-template-columns:minmax(190px,1.5fr) repeat(var(--offer-count,3),minmax(82px,.5fr))',1)
pattern=r'function renderOffersFit\(r\)\{.*?\}\nfunction showResult\(\)\{'
new='''function renderOffersFit(r){
  const section=$(\'offersFitSection\'),table=$(\'offersFitTable\'),plans=$(\'offersFitPlans\');
  if(!section||!table||!plans)return;
  const levels=r.optimizationLevels||{};
  const items=[...(levels.critical||[]),...(levels.structuring||[]),...(levels.advanced||[])];
  if(!items.length){section.hidden=true;return}
  const norm=v=>String(v||\'\').toLowerCase().normalize(\'NFD\').replace(/[\\u0300-\\u036f]/g,\'\');
  const offerFloor=x=>{
    const t=norm(x.text);
    const signature=[\'plusieurs workflows\',\'plusieurs workflow\',\'rythmes differents\',\'plusieurs conditions\',\'reactiver automatiquement\',\'reactivation automatique\',\'fidelisation automatisee\',\'automatiser la fidelisation\',\'segmenter les communications\',\'communication segmentee\',\'type de client\',\'orchestrer plusieurs parcours\',\'orchestration\',\'logique conditionnelle complexe\'];
    const plus=[\'plusieurs parcours\',\'3 parcours\',\'4 parcours\',\'5 parcours\',\'parcours differents\',\'parcours distincts\',\'ressaisie\',\'ressaisies\',\'double saisie\',\'synchronis\',\'plusieurs canaux\',\'coordonner les actions\',\'echeances importantes\',\'relier les echeances\',\'adapter les relances\',\'automatiser plusieurs etapes\',\'etapes reellement differentes\',\'structurer separement\'];
    if(signature.some(k=>t.includes(k)))return 2;
    if(plus.some(k=>t.includes(k)))return 1;
    return 0;
  };
  const maxFloor=Math.max(...items.map(offerFloor));
  const catalog={essentiel:{key:\'essentiel\',name:\'ESSENTIEL\',price:\'2 500 € Net\',floor:0},plus:{key:\'plus\',name:\'ESSENTIEL+\',price:\'4 000 € Net\',floor:1},signature:{key:\'signature\',name:\'SIGNATURE\',price:\'9 000 € Net\',floor:2}};
  const visibleOffers=maxFloor===2?[catalog.plus,catalog.signature]:[catalog.essentiel,catalog.plus];
  section.style.setProperty(\'--offer-count\',String(visibleOffers.length));
  const priority=x=>x.priority>=85?{label:\'Critique\',cls:\'critical\'}:x.priority>=70?{label:\'Structurante\',cls:\'structuring\'}:{label:\'Avancée\',cls:\'advanced\'};
  const covered=(x,o)=>o.floor>=offerFloor(x);
  const mark=v=>`<div class="offers-fit-cell offers-fit-mark ${v?\'yes\':\'no\'}">${v?\'✓\':\'—\'}</div>`;
  table.innerHTML=`<div class="offers-fit-row"><div class="offers-fit-cell offers-fit-head">Optimisations identifiées chez vous</div>${visibleOffers.map(o=>`<div class="offers-fit-cell offers-fit-head">${o.name}</div>`).join(\'\')}</div>`+items.map(x=>{const p=priority(x);return `<div class="offers-fit-row"><div class="offers-fit-cell"><div class="offers-fit-opt"><strong>${x.text}</strong><small class="offers-fit-badge ${p.cls}">${p.label}</small></div></div>${visibleOffers.map(o=>mark(covered(x,o))).join(\'\')}</div>`}).join(\'\');
  const recommended=maxFloor===0?\'essentiel\':maxFloor===1?\'plus\':\'signature\';
  const status=o=>o.key===recommended?\'La plus adaptée\':(o.floor<maxFloor?\'Couvre une partie de vos besoins\':\'Couvre également vos besoins\');
  const desc=o=>{if(o.key===\'essentiel\')return o.key===recommended?\'Couvre l’ensemble des besoins identifiés dans un parcours simple.\':\'Couvre les besoins les plus simples de votre diagnostic.\';if(o.key===\'plus\')return o.key===recommended?\'Couvre l’ensemble des optimisations identifiées dans votre fonctionnement.\':\'Va plus loin dans la structuration et l’automatisation.\';return \'Couvre également les optimisations avancées et les logiques complexes identifiées.\';};
  plans.innerHTML=visibleOffers.map(o=>`<article class="offers-fit-plan ${o.key===\'signature\'?\'signature \':\'\'}${o.key===recommended?\'recommended\':\'\'}"><span class="fit-status">${status(o)}</span><h3>${o.name}</h3><strong>${o.price}</strong><p>${desc(o)}</p></article>`).join(\'\');
  section.hidden=false
}
function showResult(){'''
s2,n=re.subn(pattern,lambda m:new,s,count=1,flags=re.S)
if n!=1: raise SystemExit('renderOffersFit function not found')
p.write_text(s2)
