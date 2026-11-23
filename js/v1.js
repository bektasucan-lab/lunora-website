/* Lunora web v1 — menu, language list, hero day flow, tasbih widget, blog filter. */
(function () {
  var d = document;
  // mobile menu
  var nav = d.querySelector('.nav'), burger = d.querySelector('.burger');
  if (nav && burger) burger.addEventListener('click', function () {
    var open = nav.classList.toggle('open');
    burger.setAttribute('aria-expanded', open ? 'true' : 'false');
  });
  // close language list on outside click / Escape
  d.addEventListener('click', function (e) {
    d.querySelectorAll('details.lang[open]').forEach(function (x) { if (!x.contains(e.target)) x.removeAttribute('open'); });
  });
  d.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    d.querySelectorAll('details.lang[open]').forEach(function (x) { x.removeAttribute('open'); });
    if (nav && nav.classList.contains('open')) { nav.classList.remove('open'); burger.setAttribute('aria-expanded', 'false'); }
  });
  // hero: the screen changes with the time of day
  var day = d.querySelector('.day');
  if (day) {
    var imgs = day.querySelectorAll('.slides img'), btns = day.querySelectorAll('.rail button'),
        cur = day.querySelector('.cur'), i = 0, tm = null;
    var show = function (n) {
      i = n;
      imgs.forEach(function (im, k) { im.classList.toggle('on', k === n); if (k === n && im.loading === 'lazy') im.loading = 'eager'; });
      btns.forEach(function (b, k) { b.classList.toggle('on', k === n); b.setAttribute('aria-pressed', k === n ? 'true' : 'false'); });
      if (cur) { cur.querySelector('.t').textContent = btns[n].dataset.t; cur.querySelector('.l').textContent = btns[n].dataset.l; }
    };
    btns.forEach(function (b, k) { b.addEventListener('click', function () { clearInterval(tm); tm = null; show(k); }); });
    var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (!reduce) tm = setInterval(function () { show((i + 1) % imgs.length); }, 3200);
  }
  // tasbih widgets: tap to count, 33 beads
  d.querySelectorAll('[data-tasbih]').forEach(function (root) {
    var n = parseInt(root.dataset.tasbih, 10) || 0, T = 33, num = root.dataset.num || '0123456789';
    var fmt = function (x) { return String(x).replace(/\d/g, function (c) { return num[+c]; }); };
    var ring = root.querySelector('.beads');
    if (ring && !ring.querySelector('i')) {
      for (var k = 0; k < T; k++) {
        var a = (k / T) * 2 * Math.PI - Math.PI / 2, b = d.createElement('i');
        b.style.left = (50 + 44 * Math.cos(a)) + '%'; b.style.top = (50 + 44 * Math.sin(a)) + '%';
        ring.insertBefore(b, ring.firstChild);
      }
    }
    var paint = function () {
      var beads = ring ? ring.querySelectorAll('i') : [];
      for (var k = 0; k < beads.length; k++) beads[beads.length - 1 - k].classList.toggle('f', k < n);
      root.querySelectorAll('[data-count]').forEach(function (e) { e.textContent = fmt(n); });
      root.querySelectorAll('[data-bar]').forEach(function (e) { e.style.width = (n / T * 100) + '%'; });
      root.querySelectorAll('[data-gauge]').forEach(function (e) {
        var C = 2 * Math.PI * 29, arc = C * .75; e.setAttribute('stroke-dasharray', Math.max(.01, arc * n / T).toFixed(1) + ' ' + C.toFixed(1));
      });
    };
    root.querySelectorAll('[data-add]').forEach(function (e) { e.addEventListener('click', function () { n = n >= T ? 1 : n + 1; paint(); }); });
    root.querySelectorAll('[data-reset]').forEach(function (e) { e.addEventListener('click', function () { n = 0; paint(); }); });
    paint();
  });
  // blog filter
  var fl = d.querySelector('.filters');
  if (fl) fl.addEventListener('click', function (e) {
    var b = e.target.closest('button'); if (!b) return;
    fl.querySelectorAll('button').forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
    var c = b.dataset.cat;
    d.querySelectorAll('.post[data-cat]').forEach(function (p) { p.hidden = c !== 'all' && p.dataset.cat.split(' ').indexOf(c) < 0; });
  });
})();
