const menuButton = document.querySelector('.menu-toggle');
const siteNavigation = document.querySelector('#site-nav');
const pageLoader = document.querySelector('#page-loader');
const loaderMessage = document.querySelector('#loader-message');
const loadingMessages = [
  'Preparando seu próximo detalhe',
  'Organizando as melhores escolhas',
  'Quase tudo no lugar',
];
let loaderTimer;
let messageTimer;

if (menuButton && siteNavigation) {
  menuButton.addEventListener('click', () => {
    const expanded = menuButton.getAttribute('aria-expanded') === 'true';
    menuButton.setAttribute('aria-expanded', String(!expanded));
    menuButton.setAttribute('aria-label', expanded ? 'Abrir menu' : 'Fechar menu');
    siteNavigation.classList.toggle('is-open', !expanded);
    menuButton.querySelector('use')?.setAttribute('href', expanded ? '#icon-menu' : '#icon-close');
  });
}

function startPageLoading() {
  if (!pageLoader || loaderTimer) return;
  let messageIndex = 0;
  loaderTimer = window.setTimeout(() => {
    pageLoader.classList.add('is-visible');
    pageLoader.setAttribute('aria-hidden', 'false');
    document.body.setAttribute('aria-busy', 'true');
    messageTimer = window.setInterval(() => {
      messageIndex = (messageIndex + 1) % loadingMessages.length;
      loaderMessage.textContent = loadingMessages[messageIndex];
    }, 1250);
  }, 400);
}

function stopPageLoading() {
  window.clearTimeout(loaderTimer);
  window.clearInterval(messageTimer);
  loaderTimer = undefined;
  messageTimer = undefined;
  pageLoader?.classList.remove('is-visible');
  pageLoader?.setAttribute('aria-hidden', 'true');
  document.body.removeAttribute('aria-busy');
}

document.addEventListener('click', (event) => {
  const link = event.target.closest('a[href]');
  if (!link || event.defaultPrevented || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
  if (link.target === '_blank' || link.hasAttribute('download') || link.origin !== location.origin) return;
  if (link.pathname === location.pathname && link.search === location.search && link.hash) return;
  startPageLoading();
});

let feedbackTimer;

document.addEventListener('submit', async (event) => {
  const form = event.target;
  if (!form.matches('form[data-cart-add]')) {
    if (form.matches('form')) startPageLoading();
    return;
  }

  event.preventDefault();
  const button = form.querySelector('button[type="submit"]');
  const feedback = document.querySelector('#action-feedback');
  button.disabled = true;
  button.setAttribute('aria-busy', 'true');
  startPageLoading();

  try {
    const response = await fetch(form.action, {
      method: 'POST',
      body: new FormData(form),
      credentials: 'same-origin',
      headers: { Accept: 'application/json' },
    });
    if (!response.ok) throw new Error('Não foi possível adicionar esta peça agora.');
    const result = await response.json();
    const cartCount = document.querySelector('.cart-count');
    const cartLink = document.querySelector('.nav-cart');
    if (cartCount) cartCount.textContent = result.cart_count;
    if (cartLink) {
      const unit = result.cart_count === 1 ? 'item' : 'itens';
      cartLink.setAttribute('aria-label', `Pedido, ${result.cart_count} ${unit}`);
    }
    feedback.textContent = result.message;
    feedback.classList.add('is-visible');
    window.clearTimeout(feedbackTimer);
    feedbackTimer = window.setTimeout(() => feedback.classList.remove('is-visible'), 3200);
  } catch (error) {
    feedback.textContent = error.message || 'Não foi possível adicionar esta peça agora.';
    feedback.classList.add('is-visible', 'is-error');
    window.clearTimeout(feedbackTimer);
    feedbackTimer = window.setTimeout(() => feedback.classList.remove('is-visible', 'is-error'), 4200);
  } finally {
    stopPageLoading();
    button.disabled = false;
    button.removeAttribute('aria-busy');
  }
});

window.addEventListener('pageshow', stopPageLoading);

document.querySelectorAll('[data-carousel]').forEach((carousel) => {
  const slides = [...carousel.querySelectorAll('[data-carousel-slide]')];
  if (slides.length < 2) return;

  const interval = Number(carousel.dataset.interval) || 6500;
  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  let activeIndex = 0;
  let timer;
  let pointerStart;

  carousel.style.setProperty('--carousel-duration', `${interval}ms`);

  function showSlide(index) {
    activeIndex = (index + slides.length) % slides.length;
    slides.forEach((slide, slideIndex) => {
      const active = slideIndex === activeIndex;
      slide.hidden = !active;
      slide.setAttribute('aria-hidden', String(!active));
      slide.classList.toggle('is-active', active);
    });
  }

  function stopTimer() {
    window.clearInterval(timer);
  }

  function startTimer() {
    stopTimer();
    if (prefersReducedMotion || document.hidden) return;
    timer = window.setInterval(() => showSlide(activeIndex + 1), interval);
  }

  carousel.addEventListener('mouseenter', stopTimer);
  carousel.addEventListener('mouseleave', startTimer);
  carousel.addEventListener('focusin', stopTimer);
  carousel.addEventListener('focusout', (event) => {
    if (!carousel.contains(event.relatedTarget)) startTimer();
  });

  const media = carousel.querySelector('.carousel-media');
  media?.addEventListener('pointerdown', (event) => {
    pointerStart = event.clientX;
  });
  media?.addEventListener('pointerup', (event) => {
    if (pointerStart === undefined) return;
    const distance = event.clientX - pointerStart;
    startTimer();
    pointerStart = undefined;
    if (Math.abs(distance) < 45) return;
    showSlide(activeIndex + (distance < 0 ? 1 : -1));
  });
  media?.addEventListener('pointercancel', () => {
    pointerStart = undefined;
  });

  document.addEventListener('visibilitychange', () => {
    if (document.hidden) stopTimer();
    else startTimer();
  });
  showSlide(0);
  startTimer();
});
