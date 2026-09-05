(() => {
  const section = document.querySelector('.of-offers');
  if (!section) return;

  const cards = [...section.querySelectorAll('.of-offer')];
  const dots = [...section.querySelectorAll('[data-offer-dot]')];
  const prev = section.querySelector('.of-offers__arrow--prev');
  const next = section.querySelector('.of-offers__arrow--next');
  const grid = section.querySelector('.of-offers__grid');
  if (!cards.length || !prev || !next || !grid) return;

  let activeIndex = 1;

  const render = () => {
    cards.forEach((card, index) => {
      const active = index === activeIndex;
      card.classList.toggle('is-active', active);
      if (active) card.setAttribute('aria-current', 'true');
      else card.removeAttribute('aria-current');
    });

    dots.forEach((dot, index) => {
      const active = index === activeIndex;
      dot.classList.toggle('is-active', active);
      if (active) dot.setAttribute('aria-current', 'true');
      else dot.removeAttribute('aria-current');
    });

    if (window.matchMedia('(max-width: 900px)').matches) {
      const carousel = section.querySelector('.of-offers__carousel');
      const availableWidth = carousel ? carousel.clientWidth - 84 : grid.clientWidth;
      const gap = 14;
      grid.style.transform = `translateX(-${activeIndex * (availableWidth + gap)}px)`;
    } else {
      grid.style.transform = '';
    }
  };

  const move = (direction) => {
    activeIndex = (activeIndex + direction + cards.length) % cards.length;
    render();
  };

  prev.addEventListener('click', () => move(-1));
  next.addEventListener('click', () => move(1));

  dots.forEach((dot, index) => {
    dot.addEventListener('click', () => {
      activeIndex = index;
      render();
    });
  });

  cards.forEach((card, index) => {
    card.addEventListener('click', (event) => {
      if (event.target.closest('a, button')) return;
      if (index !== activeIndex) {
        activeIndex = index;
        render();
      }
    });
  });

  window.addEventListener('resize', render);
  render();
})();