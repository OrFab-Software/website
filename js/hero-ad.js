(() => {
  const stage = document.querySelector('.workflow-stage');
  if (!stage) return;

  const logo = `
    <svg viewBox="0 0 100 100" aria-hidden="true">
      <path d="M19 22 39 10 48 28 34 39 13 36Z" fill="#b7b9bd"/>
      <path d="M61 10 82 23 87 39 65 39 52 28Z" fill="#d6a13b"/>
      <path d="M88 49 84 72 65 86 55 68 68 54Z" fill="#b67f23"/>
      <path d="M55 72 65 88 42 92 20 81 32 63Z" fill="#185cc6"/>
      <path d="M13 43 30 47 29 62 17 78 8 59Z" fill="#8d9197"/>
      <circle cx="50" cy="50" r="16" fill="#0c0f13"/>
    </svg>`;

  stage.className = 'ad-stage';
  stage.innerHTML = `
    <div class="ad-kicker">UN EXEMPLE — VOTRE OUTIL S’ADAPTE À VOTRE ACTIVITÉ</div>

    <section class="ad-scene ad-scene--chaos" aria-hidden="true">
      <div class="chaos-pulse"></div>
      <div class="chaos-card chaos-card--instagram"><i>◎</i><span>Instagram</span></div>
      <div class="chaos-card chaos-card--mail"><i>✉</i><span>E-mails</span></div>
      <div class="chaos-card chaos-card--agenda"><i>▣</i><span>Agenda</span></div>
      <div class="chaos-card chaos-card--quote"><i>▤</i><span>Devis</span></div>
      <div class="chaos-card chaos-card--docs"><i>▰</i><span>Documents</span></div>
      <div class="chaos-card chaos-card--pay"><i>€</i><span>Paiements</span></div>
      <div class="chaos-copy">
        <small>Votre quotidien aujourd’hui</small>
        <strong>Tout suivre. Tout retenir.<br><em>Tout relancer.</em></strong>
      </div>
    </section>

    <section class="ad-scene ad-scene--brand" aria-hidden="true">
      <div class="brand-reveal">
        <div class="brand-reveal__halo"></div>
        <div class="brand-rings"></div>
        <div>
          <div class="brand-reveal__mark">${logo}<span>OrFab</span></div>
          <p>Votre activité se met en ordre, <b>autour de votre façon de travailler.</b></p>
        </div>
      </div>
    </section>

    <section class="ad-scene ad-scene--order" aria-hidden="true">
      <div class="order-title">Vous gardez la décision. <b>OrFab orchestre le reste.</b></div>
      <svg class="order-lines" viewBox="0 0 760 500" aria-hidden="true">
        <path class="order-line order-line--purple" d="M380 75 C380 120 380 145 380 175"/>
        <path class="order-line order-line--blue" d="M380 225 C310 270 175 265 145 330"/>
        <path class="order-line order-line--gold" d="M380 225 C380 270 380 295 380 330"/>
        <path class="order-line order-line--blue" d="M380 225 C450 270 585 265 615 330"/>
        <path class="order-line order-line--gold" d="M380 370 C380 405 380 420 380 448"/>
      </svg>
      <div class="order-node order-node--request"><i>✦</i><span>Nouvelle demande</span></div>
      <div class="order-core">${logo}<span>OrFab</span></div>
      <div class="order-node order-node--rdv"><i>▣</i><span>Rendez-vous</span></div>
      <div class="order-node order-node--quote"><i>▤</i><span>Devis</span></div>
      <div class="order-node order-node--docs"><i>▰</i><span>Documents</span></div>
      <div class="order-status order-status--validate">À VALIDER</div>
      <div class="order-status order-status--auto">AUTOMATISÉ</div>
      <div class="order-status order-status--assist">ASSISTÉ</div>
      <div class="order-node order-node--client"><i>●</i><span>Client suivi</span></div>
      <div class="order-message">Moins à mémoriser. Plus de visibilité. Vous gardez la main.</div>
    </section>

    <section class="ad-scene ad-scene--final" aria-hidden="true">
      <div class="final-frame">
        <div class="final-frame__glow"></div>
        <h2>Votre activité.<br>Votre façon de travailler.<span>Votre logiciel.</span></h2>
        <div class="final-frame__rule"></div>
        <div class="final-frame__brand">${logo}<span>OrFab</span></div>
        <small>Comprendre · Optimiser · Construire</small>
      </div>
    </section>`;
})();
