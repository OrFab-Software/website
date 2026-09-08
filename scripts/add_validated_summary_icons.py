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
<script id="orfab-summary-icons">
(function(){
  const icons={
    centralisation:`<svg viewBox="0 0 32 32" aria-hidden="true"><circle cx="16" cy="16" r="3" fill="currentColor" stroke="none"/><path d="M16 3v8M16 21v8M3 16h8M21 16h8"/><path d="M13 8l3 3 3-3M13 24l3-3 3 3M8 13l3 3-3 3M24 13l-3 3 3 3"/></svg>`,
    trigger:`<svg viewBox="0 0 32 32" aria-hidden="true"><circle cx="8" cy="9" r="4"/><path d="M2.5 25v-4.5A5.5 5.5 0 0 1 8 15h1"/><circle cx="23" cy="9" r="4"/><path d="M17 25v-4.5a5.5 5.5 0 0 1 5.5-5.5H25"/><path d="M12 11h7M16 8l3 3-3 3"/><circle cx="25" cy="24" r="5"/><path d="M22.5 24l1.7 1.7 3.3-3.5"/></svg>`,
    actions:`<svg viewBox="0 0 32 32" aria-hidden="true"><path d="M17 2l-5 9h5l-2 7 6-10h-5l1-6z" fill="currentColor" stroke="none"/><path d="M16 18v4M16 22l-8 4M16 22l8 4"/><rect x="4" y="24" width="8" height="5" rx="1"/><rect x="12" y="24" width="8" height="5" rx="1"/><rect x="20" y="24" width="8" height="5" rx="1"/></svg>`,
    journey:`<svg viewBox="0 0 32 32" aria-hidden="true"><path d="M4 21h20"/><circle cx="5" cy="21" r="2.7"/><circle cx="12" cy="21" r="2.7"/><circle cx="19" cy="21" r="2.7"/><circle cx="26" cy="21" r="2.7"/><path d="M26 18V8M26 8h5l-2 2 2 2h-5"/></svg>`,
    services:`<svg viewBox="0 0 32 32" aria-hidden="true"><path d="M7 10V7a3 3 0 0 1 3-3h12a3 3 0 0 1 3 3v3"/><rect x="3" y="9" width="26" height="19" rx="3"/><path d="M3 15h26"/><path d="M10 21l3-3M12 23l3-3"/><circle cx="21.5" cy="21.5" r="3"/><path d="M21.5 17v2M21.5 24v2M17 21.5h2M24 21.5h2"/></svg>`,
    tracking:`<svg viewBox="0 0 32 32" aria-hidden="true"><path d="M3 11s4.5-6 13-6 13 6 13 6-4.5 6-13 6S3 11 3 11z"/><circle cx="16" cy="11" r="3"/><path d="M4 25h24"/><circle cx="6" cy="25" r="2" fill="currentColor" stroke="none"/><circle cx="13" cy="25" r="2" fill="currentColor" stroke="none"/><circle cx="20" cy="25" r="2" fill="currentColor" stroke="none"/><circle cx="27" cy="25" r="2.8"/></svg>`
  };
  const normalize=t=>(t||'').trim().toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'');
  function badge(svg){const span=document.createElement('span');span.className='summary-icon-badge';span.innerHTML=svg;return span;}
  function apply(){
    document.querySelectorAll('.phase-summary-card').forEach(card=>{
      const head=card.querySelector('.phase-summary-head');
      const h3=head&&head.querySelector('h3');
      if(h3 && normalize(h3.textContent)==='parcours client' && !head.querySelector('.summary-icon-badge')){
        head.classList.add('summary-head-with-icon');
        h3.before(badge(icons.journey));
      }
      card.querySelectorAll('.phase-summary-row h4').forEach(h4=>{
        if(h4.dataset.iconified==='1') return;
        const t=normalize(h4.textContent);
        let icon=null;
        if(t==='centralisation') icon=icons.centralisation;
        else if(t==='declencheur client') icon=icons.trigger;
        else if(t==='actions declenchees') icon=icons.actions;
        else if(t==='vos prestations') icon=icons.services;
        else if(t==='suivi de la prestation') icon=icons.tracking;
        if(icon){
          h4.dataset.iconified='1';
          h4.classList.add('summary-heading-with-icon');
          h4.prepend(badge(icon));
        }
      });
    });
  }
  apply();
  const target=document.getElementById('phaseSummary');
  if(target) new MutationObserver(apply).observe(target,{childList:true,subtree:true});
})();
</script>
'''

if 'summary-icon-badge{' not in s:
    s = s.replace('</style>', css + '\n</style>', 1)
if 'id="orfab-summary-icons"' not in s:
    s = s.replace('</body>', js + '\n</body>', 1)

p.write_text(s, encoding='utf-8')
