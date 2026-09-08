from pathlib import Path

p = Path('simulation.html')
s = p.read_text(encoding='utf-8')

css = r'''
.summary-icon-badge{display:inline-grid;place-items:center;flex:0 0 auto;width:42px;height:42px;border-radius:50%;background:rgba(242,238,229,.82);color:var(--blue);vertical-align:middle;box-shadow:inset 0 0 0 1px rgba(16,36,58,.08)}
.summary-icon-badge svg{width:27px;height:27px;display:block;stroke:currentColor;fill:none;stroke-width:2.1;stroke-linecap:round;stroke-linejoin:round}
.phase-summary-head .summary-icon-badge{width:60px;height:60px;margin:0 0 14px;background:rgba(242,238,229,.88)}
.phase-summary-head .summary-icon-badge svg{width:38px;height:38px;stroke-width:2}
.summary-heading-with-icon{display:flex!important;align-items:center;gap:12px}
.phase-summary-head.summary-head-with-icon{align-items:flex-start}
'''

js = r'''
<script id="orfab-summary-icons-v2">
(function(){
  const I={
    prospect:`<svg viewBox="0 0 32 32"><circle cx="10" cy="10" r="4"/><circle cx="22" cy="11" r="3.5"/><path d="M3 26v-4a7 7 0 0 1 14 0v4M18 26v-3.5a5 5 0 0 1 8.5-3.5"/><path d="M20 5h7M24 2l3 3-3 3"/></svg>`,
    qualification:`<svg viewBox="0 0 32 32"><circle cx="12" cy="9" r="4"/><path d="M5 25v-4a7 7 0 0 1 14 0v4"/><circle cx="24" cy="22" r="5"/><path d="M21.5 22l1.7 1.7 3.3-3.5"/></svg>`,
    journey:`<svg viewBox="0 0 32 32"><path d="M4 21h20"/><circle cx="5" cy="21" r="2.7"/><circle cx="12" cy="21" r="2.7"/><circle cx="19" cy="21" r="2.7"/><circle cx="26" cy="21" r="2.7"/><path d="M26 18V8M26 8h5l-2 2 2 2h-5"/></svg>`,
    loyalty:`<svg viewBox="0 0 32 32"><path d="M16 27s-10-5.8-10-13a5.5 5.5 0 0 1 10-3.2A5.5 5.5 0 0 1 26 14c0 7.2-10 13-10 13z"/><path d="M11 16h10M16 11v10"/></svg>`,
    channels:`<svg viewBox="0 0 32 32"><circle cx="16" cy="16" r="3"/><circle cx="5" cy="7" r="2.5"/><circle cx="27" cy="7" r="2.5"/><circle cx="5" cy="25" r="2.5"/><circle cx="27" cy="25" r="2.5"/><path d="M7 9l6.5 5M25 9l-6.5 5M7 23l6.5-5M25 23l-6.5-5"/></svg>`,
    followup:`<svg viewBox="0 0 32 32"><rect x="6" y="4" width="20" height="24" rx="3"/><path d="M10 10h9M10 16h9M10 22h7"/><path d="M21 20l2 2 4-5"/></svg>`,
    volume:`<svg viewBox="0 0 32 32"><path d="M6 26V17M13 26V11M20 26V6M27 26V14"/></svg>`,
    warning:`<svg viewBox="0 0 32 32"><path d="M16 4l13 23H3L16 4z"/><path d="M16 11v8M16 23h.01"/></svg>`,
    centralisation:`<svg viewBox="0 0 32 32"><circle cx="16" cy="16" r="3" fill="currentColor" stroke="none"/><path d="M16 3v8M16 21v8M3 16h8M21 16h8"/><path d="M13 8l3 3 3-3M13 24l3-3 3 3M8 13l3 3-3 3M24 13l-3 3 3 3"/></svg>`,
    contact:`<svg viewBox="0 0 32 32"><path d="M8 5l5 5-3 4c2 4 4 6 8 8l4-3 5 5-3 4c-1 1-3 1-5 0C10 24 7 21 4 12c-1-2-1-4 0-5l4-2z"/></svg>`,
    trigger:`<svg viewBox="0 0 32 32"><circle cx="8" cy="9" r="4"/><path d="M2.5 25v-4.5A5.5 5.5 0 0 1 8 15h1"/><circle cx="23" cy="9" r="4"/><path d="M17 25v-4.5a5.5 5.5 0 0 1 5.5-5.5H25"/><path d="M12 11h7M16 8l3 3-3 3"/><circle cx="25" cy="24" r="5"/><path d="M22.5 24l1.7 1.7 3.3-3.5"/></svg>`,
    documents:`<svg viewBox="0 0 32 32"><path d="M7 5h11l7 7v15H7z"/><path d="M18 5v7h7M11 18h10M11 23h8"/></svg>`,
    prepare:`<svg viewBox="0 0 32 32"><path d="M7 5h11l7 7v15H7z"/><path d="M18 5v7h7M11 20h6"/><path d="M21 17l5 5M23.5 14.5l3 3"/></svg>`,
    actions:`<svg viewBox="0 0 32 32"><path d="M17 2l-5 9h5l-2 7 6-10h-5l1-6z" fill="currentColor" stroke="none"/><path d="M16 18v4M16 22l-8 4M16 22l8 4"/><rect x="4" y="24" width="8" height="5" rx="1"/><rect x="12" y="24" width="8" height="5" rx="1"/><rect x="20" y="24" width="8" height="5" rx="1"/></svg>`,
    services:`<svg viewBox="0 0 32 32"><path d="M7 10V7a3 3 0 0 1 3-3h12a3 3 0 0 1 3 3v3"/><rect x="3" y="9" width="26" height="19" rx="3"/><path d="M3 15h26"/><path d="M10 21l3-3M12 23l3-3"/><circle cx="21.5" cy="21.5" r="3"/><path d="M21.5 17v2M21.5 24v2M17 21.5h2M24 21.5h2"/></svg>`,
    double:`<svg viewBox="0 0 32 32"><rect x="4" y="7" width="18" height="14" rx="2"/><rect x="10" y="12" width="18" height="14" rx="2"/><path d="M8 11h8M14 16h8M14 20h6"/></svg>`,
    deadline:`<svg viewBox="0 0 32 32"><circle cx="16" cy="16" r="12"/><path d="M16 9v8l5 3"/></svg>`,
    organization:`<svg viewBox="0 0 32 32"><circle cx="16" cy="6" r="3"/><circle cx="7" cy="25" r="3"/><circle cx="16" cy="25" r="3"/><circle cx="25" cy="25" r="3"/><path d="M16 9v6M7 18h18M7 18v4M16 15v7M25 18v4"/></svg>`,
    tracking:`<svg viewBox="0 0 32 32"><path d="M3 11s4.5-6 13-6 13 6 13 6-4.5 6-13 6S3 11 3 11z"/><circle cx="16" cy="11" r="3"/><path d="M4 25h24"/><circle cx="6" cy="25" r="2" fill="currentColor" stroke="none"/><circle cx="13" cy="25" r="2" fill="currentColor" stroke="none"/><circle cx="20" cy="25" r="2" fill="currentColor" stroke="none"/><circle cx="27" cy="25" r="2.8"/></svg>`,
    recurring:`<svg viewBox="0 0 32 32"><path d="M25 9a11 11 0 1 0 1 13"/><path d="M25 4v5h-5M27 28v-6h-6"/></svg>`,
    order:`<svg viewBox="0 0 32 32"><path d="M11 8h16M11 16h16M11 24h16"/><circle cx="5" cy="8" r="2"/><circle cx="5" cy="16" r="2"/><circle cx="5" cy="24" r="2"/></svg>`,
    review:`<svg viewBox="0 0 32 32"><path d="M16 4l3.5 7 7.5 1-5.5 5.3 1.3 7.5L16 21l-6.8 3.8 1.3-7.5L5 12l7.5-1L16 4z"/></svg>`,
    message:`<svg viewBox="0 0 32 32"><path d="M5 6h22v16H12l-7 5z"/><path d="M10 12h12M10 17h9"/></svg>`,
    reactivation:`<svg viewBox="0 0 32 32"><circle cx="16" cy="16" r="10"/><path d="M16 10v6l4 3M4 8v7h7"/><path d="M7 11a11 11 0 0 1 19 2"/></svg>`
  };
  const normalize=t=>(t||'').trim().toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'');
  function badge(svg){const span=document.createElement('span');span.className='summary-icon-badge';span.innerHTML=svg;return span;}
  function iconFor(t){
    if(t.includes('canaux')||t.includes('entree')) return I.channels;
    if(t.includes('relance')) return I.followup;
    if(t.includes('volume')) return I.volume;
    if(t.includes('risque')||t.includes('oubli')) return I.warning;
    if(t.includes('centralisation')) return I.centralisation;
    if(t.includes('premier contact')) return I.contact;
    if(t.includes('declencheur client')) return I.trigger;
    if(t.includes('preparation')&&t.includes('document')) return I.prepare;
    if(t.includes('document')) return I.documents;
    if(t.includes('actions declenchees')) return I.actions;
    if(t.includes('prestations')) return I.services;
    if(t.includes('double saisie')||t.includes('ressaisie')) return I.double;
    if(t.includes('echeance')) return I.deadline;
    if(t.includes('organisation')&&t.includes('parcours')) return I.organization;
    if(t.includes('suivi de la prestation')) return I.tracking;
    if(t.includes('actions recurrentes')) return I.recurring;
    if(t.includes('ordre des etapes')) return I.order;
    if(t.includes('avis')) return I.review;
    if(t.includes('message')||t.includes('communication')) return I.message;
    if(t.includes('reactiv')) return I.reactivation;
    return null;
  }
  function headIcon(t){
    if(t.includes('parcours prospect')) return I.prospect;
    if(t.includes('qualification')) return I.qualification;
    if(t.includes('parcours client')) return I.journey;
    if(t.includes('fidelisation')) return I.loyalty;
    return null;
  }
  function apply(){
    document.querySelectorAll('.phase-summary-card').forEach(card=>{
      const head=card.querySelector('.phase-summary-head');
      const h3=head&&head.querySelector('h3');
      if(h3 && !head.querySelector('.summary-icon-badge')){
        const icon=headIcon(normalize(h3.textContent));
        if(icon){head.classList.add('summary-head-with-icon');h3.before(badge(icon));}
      }
      card.querySelectorAll('.phase-summary-row h4').forEach(h4=>{
        if(h4.dataset.iconified==='1') return;
        const icon=iconFor(normalize(h4.textContent));
        if(icon){h4.dataset.iconified='1';h4.classList.add('summary-heading-with-icon');h4.prepend(badge(icon));}
      });
    });
  }
  apply();
  const target=document.getElementById('phaseSummary');
  if(target) new MutationObserver(apply).observe(target,{childList:true,subtree:true});
})();
</script>
'''

# Remove the previous icon script if present, then inject the complete version.
import re
s = re.sub(r'<script id="orfab-summary-icons">.*?</script>\s*', '', s, flags=re.S)
s = re.sub(r'<script id="orfab-summary-icons-v2">.*?</script>\s*', '', s, flags=re.S)
if 'summary-icon-badge{' not in s:
    s = s.replace('</style>', css + '\n</style>', 1)
s = s.replace('</body>', js + '\n</body>', 1)

p.write_text(s, encoding='utf-8')
