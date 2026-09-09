from pathlib import Path
import re

p = Path('simulation.html')
s = p.read_text(encoding='utf-8')

css = r'''
/* Simulation save form */
.simulation-save-card{margin:28px 0 6px;padding:30px 32px;border:2px solid var(--gold);border-radius:22px;background:linear-gradient(180deg,#fffdf8,#f4efe4);color:var(--blue);box-shadow:0 12px 30px rgba(16,36,58,.12)}
.simulation-save-card[hidden]{display:none!important}.simulation-save-kicker{font-size:11px;letter-spacing:2.1px;text-transform:uppercase;font-weight:900;color:#607487;margin-bottom:8px}.simulation-save-card h2{font-size:clamp(30px,3.3vw,43px);line-height:1.08;margin:0 0 10px;color:var(--blue)}.simulation-save-lead{max-width:850px;margin:0 0 22px;color:#50677a;line-height:1.6}.simulation-save-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px}.simulation-save-field{display:grid;gap:7px;font-size:13px;font-weight:850;color:#29445c}.simulation-save-field input{width:100%;min-height:52px;border:1.5px solid rgba(16,36,58,.25);border-radius:14px;background:#fff;color:var(--blue);padding:0 15px;font:inherit;font-weight:600;outline:none}.simulation-save-field input:focus{border-color:var(--gold);box-shadow:0 0 0 3px rgba(209,160,71,.18)}.simulation-save-actions{display:flex;align-items:center;gap:18px;flex-wrap:wrap;margin-top:18px}.simulation-save-submit{border:0;border-radius:18px;min-height:56px;padding:0 25px;background:var(--blue);color:var(--cream);font-weight:900;font-size:15px;cursor:pointer}.simulation-save-submit:disabled{opacity:.55;cursor:not-allowed}.simulation-save-status{margin:0;color:#29445c;font-size:14px;font-weight:750}.simulation-save-status.is-error{color:#8b2a2a}.simulation-save-status.is-success{color:#1f6a46}.simulation-save-privacy{margin:14px 0 0;color:#607487;font-size:12px;line-height:1.55;max-width:900px}.simulation-save-honeypot{position:absolute!important;left:-10000px!important;width:1px!important;height:1px!important;overflow:hidden!important}
@media(max-width:800px){.simulation-save-card{padding:24px 22px}.simulation-save-grid{grid-template-columns:1fr}.simulation-save-actions{align-items:stretch;flex-direction:column}.simulation-save-submit{width:100%}}
'''

if '/* Simulation save form */' not in s:
    marker = '</style><style id="optimization-horizontal-override">'
    if marker not in s:
        raise SystemExit('style marker not found')
    s = s.replace(marker, css + '\n</style><style id="optimization-horizontal-override">', 1)

html = r'''
<section class="simulation-save-card" id="simulationSaveCard" hidden>
  <div class="simulation-save-kicker">Sauvegarder votre simulation</div>
  <h2>Gardez une trace de votre diagnostic.</h2>
  <p class="simulation-save-lead">Renseignez simplement votre prénom, votre nom et votre adresse e-mail. Votre simulation complète sera enregistrée et rattachée à votre fiche prospect OrFab.</p>
  <form id="simulationSaveForm" novalidate>
    <div class="simulation-save-grid">
      <label class="simulation-save-field">Prénom<input id="simulationFirstName" name="firstName" type="text" autocomplete="given-name" maxlength="80" required></label>
      <label class="simulation-save-field">Nom<input id="simulationLastName" name="lastName" type="text" autocomplete="family-name" maxlength="80" required></label>
      <label class="simulation-save-field">Adresse e-mail<input id="simulationEmail" name="email" type="email" autocomplete="email" maxlength="254" required></label>
    </div>
    <label class="simulation-save-honeypot" aria-hidden="true">Site internet<input id="simulationCompanyWebsite" name="companyWebsite" type="text" tabindex="-1" autocomplete="off"></label>
    <div class="simulation-save-actions">
      <button class="simulation-save-submit" id="simulationSaveSubmit" type="submit">Enregistrer ma simulation</button>
      <p class="simulation-save-status" id="simulationSaveStatus" role="status" aria-live="polite"></p>
    </div>
    <p class="simulation-save-privacy">Vos informations sont utilisées pour sauvegarder cette simulation et permettre à OrFab de vous recontacter à son sujet. Cet enregistrement ne vous inscrit à aucune newsletter.</p>
  </form>
</section>
'''

if 'id="simulationSaveCard"' not in s:
    pat = r'(<section class="offers-fit" id="offersFitSection" hidden>.*?</section>)(\s*<div class="result-actions">)'
    s, n = re.subn(pat, lambda m: m.group(1) + '\n' + html + m.group(2), s, count=1, flags=re.S)
    if n != 1:
        raise SystemExit('offers section insertion point not found')

script = r'''
<script src="js/orfab-runtime-config.js"></script>
<script id="orfab-simulation-save-script">
(function(){
  const card=document.getElementById('simulationSaveCard');
  const form=document.getElementById('simulationSaveForm');
  if(!card||!form)return;

  const apiBase=String(window.ORFAB_SIMULATION_API_BASE||'').trim().replace(/\/+$/,'');
  if(!apiBase){card.hidden=true;return}
  card.hidden=false;

  const firstName=document.getElementById('simulationFirstName');
  const lastName=document.getElementById('simulationLastName');
  const email=document.getElementById('simulationEmail');
  const honeypot=document.getElementById('simulationCompanyWebsite');
  const submit=document.getElementById('simulationSaveSubmit');
  const status=document.getElementById('simulationSaveStatus');

  let submissionId='';
  try{submissionId=sessionStorage.getItem('orfab-simulation-submission-id')||''}catch(e){}
  if(!submissionId){
    submissionId=(globalThis.crypto&&crypto.randomUUID)?crypto.randomUUID():`sim-${Date.now()}-${Math.random().toString(36).slice(2)}`;
    try{sessionStorage.setItem('orfab-simulation-submission-id',submissionId)}catch(e){}
  }

  function selectedOptimizations(){
    return [...document.querySelectorAll('#offersFitTable .interest-toggle[aria-pressed="true"]')].map(button=>{
      const row=button.closest('.offers-fit-row');
      return {
        text:row?.querySelector('.offers-fit-opt strong')?.textContent?.trim()||'',
        priority:row?.querySelector('.offers-fit-mark span')?.textContent?.trim()||''
      };
    }).filter(item=>item.text);
  }

  function setStatus(message,type){
    status.textContent=message||'';
    status.classList.toggle('is-error',type==='error');
    status.classList.toggle('is-success',type==='success');
  }

  form.addEventListener('submit',async(event)=>{
    event.preventDefault();
    setStatus('',null);

    if(!firstName.value.trim()||!lastName.value.trim()||!email.value.trim()){
      setStatus('Renseignez votre prénom, votre nom et votre adresse e-mail.','error');
      return;
    }
    if(!email.checkValidity()){
      setStatus('Vérifiez votre adresse e-mail.','error');
      return;
    }

    submit.disabled=true;
    submit.textContent='Enregistrement…';

    let answers={};
    try{answers=JSON.parse(JSON.stringify(state||{}))}catch(e){}
    let result=null;
    try{result=typeof buildResult==='function'?buildResult():null}catch(e){}

    const payload={
      firstName:firstName.value.trim(),
      lastName:lastName.value.trim(),
      email:email.value.trim(),
      companyWebsite:honeypot.value,
      clientSubmissionId:submissionId,
      simulation:{
        version:'2026-09-v1',
        completedAt:new Date().toISOString(),
        answers
      },
      result,
      selectedOptimizations:selectedOptimizations(),
      estimateLabel:document.querySelector('.orfab-reco-price')?.textContent?.trim()||null,
      pageUrl:location.href,
      privacyNoticeVersion:'2026-09-v1'
    };

    try{
      const response=await fetch(`${apiBase}/api/simulations`,{
        method:'POST',
        headers:{'Content-Type':'application/json'},
        body:JSON.stringify(payload)
      });
      const data=await response.json().catch(()=>({}));
      if(!response.ok||!data.ok)throw new Error(data.error||'Enregistrement impossible pour le moment.');

      setStatus('Simulation enregistrée. Elle est maintenant rattachée à votre fiche prospect OrFab.','success');
      submit.textContent='Simulation enregistrée ✓';
      firstName.readOnly=true;lastName.readOnly=true;email.readOnly=true;
      try{localStorage.setItem('orfab-last-saved-simulation',data.simulationId||submissionId)}catch(e){}
    }catch(error){
      submit.disabled=false;
      submit.textContent='Enregistrer ma simulation';
      setStatus(error.message||'Enregistrement impossible pour le moment.','error');
    }
  });

  const restart=document.getElementById('restart');
  if(restart)restart.addEventListener('click',()=>{
    try{sessionStorage.removeItem('orfab-simulation-submission-id')}catch(e){}
  });
})();
</script>
'''

if 'id="orfab-simulation-save-script"' not in s:
    if '</body>' not in s:
        raise SystemExit('body end not found')
    s=s.replace('</body>',script+'\n</body>',1)

p.write_text(s,encoding='utf-8')
