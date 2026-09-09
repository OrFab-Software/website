from pathlib import Path
import re

p=Path('simulation.html')
s=p.read_text(encoding='utf-8')

section_pat=r'(<section class="offers-fit" id="offersFitSection" hidden>)<h2>.*?</h2><p class="offers-fit-lead">.*?</p>'
section_html='''<h2>Les optimisations identifiées</h2><p class="offers-fit-lead"><strong>Sélectionnez celles que vous souhaiteriez réellement traiter.</strong><br>La simulation a identifié plusieurs pistes d’amélioration dans votre fonctionnement. Votre sélection sert uniquement à estimer l’ampleur du projet : elle ne compose pas un pack de fonctionnalités. Chaque solution OrFab est conçue sur mesure. Le périmètre exact et le tarif définitif sont déterminés lors de l’appel visio, une fois votre besoin précisément défini.</p>'''
s,n=re.subn(section_pat,lambda m:m.group(1)+section_html,s,count=1,flags=re.S)
if n!=1: raise SystemExit('offers fit intro not found')

new_js=r'''<script id="orfab-recommendation-card-script">
(function(){
 const norm=t=>(t||'').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'');
 function floorFor(x){const t=norm((x.text||'')+' '+(x.why||''));if(/plusieurs workflow|differents rythmes|reactiv|fidelis|segment|plusieurs conditions|type de client|orchestr|automatisation avancee|parcours complexes/.test(t))return 2;if(/plusieurs parcours|\d+ parcours|ressaisi|etapes reellement differentes|coordonner les actions|plusieurs canaux|synchronis|adapter les relances|automatiser plusieurs etapes|double saisie|personnalis.*document|document.*automati/.test(t))return 1;return 0}
 let currentItems=[];
 function removeCard(){const card=document.querySelector('#offersFitSection .orfab-recommendation-card');if(card)card.remove()}
 function refreshCard(){
   const section=document.getElementById('offersFitSection'),table=document.getElementById('offersFitTable');
   if(!section||!table)return;
   const selected=[...table.querySelectorAll('.interest-toggle[aria-pressed="true"]')]
     .map(b=>currentItems[Number(b.dataset.interest)]).filter(Boolean);
   if(!selected.length){removeCard();return}
   const max=Math.max(...selected.map(floorFor));
   const price=max===0?'autour de 2 500 €':max===1?'autour de 4 000 €':'autour de 9 000 €';
   let card=section.querySelector('.orfab-recommendation-card');
   if(!card){card=document.createElement('div');card.className='orfab-recommendation-card';const cta=section.querySelector('.offers-fit-cta-wrap');if(cta)cta.before(card);else table.after(card)}
   card.innerHTML=`<div><div class="orfab-reco-kicker">Notre estimation</div><h3 class="orfab-reco-title">Votre projet sur mesure est estimé</h3><div class="orfab-reco-price">${price}</div><p class="orfab-reco-note">Cette estimation tient compte des optimisations que vous avez sélectionnées. Elle vous donne un ordre de grandeur, pas un devis. Le périmètre exact et le tarif définitif seront déterminés avec vous lors de l’appel visio, après analyse de votre fonctionnement.</p></div><div class="orfab-reco-benefits"><div class="orfab-reco-benefit"><span class="orfab-reco-check">✓</span><span>Une solution entièrement conçue autour de votre activité</span></div><div class="orfab-reco-benefit"><span class="orfab-reco-check">✓</span><span>Les optimisations retenues intégrées dans un fonctionnement cohérent</span></div><div class="orfab-reco-benefit"><span class="orfab-reco-check">✓</span><span>Le tarif final défini avec vous lors de l’appel visio</span></div></div>`;
 }
 const old=window.renderOffersFit;
 window.renderOffersFit=function(r){if(old)old(r);const l=r.optimizationLevels||{};currentItems=[...(l.critical||[]),...(l.structuring||[]),...(l.advanced||[])];removeCard()};
 document.addEventListener('click',e=>{const b=e.target.closest&&e.target.closest('.interest-toggle');if(!b)return;setTimeout(refreshCard,0)});
})();
</script>'''
pat=r'<script id="orfab-recommendation-card-script">.*?</script>'
s2,n=re.subn(pat,lambda m:new_js,s,count=1,flags=re.S)
if n!=1: raise SystemExit('recommendation script not found')
p.write_text(s2,encoding='utf-8')
