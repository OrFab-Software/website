from pathlib import Path
import re
p=Path('simulation.html')
s=p.read_text(encoding='utf-8')
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
   const offer=max===0?'ESSENTIEL':max===1?'ESSENTIEL+':'SIGNATURE';
   const price=max===0?'autour de 2 500 €':max===1?'autour de 4 000 €':'autour de 9 000 €';
   let card=section.querySelector('.orfab-recommendation-card');
   if(!card){card=document.createElement('div');card.className='orfab-recommendation-card';const cta=section.querySelector('.offers-fit-cta-wrap');if(cta)cta.before(card);else table.after(card)}
   card.innerHTML=`<div><div class="orfab-reco-kicker">Notre recommandation</div><h3 class="orfab-reco-title">Votre projet se situe probablement dans l’offre <strong>${offer}</strong></h3><div class="orfab-reco-price">${price}</div><p class="orfab-reco-note">Cette estimation tient compte des optimisations que vous avez indiqué vouloir approfondir. Le prix exact sera précisé lors de l’échange, selon la manière dont ces besoins s’articulent dans votre fonctionnement.</p></div><div class="orfab-reco-benefits"><div class="orfab-reco-benefit"><span class="orfab-reco-check">✓</span><span>Un CRM entièrement adapté à votre activité</span></div><div class="orfab-reco-benefit"><span class="orfab-reco-check">✓</span><span>Les optimisations que vous souhaitez approfondir prises en compte</span></div><div class="orfab-reco-benefit"><span class="orfab-reco-check">✓</span><span>Un accompagnement de la conception à la mise en main</span></div></div>`;
 }
 const old=window.renderOffersFit;
 window.renderOffersFit=function(r){if(old)old(r);const l=r.optimizationLevels||{};currentItems=[...(l.critical||[]),...(l.structuring||[]),...(l.advanced||[])];removeCard()};
 document.addEventListener('click',e=>{const b=e.target.closest&&e.target.closest('.interest-toggle');if(!b)return;setTimeout(refreshCard,0)});
})();
</script>'''
pat=r'<script id="orfab-recommendation-card-script">.*?</script>'
s2,n=re.subn(pat,new_js,s,count=1,flags=re.S)
if n!=1: raise SystemExit('recommendation script not found')
p.write_text(s2,encoding='utf-8')
