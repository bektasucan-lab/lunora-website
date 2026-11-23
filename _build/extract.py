# -*- coding: utf-8 -*-
"""One-time: read the live (pre-v1) pages and save their content as JSON.
After the v1 redesign the JSON in _build/content is the source of truth;
do not re-run on generated pages."""
import re, json, html, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, '_build', 'content')

EMOJI = re.compile('[\U0001F000-\U0001FAFF☀-➿⬀-⯿️‍✨✅⌛⏳]+')
def clean(t): return re.sub(r'\s+', ' ', EMOJI.sub('', t)).strip()
def inner(s): return s.strip()
def text(s): return clean(html.unescape(re.sub(r'<[^>]+>', '', s)))
def one(p, s, flags=re.S):
    m = re.search(p, s, flags); return m.group(1) if m else None
def all_(p, s, flags=re.S): return re.findall(p, s, flags)

def head(s):
    h = s[:s.find('</head>')]
    meta = {
        'lang': one(r'<html lang="([^"]+)"', s),
        'title': html.unescape(one(r'<title>(.*?)</title>', h)),
        'tags': [t for t in all_(r'(<(?:meta|link)\b[^>]*>)', h)
                 if not re.search(r'charset|viewport|theme-color|fonts\.googleapis|rel="(?:icon|apple-touch-icon|shortcut icon)"', t)],
        'jsonld': all_(r'<script type="application/ld\+json">(.*?)</script>', h),
    }
    return meta

def section(s, sid):
    return one(r'<section[^>]*id="%s"[^>]*>(.*?)</section>' % sid, s)

def sec_head(sec):
    sh = one(r'<div class="section-head">(.*?)</div>', sec) or ''
    return {'badge': text(one(r'<span class="badge[^"]*">(.*?)</span>', sh) or ''),
            'h2': inner(one(r'<h2[^>]*>(.*?)</h2>', sh) or ''),
            'p': inner(one(r'<p>(.*?)</p>', sh) or '')}

def stores(s):
    return {'apple': all_(r'href="(https://apps\.apple\.com[^"]+)"', s),
            'play': all_(r'href="(https://play\.google\.com[^"]+)"', s),
            'small': [html.unescape(x) for x in all_(r'<small>(.*?)</small>', s)[:2]]}

def feature(path):
    s = open(path).read()
    d = {'path': os.path.relpath(path, ROOT), 'head': head(s)}
    hero = one(r'<header class="page-hero">(.*?)</header>', s)
    d['crumbs'] = [(text(t), h) for h, t in all_(r'<a href="([^"]+)">(.*?)</a>', one(r'<p class="crumbs">(.*?)</p>', hero))]
    d['crumb_last'] = text(re.split(r'</a>', one(r'<p class="crumbs">(.*?)</p>', hero))[-1].replace('›', ''))
    d['badge'] = text(one(r'<span class="hero-badge">(.*?)</span>', hero))
    d['h1'] = inner(one(r'<h1[^>]*>(.*?)</h1>', hero))
    d['summary'] = [inner(p) for p in all_(r'<p>(.*?)</p>', one(r'<div class="summary">(.*?)</div>', hero))]
    d['trust'] = [text(t) for t in all_(r'<span>(.*?)</span>', one(r'<div class="trust">(.*?)</div>', hero))]
    d['shot'] = {'src': one(r'<img class="shot[a-z-]*" src="([^"]+)"', hero), 'alt': html.unescape(one(r'<img class="shot[a-z-]*"[^>]*alt="([^"]*)"', hero) or '')}
    d['stores'] = stores(s)
    w = section(s, 'what'); d['what'] = sec_head(w)
    d['what']['cards'] = [{'icon': ic, 'h3': inner(h), 'p': inner(p)} for ic, h, p in
                          all_(r'<div class="fcard"><span class="icn">(.*?)</span><h3>(.*?)</h3><p>(.*?)</p></div>', w)]
    hw = section(s, 'how-it-works'); d['how'] = sec_head(hw)
    d['how']['steps'] = [{'h3': inner(h), 'p': inner(p)} for h, p in
                         all_(r'<li class="step"><span class="step-num">\d+</span><div><h3>(.*?)</h3><p>(.*?)</p></div></li>', hw)]
    dt = section(s, 'details'); d['details'] = sec_head(dt)
    d['details']['items'] = [{'h3': inner(one(r'<h3>(.*?)</h3>', x)), 'ps': [inner(p) for p in all_(r'<p>(.*?)</p>', x)]}
                             for x in all_(r'<div class="detail">(.*?)</div>', dt)]
    d['details']['note'] = inner(one(r'<p class="note">(.*?)</p>', dt) or '')
    fq = section(s, 'faq'); d['faq'] = sec_head(fq)
    d['faq']['items'] = [{'q': inner(q), 'a': inner(a)} for q, a in
                         all_(r'<button[^>]*class="faq-q"[^>]*>(.*?)</button>\s*<div class="faq-a">(.*?)</div>', fq)]
    mo = section(s, 'more'); d['more'] = sec_head(mo)
    d['more']['cards'] = [{'href': h, 'icon': ic, 'h3': inner(t), 'p': inner(p)} for h, ic, t, p in
                          all_(r'<a class="rcard" href="([^"]+)"><span class="icn">(.*?)</span><h3>(.*?)</h3><p>(.*?)</p></a>', mo)]
    rd = one(r'<div class="reading">(.*?)</div>', mo)
    d['more']['reading'] = {'h3': inner(one(r'<h3>(.*?)</h3>', rd)), 'links': [(h, inner(t)) for h, t in all_(r'<a href="([^"]+)">(.*?)</a>', rd)]}
    dl = section(s, 'download')
    d['download'] = {'badge': text(one(r'<span class="badge">(.*?)</span>', dl)), 'h2': inner(one(r'<h2[^>]*>(.*?)</h2>', dl)),
                     'p': inner(one(r'</h2>\s*<p>(.*?)</p>', dl)), 'greeting': text(one(r'<p class="greeting">(.*?)</p>', dl))}
    d['footer_about'] = inner(one(r'<div class="footer-brand">.*?<p>(.*?)</p>', s))
    d['langs'] = all_(r'<a href="([^"]+)"[^>]*hreflang="([a-z]+)">', one(r'<div class="lang-switch">(.*?)</div>', s))
    return d

def home(path):
    s = open(path).read()
    d = {'path': os.path.relpath(path, ROOT), 'head': head(s), 'stores': stores(s)}
    fq = one(r'<section class="faq" id="faq">(.*?)</section>', s)
    d['faq'] = sec_head(fq)
    d['faq']['items'] = [{'q': inner(q), 'a': inner(a)} for q, a in
                         all_(r'class="faq-q"[^>]*>(.*?)</(?:div|button)>\s*<div class="faq-a">(.*?)</div>', fq)]
    return d

def blog(path):
    s = open(path).read()
    d = {'path': os.path.relpath(path, ROOT), 'head': head(s), 'stores': stores(s)}
    hero = one(r'<section class="blog-hero">(.*?)</section>', s)
    d['h1'] = inner(one(r'<h1[^>]*>(.*?)</h1>', hero)); d['p'] = inner(one(r'<p>(.*?)</p>', hero))
    d['posts'] = [{'href': h, 'badge': text(b), 'h2': inner(t), 'p': inner(p), 'meta': [text(x) for x in all_(r'<span>(.*?)</span>', m)]}
                  for h, b, t, p, m in all_(r'<a href="([^"]+)" class="blog-card">\s*<div class="blog-card-badge"[^>]*>(.*?)</div>\s*<h2[^>]*>(.*?)</h2>\s*<p>(.*?)</p>\s*<div class="blog-card-meta">(.*?)</div>', s)]
    return d

def article(path):
    s = open(path).read()
    d = {'path': os.path.relpath(path, ROOT), 'head': head(s), 'stores': stores(s)}
    hero = one(r'<section class="article-hero">(.*?)</section>', s)
    d['crumbs_html'] = inner(one(r'<div class="breadcrumb">(.*?)</div>', hero))
    d['h1'] = inner(one(r'<h1[^>]*>(.*?)</h1>', hero))
    d['meta'] = inner(one(r'<p class="article-meta">(.*?)</p>', hero) or '')
    d['body'] = inner(one(r'<article class="article-content">(.*?)</article>', s))
    tail = s[s.find('</article>'):s.find('<footer')]
    d['related_h3'] = text(one(r'<h3[^>]*>(.*?)</h3>', tail) or '')
    d['related'] = [{'href': h, 'k': text(k), 't': inner(t), 'p': inner(p)} for h, k, t, p in
                    all_(r'<a href="([^"]+)"[^>]*>\s*<span[^>]*>(.*?)</span>\s*<h4[^>]*>(.*?)</h4>\s*<p[^>]*>(.*?)</p>\s*</a>', tail)]
    cta = one(r'<div class="article-cta-inner">(.*?)</div>', tail + '</div>') or ''
    d['cta'] = {'h2': inner(one(r'<h2[^>]*>(.*?)</h2>', cta) or ''), 'p': inner(one(r'<p>(.*?)</p>', cta) or '')}
    d['body_scripts'] = [x for x in all_(r'<script type="application/ld\+json">(.*?)</script>', s[s.find('<body'):])]
    return d

FEATURES = {
    'period': ['period-mode.html', 'tr/donem-modu.html', 'de/periodenmodus.html', 'fr/mode-regles.html'],
    'protect': ['protect-my-prayer.html', 'tr/namazimi-koru.html', 'de/mein-gebet-schuetzen.html', 'fr/proteger-ma-priere.html'],
    'quran': ['quran-reading-plan.html', 'tr/kuran-okuma-plani.html', 'de/koran-leseplan.html', 'fr/plan-lecture-coran.html'],
    'dhikr': ['dhikr-widget.html', 'tr/zikir-widget.html', 'de/dhikr-widget.html', 'fr/widget-dhikr.html'],
}
ARTICLES = ['can-muslim-women-pray-during-period.html', 'daily-duas-dhikr-muslim-women-guide.html',
            'muslim-women-marriage-spiritual-guide.html', 'muslim-women-mental-health-faith.html',
            'muslim-women-prayer-times-salah-guide.html', 'quran-reading-guide-muslim-women.html',
            'spiritual-self-care-muslim-women.html', 'what-to-do-during-period-in-islam.html']

if __name__ == '__main__':
    data = {'features': {k: {p.split('/')[0] if '/' in p else 'en': feature(os.path.join(ROOT, p)) for p in v} for k, v in FEATURES.items()},
            'home': {l: home(os.path.join(ROOT, p)) for l, p in [('en', 'index.html'), ('tr', 'tr/index.html'), ('de', 'de/index.html'), ('fr', 'fr/index.html')]},
            'blog': {'en': blog(os.path.join(ROOT, 'blog.html')), 'tr': blog(os.path.join(ROOT, 'tr/blog.html'))},
            'articles': {p[:-5]: article(os.path.join(ROOT, p)) for p in ARTICLES}}
    json.dump(data, open(os.path.join(OUT, 'live.json'), 'w'), ensure_ascii=False, indent=1)
    # sanity report
    for k, v in data['features'].items():
        for l, d in v.items():
            print(k, l, len(d['what']['cards']), len(d['how']['steps']), len(d['details']['items']), len(d['faq']['items']), len(d['more']['cards']), len(d['stores']['apple']), len(d['stores']['play']), d['shot']['src'])
    for l, d in data['home'].items(): print('home', l, len(d['faq']['items']), len(d['stores']['apple']), len(d['head']['jsonld']))
    for l, d in data['blog'].items(): print('blog', l, len(d['posts']))
    for k, d in data['articles'].items(): print('art', k, len(d['body']), len(d['related']), bool(d['cta']['h2']), len(d['stores']['apple']), len(d['head']['jsonld']), len(d['body_scripts']))

def simple(path):
    """support / privacy / terms: header + body html (run once, 23 Nov)."""
    s = open(path).read()
    d = {'path': os.path.relpath(path, ROOT), 'head': head(s)}
    ph = one(r'<div class="page-header">(.*?)</div>', s)
    d['badge'] = text(one(r'<span class="badge">(.*?)</span>', ph) or '')
    d['h1'] = inner(one(r'<h1[^>]*>(.*?)</h1>', ph)); d['sub'] = inner(one(r'<p class="subtitle">(.*?)</p>', ph) or '')
    body = s[s.find('</div>', s.find('<div class="page-header">')) + 6: s.find('<footer')]
    body = re.sub(r'<div class="(?:back-home|links)">.*?</div>', '', body, flags=re.S)
    body = re.sub(r'<script.*?</script>', '', body, flags=re.S)
    faqs = all_(r'<div class="faq-item">\s*<button class="faq-question">\s*<span>(.*?)</span>.*?<div class="faq-answer-inner">(.*?)</div>', body)
    d['faq'] = [{'q': inner(q), 'a': inner(a)} for q, a in faqs]
    if faqs:
        body = re.sub(r'<div class="faq-section">.*$', '', body, flags=re.S)
        d['faq_h2'] = text(one(r'<div class="faq-section">\s*<h2>(.*?)</h2>', s) or '')
    d['body'] = body.strip()
    return d
