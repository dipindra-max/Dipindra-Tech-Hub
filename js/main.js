// TechPulse Hub — shared site behavior
document.addEventListener('DOMContentLoaded', function () {

  // Mobile nav toggle
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.querySelector('.main-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  // Footer year
  document.querySelectorAll('[data-year]').forEach(function (el) {
    el.textContent = new Date().getFullYear();
  });

  // Reading progress bar (article pages)
  var bar = document.querySelector('.reading-bar');
  if (bar) {
    window.addEventListener('scroll', function () {
      var h = document.documentElement;
      var scrollTop = h.scrollTop || document.body.scrollTop;
      var scrollHeight = (h.scrollHeight || document.body.scrollHeight) - h.clientHeight;
      var pct = scrollHeight > 0 ? (scrollTop / scrollHeight) * 100 : 0;
      bar.value = pct;
    });
  }

  // Simple client-side blog search/filter (used on blog.html)
  var searchInput = document.getElementById('blog-search');
  if (searchInput) {
    searchInput.addEventListener('input', function () {
      var q = searchInput.value.trim().toLowerCase();
      document.querySelectorAll('[data-post-card]').forEach(function (card) {
        var text = card.getAttribute('data-search') || card.textContent;
        card.style.display = text.toLowerCase().indexOf(q) !== -1 ? '' : 'none';
      });
    });
  }

  // Category filter chips (used on blog.html)
  document.querySelectorAll('[data-filter]').forEach(function (chip) {
    chip.addEventListener('click', function () {
      document.querySelectorAll('[data-filter]').forEach(function (c) { c.classList.remove('active'); });
      chip.classList.add('active');
      var cat = chip.getAttribute('data-filter');
      document.querySelectorAll('[data-post-card]').forEach(function (card) {
        var cardCat = card.getAttribute('data-category');
        card.style.display = (cat === 'all' || cardCat === cat) ? '' : 'none';
      });
    });
  });

  // Newsletter form (static demo — replace action with real endpoint)
  var newsletterForm = document.getElementById('newsletter-form');
  if (newsletterForm) {
    newsletterForm.addEventListener('submit', function (e) {
      e.preventDefault();
      var msg = document.getElementById('newsletter-msg');
      if (msg) msg.textContent = 'Thanks for subscribing! Please check your inbox to confirm.';
      newsletterForm.reset();
    });
  }

  // Contact form (static demo — replace action with real endpoint / Formspree / etc.)
  var contactForm = document.getElementById('contact-form');
  if (contactForm) {
    contactForm.addEventListener('submit', function (e) {
      e.preventDefault();
      var msg = document.getElementById('contact-msg');
      if (msg) msg.textContent = 'Thanks for reaching out! This is a demo form — connect it to a form service (see README) to receive real messages.';
      contactForm.reset();
    });
  }
});
