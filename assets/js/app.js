/* Progressive enhancement: the full research record is readable without JS. */
(function () {
  'use strict';
  document.documentElement.classList.add('enhanced');

  var menuButton = document.querySelector('[data-menu-toggle]');
  var menu = document.getElementById('mobile-navigation');
  function setMenu(open, returnFocus) {
    if (!menu || !menuButton) return;
    menu.classList.toggle('is-open', open);
    menuButton.setAttribute('aria-expanded', String(open));
    if (returnFocus) menuButton.focus();
  }
  if (menuButton && menu) {
    menuButton.addEventListener('click', function () {
      setMenu(menuButton.getAttribute('aria-expanded') !== 'true', false);
    });
    document.addEventListener('keydown', function (event) {
      if (event.key === 'Escape' && menuButton.getAttribute('aria-expanded') === 'true') setMenu(false, true);
    });
    document.addEventListener('click', function (event) {
      if (!event.target.closest('.site-header') && menuButton.getAttribute('aria-expanded') === 'true') setMenu(false, menu.contains(document.activeElement));
      if (event.target.closest('#mobile-navigation a')) setMenu(false, false);
    });
    window.matchMedia('(min-width: 601px)').addEventListener('change', function (event) {
      if (event.matches) setMenu(false, false);
    });
  }

  function revealTarget(hash, scroll) {
    if (!hash || hash === '#') return;
    var id;
    try { id = decodeURIComponent(hash.slice(1)); } catch (error) { return; }
    var target = document.getElementById(id);
    if (!target) return;
    var node = target;
    while (node) {
      if (node.tagName === 'DETAILS') node.open = true;
      node = node.parentElement;
    }
    if (scroll) requestAnimationFrame(function () { target.scrollIntoView({block: 'start'}); });
  }
  document.addEventListener('click', function (event) {
    var link = event.target.closest('a[href]');
    if (!link) return;
    var url = new URL(link.href, location.href);
    if (url.origin === location.origin && url.pathname === location.pathname && url.search === location.search && url.hash) revealTarget(url.hash, true);
  });
  window.addEventListener('hashchange', function () { revealTarget(location.hash, true); });
  revealTarget(location.hash, true);

  // Original ASCII figures stay available as selectable text.
  document.querySelectorAll('[data-original-content] pre').forEach(function (pre) {
    if (!/[┌└├│↓→]/.test(pre.textContent)) return;
    var container = pre.closest('.highlighter-rouge') || pre;
    var details = document.createElement('details');
    details.className = 'diagram-source';
    var summary = document.createElement('summary');
    summary.textContent = '원본 도식 · 텍스트로 펼쳐 읽기';
    container.parentNode.insertBefore(details, container);
    details.appendChild(summary);
    details.appendChild(container);
  });

  var headings = Array.from(document.querySelectorAll('.paper h2[id], .paper h3[id]'));
  var outline = document.querySelector('[data-outline]');
  var linksContainer = document.querySelector('[data-outline-links]');
  if (headings.length && outline && linksContainer) {
    var fragment = document.createDocumentFragment();
    var links = new Map();
    headings.forEach(function (heading) {
      var link = document.createElement('a');
      link.href = '#' + encodeURIComponent(heading.id);
      link.textContent = heading.textContent;
      if (heading.tagName === 'H3') link.className = 'is-subheading';
      fragment.appendChild(link);
      links.set(heading.id, link);
    });
    linksContainer.appendChild(fragment);
    outline.hidden = false;

    var mobileOutline = document.createElement('div');
    mobileOutline.className = 'mobile-outline';
    var label = document.createElement('label');
    label.htmlFor = 'section-jump'; label.textContent = '이 페이지 목차';
    var select = document.createElement('select');
    select.id = 'section-jump';
    var placeholder = document.createElement('option');
    placeholder.value = ''; placeholder.textContent = '읽을 절을 선택하세요';
    select.appendChild(placeholder);
    headings.forEach(function (heading) {
      var option = document.createElement('option');
      option.value = heading.id;
      option.textContent = (heading.tagName === 'H3' ? '　' : '') + heading.textContent;
      select.appendChild(option);
    });
    select.addEventListener('change', function () {
      if (select.value) {
        var hash = '#' + encodeURIComponent(select.value);
        revealTarget(hash, false);
        location.hash = hash;
        revealTarget(hash, true);
      }
    });
    mobileOutline.appendChild(label); mobileOutline.appendChild(select);
    document.querySelector('.paper-head').insertAdjacentElement('afterend', mobileOutline);

    if ('IntersectionObserver' in window) {
      var active;
      var observer = new IntersectionObserver(function (entries) {
        var visible = entries.filter(function (entry) { return entry.isIntersecting; });
        if (!visible.length) return;
        visible.sort(function (a, b) { return a.boundingClientRect.top - b.boundingClientRect.top; });
        if (active) active.removeAttribute('aria-current');
        active = links.get(visible[0].target.id);
        if (active) active.setAttribute('aria-current', 'location');
      }, {rootMargin: '-90px 0px -65% 0px', threshold: 0});
      headings.forEach(function (heading) { observer.observe(heading); });
    }
  }

  // Ensure native print dialogs include every original section and restore state.
  var beforePrintClosed = [];
  window.addEventListener('beforeprint', function () {
    beforePrintClosed = Array.from(document.querySelectorAll('details:not([open])'));
    beforePrintClosed.forEach(function (details) { details.open = true; });
  });
  window.addEventListener('afterprint', function () {
    beforePrintClosed.forEach(function (details) { details.open = false; });
    beforePrintClosed = [];
  });
})();
