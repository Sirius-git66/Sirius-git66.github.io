/* THE ARC · AI Investment ROI — motion layer
   reveals · count-ups · discount-chain waterfall · reverse break-even demo */
(function () {
  'use strict';
  /* ?qa=1 → still-frame mode for screenshots: everything at final state */
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches ||
                new URLSearchParams(location.search).has('qa');
  if (reduced) {
    var s = document.createElement('style');
    s.textContent = '*{transition:none!important;animation:none!important}' +
      'html{scroll-behavior:auto!important}' +
      '.rv{opacity:1!important;transform:none!important}' +
      '.hero h1 .w>span{transform:none!important}' +
      'h2.mk .h2-in{transform:none!important}' +
      '#qadump{position:fixed;top:0;left:0;right:0;z-index:99;background:#401418;color:#ffd7d7;padding:6px 10px;font:11px/1.4 monospace}';
    document.head.appendChild(s);
    if (location.hash) {
      var t = document.querySelector(location.hash);
      if (t) window.scrollTo(0, t.offsetTop);
    }
    var sec = new URLSearchParams(location.search).get('s');
    if (sec) {
      var el = document.getElementById(sec);
      if (el) window.scrollTo(0, el.offsetTop);
    }
    var only = new URLSearchParams(location.search).get('only');
    if (only) {
      document.querySelectorAll('header.hero, section, footer, nav#mast').forEach(function (el) {
        if (el.id !== only) el.style.display = 'none';
      });
      window.scrollTo(0, 0);
    }
    if (new URLSearchParams(location.search).has('dump')) {
      setTimeout(function () {
        var bad = [];
        document.querySelectorAll('*').forEach(function (el) {
          var r = el.getBoundingClientRect();
          if (r.right > window.innerWidth + 1 || r.left < -1) {
            bad.push(el.tagName + '.' + (el.className.baseVal !== undefined ? '' : String(el.className).split(' ')[0]) + ' r=' + Math.round(r.right) + ' l=' + Math.round(r.left));
          }
        });
        var d = document.createElement('div');
        d.id = 'qadump';
        d.textContent = 'SW=' + document.documentElement.scrollWidth + ' IW=' + window.innerWidth + ' | ' + bad.slice(0, 12).join(' ; ');
        document.body.appendChild(d);
      }, 300);
    }
  }

  /* ---------- masthead + threshold ruler · one rAF-throttled scroll handler ---------- */
  var mast = document.getElementById('mast');
  var rcur = document.getElementById('rulerCursor');
  var ticking = false;
  function onScroll() {
    ticking = false;
    if (mast) mast.classList.toggle('scrolled', window.scrollY > 12);
    if (rcur) {
      var max = document.documentElement.scrollHeight - window.innerHeight;
      var p = max > 0 ? Math.min(window.scrollY / max, 1) : 0;
      rcur.style.left = (p * 100).toFixed(2) + '%';
      rcur.classList.toggle('past', p * 100 >= 55.3);
    }
  }
  window.addEventListener('scroll', function () {
    if (!ticking) { ticking = true; requestAnimationFrame(onScroll); }
  }, { passive: true });
  onScroll();

  /* ---------- hero word stagger · words read from the DOM, not restated ---------- */
  var h1 = document.getElementById('heroH1');
  if (h1) {
    var toks = [];
    (function walk(n) {
      n.childNodes.forEach(function (c) {
        if (c.nodeType === 3) {
          c.textContent.split(/\s+/).forEach(function (w) {
            if (w) toks.push(w.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'));
          });
        } else if (c.nodeType === 1) {
          if (c.querySelector('*')) walk(c); else toks.push(c.outerHTML);
        }
      });
    })(h1);
    if (toks.length > 1) toks[toks.length - 2] += '\u00A0' + toks.pop(); /* last pair unbreakable */
    h1.innerHTML = toks.map(function (w, i) {
      return '<span class="w"><span style="transition-delay:' + (120 + i * 90) + 'ms">' + w + '</span></span>';
    }).join(' ');
    requestAnimationFrame(function () {
      requestAnimationFrame(function () { h1.classList.add('in'); });
    });
  }

  /* ---------- heading mask reveal + widow rescue ---------- */
  function bindWidow(el) {
    var node = el;
    while (node.lastElementChild) node = node.lastElementChild;
    var tn = node.lastChild;
    while (tn && tn.nodeType !== 3) tn = tn.previousSibling;
    if (tn) tn.textContent = tn.textContent.replace(/\s+(\S+)\s+(\S+)$/, '\u00A0$1\u00A0$2');
  }
  document.querySelectorAll('h2').forEach(function (h) {
    h.classList.remove('rv');
    h.classList.add('mk');
    h.innerHTML = '<span class="h2-in">' + h.innerHTML + '</span>';
    bindWidow(h);
  });
  document.querySelectorAll('h3, p, li').forEach(bindWidow);

  /* ---------- kicker decode ---------- */
  if (!reduced) {
    var CH = '—·/\\_<>#0123456789';
    document.querySelectorAll('.kicker').forEach(function (k) {
      var txt = k.textContent;
      k.setAttribute('aria-label', txt);          /* screen readers get the true string… */
      var inner = document.createElement('span'); /* …the visible copy scrambles */
      inner.setAttribute('aria-hidden', 'true');
      inner.textContent = txt;
      k.textContent = '';
      k.appendChild(inner);
      var kio = new IntersectionObserver(function (es) {
        es.forEach(function (en) {
          if (!en.isIntersecting) return;
          kio.unobserve(k);
          var t0 = null, dur = 650, n = txt.length;
          function tick(t) {
            if (!t0) t0 = t;
            var p = Math.min((t - t0) / dur, 1);
            var lock = Math.floor(p * n);
            var out = '';
            for (var i = 0; i < n; i++) {
              var c = txt.charAt(i);
              out += (i < lock || c === ' ' || c === '·') ? c : CH.charAt((Math.random() * CH.length) | 0);
            }
            inner.textContent = p === 1 ? txt : out;
            if (p < 1) requestAnimationFrame(tick);
          }
          requestAnimationFrame(tick);
        });
      }, { threshold: 0.6 });
      kio.observe(k);
    });
  }

  /* ---------- number formatting ---------- */
  function fmt(v, kind) {
    if (kind === 'usd') return '$' + Math.round(v).toLocaleString('en-US');
    if (kind === 'pct1') return v.toFixed(1) + '%';
    return Math.round(v).toLocaleString('en-US');
  }

  /* ---------- count-up ---------- */
  function countUp(el) {
    var target = parseFloat(el.getAttribute('data-count'));
    var kind = el.getAttribute('data-fmt') || 'int';
    if (reduced) { el.textContent = fmt(target, kind); return; }
    var t0 = null, dur = 1400;
    function tick(t) {
      if (!t0) t0 = t;
      var p = Math.min((t - t0) / dur, 1);
      var e = 1 - Math.pow(2, -10 * p);           /* expo.out */
      el.textContent = fmt(target * (p === 1 ? 1 : e), kind);
      if (p < 1) requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
  }

  /* ---------- reveal observer ---------- */
  var rv = document.querySelectorAll('.rv, h2.mk');
  var counted = new WeakSet();
  function activate(el) {
    el.classList.add('in');
    el.querySelectorAll('[data-count]').forEach(function (c) {
      if (!counted.has(c)) { counted.add(c); countUp(c); }
    });
    if (el.hasAttribute('data-count') && !counted.has(el)) { counted.add(el); countUp(el); }
  }
  if (reduced || !('IntersectionObserver' in window)) {
    rv.forEach(activate);
    var chainNow = document.getElementById('chain');
    if (chainNow) chainNow.classList.add('go');
  } else {
    var io = new IntersectionObserver(function (entries) {
      var batch = 0;
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        var el = en.target;
        el.style.transitionDelay = (Math.min(batch, 4) * 70) + 'ms';
        batch++;
        activate(el);
        io.unobserve(el);
      });
    }, { threshold: 0.15, rootMargin: '0px 0px -48px 0px' });
    rv.forEach(function (el) { io.observe(el); });

    /* chain bars fire when the chain enters view */
    var chain = document.getElementById('chain');
    if (chain) {
      var cio = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) {
          if (en.isIntersecting) { chain.classList.add('go'); cio.disconnect(); }
        });
      }, { threshold: 0.25 });
      cio.observe(chain);
    }
  }

  /* chain bar widths */
  document.querySelectorAll('.bar i').forEach(function (b) {
    b.style.setProperty('--w', b.getAttribute('data-w'));
  });

  /* ---------- perimeter probe ---------- */
  var stage = document.getElementById('perimStage');
  var probe = document.getElementById('perimProbe');
  var pread = document.getElementById('perimRead');
  if (stage && probe && pread && !reduced) {
    stage.addEventListener('mousemove', function (e) {
      var r = stage.getBoundingClientRect();
      var cx = r.width / 2, cy = r.height / 2;
      var ang = Math.atan2(e.clientY - r.top - cy, e.clientX - r.left - cx);
      var R = Math.min(cx, cy) * 0.86;
      probe.style.transform = 'translate(' + (Math.cos(ang) * R).toFixed(1) + 'px,' + (Math.sin(ang) * R).toFixed(1) + 'px)';
      stage.classList.add('live');
      pread.textContent = 'egress probe · blocked at perimeter · 0 bytes out';
    });
    stage.addEventListener('mouseleave', function () {
      stage.classList.remove('live');
      pread.textContent = 'perimeter sealed · 0 bytes out';
    });
  }

  /* ---------- door spotlight ---------- */
  document.querySelectorAll('.door').forEach(function (d) {
    d.addEventListener('mousemove', function (e) {
      var r = d.getBoundingClientRect();
      d.style.setProperty('--mx', (e.clientX - r.left).toFixed(0) + 'px');
      d.style.setProperty('--my', (e.clientY - r.top).toFixed(0) + 'px');
    });
  });

  /* ---------- reverse break-even demo ----------
     Worked example: adoption threshold 55.3228%, forecast 62%,
     NPV(62%) = $276,189. NPV is affine in adoption: NPV(x) = a·(x − T). */
  var T = 55.3227660215367;
  var F0 = 62;
  var NPV0 = 276188.716678167;
  var slope = NPV0 / (F0 - T);                 /* $ per percentage point */
  var LO = 35, HI = 85;

  var slider = document.getElementById('demoSlider');
  var fill = document.getElementById('demoFill');
  var cursor = document.getElementById('demoCursor');
  var thresh = document.getElementById('demoThresh');
  var live = document.getElementById('demoLive');
  var forecastEl = document.getElementById('demoForecast');
  var npvEl = document.getElementById('demoNpv');
  var noteEl = document.getElementById('demoNote');

  if (slider && fill && cursor && thresh && live && forecastEl && npvEl && noteEl) {
    function pos(x) { return ((x - LO) / (HI - LO)) * 100; }
    thresh.style.left = pos(T) + '%';

    function demoUpdate() {
      var x = parseFloat(slider.value);
      var npv = slope * (x - T);
      var head = x - T;
      fill.style.width = pos(x) + '%';
      cursor.style.left = pos(x) + '%';
      forecastEl.textContent = x.toFixed(1) + '%';
      npvEl.textContent = (npv < 0 ? '−$' : '$') + Math.abs(Math.round(npv)).toLocaleString('en-US');
      npvEl.classList.toggle('neg', npv < 0);
      live.classList.toggle('neg', head < 0);
      live.textContent = head >= 0
        ? 'headroom +' + head.toFixed(1) + ' pts'
        : 'case breaks · ' + head.toFixed(1) + ' pts';
      noteEl.textContent = head >= 0
        ? 'You forecast ' + x.toFixed(1) + '%. The case breaks below ' + T.toFixed(1) +
          '% — headroom of ' + head.toFixed(1) +
          ' percentage points on a driver the committee can watch every month.'
        : 'At ' + x.toFixed(1) + '% the case is below its break-even threshold of ' + T.toFixed(1) +
          '%. NPV turns negative — which is precisely the statement the instrument puts on record before the money moves.';
    }
    slider.addEventListener('input', demoUpdate);
    demoUpdate();
  }
})();
