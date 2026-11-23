# -*- coding: utf-8 -*-
"""Lunora web v1 page builder. Content: content/live.json (texts, FAQ, SEO tags
and store links of the pre-v1 pages) + home_text.py. Output: the site's HTML.
Run from anywhere:  python3 _build/build.py"""
import os, re, json, html as H
from home_text import T as HT, REVIEWS, FAQ as NEW_FAQ

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = os.path.join(ROOT, '_build')
LIVE = json.load(open(os.path.join(B, 'content', 'live.json')))
V = '4'  # css/js cache version
SITE = 'https://mylunora.app'
APPLE = 'https://apps.apple.com/app/apple-store/id6758765933?pt=128518745&amp;ct=%s&amp;mt=8'
PLAY = 'https://play.google.com/store/apps/details?id=com.studiolunora.lunora&amp;referrer=utm_source%%3Dmylunora.app%%26utm_medium%%3Dweb%%26utm_campaign%%3D%s'

LANGS = ['en', 'tr', 'ar', 'de', 'fr', 'id']
LNAME = {'en': 'English', 'tr': 'Türkçe', 'ar': 'العربية', 'de': 'Deutsch', 'fr': 'Français', 'id': 'Bahasa Indonesia'}
HOME = {l: '/' if l == 'en' else '/%s/' % l for l in LANGS}
OGLOC = {'en': 'en_US', 'tr': 'tr_TR', 'ar': 'ar_AR', 'de': 'de_DE', 'fr': 'fr_FR', 'id': 'id_ID'}
FEAT_PATHS = {
    'period': {'en': '/period-mode.html', 'tr': '/tr/donem-modu.html', 'de': '/de/periodenmodus.html', 'fr': '/fr/mode-regles.html'},
    'protect': {'en': '/protect-my-prayer.html', 'tr': '/tr/namazimi-koru.html', 'de': '/de/mein-gebet-schuetzen.html', 'fr': '/fr/proteger-ma-priere.html'},
    'quran': {'en': '/quran-reading-plan.html', 'tr': '/tr/kuran-okuma-plani.html', 'de': '/de/koran-leseplan.html', 'fr': '/fr/plan-lecture-coran.html'},
    'dhikr': {'en': '/dhikr-widget.html', 'tr': '/tr/zikir-widget.html', 'de': '/de/dhikr-widget.html', 'fr': '/fr/widget-dhikr.html'},
}
BLOG_PATHS = {'en': '/blog.html', 'tr': '/tr/blog.html'}

UI = {
 'en': dict(nav=['Features', 'Period Mode', 'Protect My Prayer', 'Blog', 'Support'], menu='Menu', language='Language', skip='Skip to content',
            dl1='Download on the', dl2='Get it on', iphone='iPhone & Android', noads='No ads', langs='9 languages', home='Home',
            about='A spiritual companion designed for Muslim women, with care and understanding at its heart.', app='App', help='Help', priv='Privacy Policy', terms='Terms of Service', follow='Follow',
            quran='Quran reading plan', dhikr='Dhikr widget', minread='min read', all='All', reltitle='Related reading', blogLead='Blog'),
 'tr': dict(nav=['Özellikler', 'Dönem Modu', 'Namazımı Koru', 'Blog', 'Destek'], menu='Menü', language='Dil', skip='İçeriğe geç',
            dl1='App Store’dan', dl2='Google Play’den', iphone='iPhone ve Android', noads='Reklam yok', langs='9 dil', home='Ana sayfa',
            about='Müslüman kadınlar için, özenle ve anlayışla tasarlanmış manevi bir yol arkadaşı.', app='Uygulama', help='Yardım', priv='Gizlilik Politikası', terms='Kullanım Koşulları', follow='Takip edin',
            quran='Kur’an okuma planı', dhikr='Zikir widget’ı', minread='dk okuma', all='Tümü', reltitle='İlgili yazılar', blogLead='Blog'),
 'de': dict(nav=['Funktionen', 'Periodenmodus', 'Mein Gebet schützen', 'Blog', 'Support'], menu='Menü', language='Sprache', skip='Zum Inhalt',
            dl1='Laden im', dl2='Jetzt bei', iphone='iPhone & Android', noads='Keine Werbung', langs='9 Sprachen', home='Startseite',
            about='Eine spirituelle Begleiterin für muslimische Frauen, mit Sorgfalt und Verständnis gestaltet.', app='App', help='Hilfe', priv='Datenschutz', terms='Nutzungsbedingungen', follow='Folgen',
            quran='Koran-Leseplan', dhikr='Dhikr-Widget', minread='Min. Lesezeit', all='Alle', reltitle='Weiterlesen', blogLead='Blog'),
 'fr': dict(nav=['Fonctionnalités', 'Mode règles', 'Protéger ma prière', 'Blog', 'Aide'], menu='Menu', language='Langue', skip='Aller au contenu',
            dl1='Télécharger dans l’', dl2='Disponible sur', iphone='iPhone et Android', noads='Sans publicité', langs='9 langues', home='Accueil',
            about='Une compagne spirituelle conçue pour les femmes musulmanes, avec soin et bienveillance.', app='Appli', help='Aide', priv='Confidentialité', terms='Conditions d’utilisation', follow='Suivre',
            quran='Plan de lecture du Coran', dhikr='Widget dhikr', minread='min de lecture', all='Tout', reltitle='À lire aussi', blogLead='Blog'),
 'ar': dict(nav=['المزايا', 'وضع الدورة', 'احمي صلاتي', 'المدوّنة', 'الدعم'], menu='القائمة', language='اللغة', skip='انتقلي إلى المحتوى',
            dl1='حمّليه من', dl2='احصلي عليه من', iphone='iPhone وAndroid', noads='بلا إعلانات', langs='٩ لغات', home='الرئيسية',
            about='رفيقة روحية صُممت للمرأة المسلمة، بعناية وتفهّم.', app='التطبيق', help='المساعدة', priv='سياسة الخصوصية', terms='شروط الاستخدام', follow='تابعينا',
            quran='خطة قراءة القرآن', dhikr='أداة الذكر', minread='دقائق قراءة', all='الكل', reltitle='اقرئي أيضًا', blogLead='المدوّنة'),
 'id': dict(nav=['Fitur', 'Mode Haid', 'Jaga Salatku', 'Blog', 'Bantuan'], menu='Menu', language='Bahasa', skip='Langsung ke konten',
            dl1='Unduh di', dl2='Dapatkan di', iphone='iPhone & Android', noads='Tanpa iklan', langs='9 bahasa', home='Beranda',
            about='Teman spiritual yang dirancang untuk muslimah, dengan perhatian dan pengertian.', app='Aplikasi', help='Bantuan', priv='Kebijakan Privasi', terms='Ketentuan Layanan', follow='Ikuti',
            quran='Rencana baca Al-Qur’an', dhikr='Widget zikir', minread='menit baca', all='Semua', reltitle='Bacaan terkait', blogLead='Blog'),
}

# ---------------------------------------------------------------- helpers
_ICONS = {}
def ic(name, cls=''):
    if name not in _ICONS:
        s = open(os.path.join(B, 'icons', name + '.svg')).read()
        s = re.sub(r'<svg[^>]*viewBox="([^"]+)"[^>]*>', r'<svg viewBox="\1" class="ic%s" aria-hidden="true" focusable="false">', s, count=1)
        _ICONS[name] = s.replace('\n', '')
    return _ICONS[name].replace('class="ic%s"', 'class="ic%s"' % ((' ' + cls) if cls else ''))

def esc(s): return H.escape(s, quote=True)
def att(s): return H.escape(H.unescape(s), quote=True)
def img(name): return '/img/v1/%s.webp' % name

def shot(lang, key):
    p = os.path.join(ROOT, 'img/v1/app/%s-%s.webp' % (lang, key))
    return '/img/v1/app/%s-%s.webp' % (lang if os.path.exists(p) else 'en', key)

def store_btns(l, apple, play, light=False):
    u = UI[l]; c = ' light' if light else ''
    return ('<div class="stores">'
            '<a class="store%s" href="%s">%s<span><small>%s</small><b>App Store</b></span></a>'
            '<a class="store%s" href="%s">%s<span><small>%s</small><b>Google Play</b></span></a></div>') % (
        c, apple, ic('apple-logo-fill'), esc(u['dl1']), c, play, ic('google-play-logo-fill'), esc(u['dl2']))

def fonts(l, amiri=False):
    fam = ['Playfair+Display:ital,wght@0,500;0,600;1,500', 'Nunito:wght@400;600;700;800']
    if l == 'ar': fam += ['Amiri:wght@400;700', 'Cairo:wght@400;600;700;800']
    elif amiri: fam += ['Amiri:wght@700']
    return ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
            '<link href="https://fonts.googleapis.com/css2?%s&amp;display=swap" rel="stylesheet">' % '&amp;'.join('family=' + f for f in fam))

def fix_tag(t):
    # relative og:image -> absolute; leave everything else as it was
    t = re.sub(r'(property="og:image" content=")(?!https?:)/?([^"]+)"', lambda m: '%s%s/%s"' % (m.group(1), SITE, m.group(2)), t)
    return t

def head(l, title, tags, jsonld=(), amiri=False, preload=None):
    out = ['<!DOCTYPE html>', '<html lang="%s"%s>' % (l, ' dir="rtl"' if l == 'ar' else ''), '<head>',
           '<meta charset="UTF-8">', '<meta name="viewport" content="width=device-width, initial-scale=1">',
           '<title>%s</title>' % esc(H.unescape(title)),
           '<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">', '<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">',
           '<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">', '<link rel="shortcut icon" href="/favicon.ico">',
           '<meta name="theme-color" content="#3F6B55">']
    out += [fix_tag(t) for t in tags]
    out.append(fonts(l, amiri))
    if preload: out.append('<link rel="preload" as="image" href="%s">' % preload)
    out.append('<link rel="stylesheet" href="/css/v1.css?v=%s">' % V)
    out.append('<script src="/js/v1.js?v=%s" defer></script>' % V)
    for j in jsonld: out.append('<script type="application/ld+json">%s</script>' % j.strip())
    out.append('</head>')
    return '\n'.join(out)

def nav(l, active, alternates):
    """alternates: {lang: path} for the language list (only languages that have this page)."""
    u = UI[l]
    feat = FEAT_PATHS
    links = [(u['nav'][0], HOME[l] + '#features', 'features'),
             (u['nav'][1], feat['period'].get(l, feat['period']['en']), 'period'),
             (u['nav'][2], feat['protect'].get(l, feat['protect']['en']), 'protect'),
             (u['nav'][3], BLOG_PATHS.get(l, '/blog.html'), 'blog'),
             (u['nav'][4], '/support.html', 'support')]
    def la(k): return ' aria-current="page"' if k == active else ''
    items = ''.join('<a href="%s"%s>%s</a>' % (h, la(k), esc(t)) for t, h, k in links)
    langs = ''.join('<li><a href="%s" hreflang="%s" lang="%s"%s>%s<small>%s</small></a></li>' % (
        alternates[x], x, x, ' aria-current="true"' if x == l else '', esc(LNAME[x]), x.upper()) for x in LANGS if x in alternates)
    lang_box = ('<details class="lang"><summary aria-label="%s">%s%s</summary><ul>%s</ul></details>' % (esc(u['language']), l.upper(), ic('caret-down'), langs)) if len(alternates) > 1 else ''
    panel_langs = ''.join('<a href="%s" hreflang="%s" lang="%s"%s>%s</a>' % (alternates[x], x, x, ' aria-current="page"' if x == l else '', esc(LNAME[x])) for x in LANGS if x in alternates and x != l)
    return ('<a class="skip" href="#main">%s</a>'
            '<header class="nav"><div class="wrap nav-in">'
            '<a class="brand" href="%s"><img src="/img/v1/app-icon.webp" alt="" width="36" height="36"><span>Lunora</span></a>'
            '<nav class="nav-links" aria-label="%s">%s</nav>'
            '<div class="nav-end">%s<button class="burger" type="button" aria-expanded="false" aria-controls="panel" aria-label="%s">%s%s</button></div>'
            '</div><div class="panel" id="panel">%s<div class="panel-langs">%s</div></div></header>') % (
        esc(u['skip']), HOME[l], esc(u['menu']), items, lang_box, esc(u['menu']), ic('list', 'ic-list'), ic('x', 'ic-x'), items, panel_langs)

def footer(l):
    u = UI[l]; f = FEAT_PATHS
    g = lambda k: f[k].get(l, f[k]['en'])
    return ('<footer class="foot"><div class="wrap foot-grid">'
            '<div class="foot-about"><a class="brand" href="%s"><img src="/img/v1/app-icon.webp" alt="" width="32" height="32"><span>Lunora</span></a><p>%s</p></div>'
            '<div><h4>%s</h4><a href="%s#features">%s</a><a href="%s">%s</a><a href="%s">%s</a><a href="%s">%s</a><a href="%s">%s</a><a href="%s">%s</a></div>'
            '<div><h4>%s</h4><a href="/support.html">%s</a><a href="/privacy.html">%s</a><a href="/terms.html">%s</a></div>'
            '<div><h4>%s</h4><a class="ig" href="https://instagram.com/mylunora.app" rel="noopener">%s@mylunora.app</a><span class="copy">© 2026 Studio Lunora</span></div>'
            '</div></footer>') % (
        HOME[l], esc(u['about']),
        esc(u['app']), HOME[l], esc(u['nav'][0]), g('period'), esc(u['nav'][1]), g('protect'), esc(u['nav'][2]), g('quran'), esc(u['quran']), g('dhikr'), esc(u['dhikr']), BLOG_PATHS.get(l, '/blog.html'), esc(u['nav'][3]),
        esc(u['help']), esc(u['nav'][4]), esc(u['priv']), esc(u['terms']), esc(u['follow']), ic('instagram-logo'))

def page(l, headhtml, body, active, alternates):
    return '%s\n<body>\n%s\n<main id="main">\n%s\n</main>\n%s\n</body>\n</html>\n' % (headhtml, nav(l, active, alternates), body, footer(l))

# Store rating and review count (Beck, 23 Nov): Google Play 629 reviews,
# 4.7 (US listing); App Store 40 ratings, 4.7. Together: 650+, 4.7. Written by
# hand; update when the count passes 700 or the rating moves.
RATING = {
    'en': '4.7 · 650+ reviews on the App Store and Google Play',
    'tr': "4,7 · App Store ve Google Play'de 650+ yorum",
    'de': '4,7 · 650+ Bewertungen im App Store und bei Google Play',
    'fr': "4,7 · plus de 650 avis sur l'App Store et Google Play",
    'ar': '٤٫٧ · أكثر من ٦٥٠ مراجعة على App Store وGoogle Play',
    'id': '4,7 · 650+ ulasan di App Store dan Google Play',
}
# The hero line sits under the two store buttons, so it names no store.
RATING_SHORT = {'en': '4.7 · 650+ reviews', 'tr': '4,7 · 650+ yorum', 'de': '4,7 · 650+ Bewertungen',
                'fr': '4,7 · plus de 650 avis', 'ar': '٤٫٧ · أكثر من ٦٥٠ مراجعة', 'id': '4,7 · 650+ ulasan'}


def trust(items):
    return '<div class="trust">%s</div>' % ''.join('<span>%s%s</span>' % (ic(i), esc(t)) for i, t in items)

def faq_block(items, first_open=True):
    out = []
    for i, it in enumerate(items):
        a = it['a'] if it['a'].lstrip().startswith('<') else '<p>%s</p>' % it['a']
        out.append('<details%s><summary>%s%s%s</summary><div class="a">%s</div></details>' % (
            ' open' if (i == 0 and first_open) else '', it['q'], ic('plus', 'pl'), ic('minus', 'mi'), a))
    return '<div class="faq">%s</div>' % ''.join(out)

def faq_jsonld(items):
    return json.dumps({'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
        {'@type': 'Question', 'name': H.unescape(re.sub('<[^>]+>', '', i['q'])), 'acceptedAnswer': {'@type': 'Answer', 'text': H.unescape(re.sub('<[^>]+>', '', i['a'])).strip()}} for i in items]},
        ensure_ascii=False, indent=1)

def write(path, s):
    # Turkish uppercase turns "iPhone" into "İPHONE" in the caps labels; mark the brand as English there.
    if path.startswith('/tr/'):
        s = re.sub(r'(<span class="(?:pill|kicker)[^"]*"[^>]*>[^<]*?)iPhone', r'\1<span lang="en">iPhone</span>', s)
    full = os.path.join(ROOT, path.lstrip('/'))
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, 'w').write(s)
    return path

def split_h1(h):
    m = re.match(r'^(.*?\S)(\s?:)\s+(.+)$', h)
    return ('%s%s <em>%s</em>' % (m.group(1), m.group(2), m.group(3))) if m else h

# ---------------------------------------------------------------- home
AR_DIGITS = '٠١٢٣٤٥٦٧٨٩'
FAQ_H2 = {'en': 'Frequently asked questions', 'tr': 'Sık sorulan sorular', 'de': 'Häufige Fragen', 'fr': 'Questions fréquentes'}
def home_page(l):
    t = HT[l]; u = UI[l]; live = LIVE['home'].get(l)
    if live:
        a, p = live['stores']['apple'], live['stores']['play']
        faq_items = live['faq']['items']; faq_h2 = FAQ_H2[l]
    else:
        a = [APPLE % ('web-home-%s-1' % l), APPLE % ('web-home-%s-2' % l)]
        p = [PLAY % ('home_hero_%s' % l), PLAY % ('home_download_%s' % l)]
        faq_h2, raw = NEW_FAQ[l]; faq_items = [{'q': esc(q), 'a': esc(x)} for q, x in raw]
    canon = SITE + HOME[l]
    tags = ['<meta name="description" content="%s">' % esc(t['desc']), '<link rel="canonical" href="%s">' % canon]
    tags += ['<link rel="alternate" hreflang="%s" href="%s%s">' % (x, SITE, HOME[x]) for x in LANGS] + ['<link rel="alternate" hreflang="x-default" href="%s/">' % SITE]
    tags += ['<meta property="og:title" content="%s">' % esc(t['og']), '<meta property="og:description" content="%s">' % esc(t['desc']),
             '<meta property="og:url" content="%s">' % canon, '<meta property="og:image" content="%s/icon-192.png">' % SITE,
             '<meta property="og:type" content="website">', '<meta property="og:site_name" content="Lunora">', '<meta property="og:locale" content="%s">' % OGLOC[l],
             '<meta name="twitter:card" content="summary">']
    graph = [j for j in LIVE['home']['en']['head']['jsonld'] if '"@graph"' in j][0]
    jsonld = [faq_jsonld(faq_items), graph]
    keys = ['F', 'B5', 'D', 'C', 'A2']   # index order of t['day'] / t['shot_alt']
    num = AR_DIGITS if l == 'ar' else '0123456789'
    # Hero flow follows the captured screens' own times (emulator, 23 Nov):
    # Fajr verse, Dhuhr Pray Together ("now Dhuhr"), Asr Quran lesson,
    # Maghrib Protect My Prayer (shield shows Maghrib), night Period Mode.
    TIMES = ['06:24', '12:56', '15:26', '17:47', None]
    order = [0, 2, 3, 1, 4]
    names = [x[0].split(' · ')[0] for x in t['day']]
    day = [(names[i] + (' · ' + ''.join(num[int(c)] if c.isdigit() else c for c in TIMES[i]) if TIMES[i] else ''), t['day'][j][1]) for i, j in enumerate(order)]
    alts = [t['shot_alt'][j] for j in order]
    hero_shots = [shot(l, keys[j]) for j in order]

    slides = ''.join('<img src="%s" alt="%s" width="390" height="800"%s%s>' % (
        s, esc(alts[i]), ' class="on"' if i == 0 else '', '' if i == 0 else ' loading="lazy"') for i, s in enumerate(hero_shots))
    rail = ''.join('<li><button type="button" class="%s" aria-pressed="%s" data-t="%s" data-l="%s"><span class="dot"></span><span class="lbl"><span class="t">%s</span><span class="l">%s</span></span></button></li>' % (
        'on' if i == 0 else '', 'true' if i == 0 else 'false', esc(tm), esc(lb), esc(tm), esc(lb)) for i, (tm, lb) in enumerate(day))
    hero = ('<section class="hero"><img class="bg" src="%s" alt="" fetchpriority="high"><div class="hero-wash"></div>'
            '<div class="wrap hero-grid"><div class="hero-txt">'
            '<div class="pill-row"><span class="pill">%s</span></div>'
            '<h1>%s <em>%s</em></h1><p class="lead">%s</p>%s%s</div>'
            '<div class="day" role="group" aria-label="%s"><div class="phone"><div class="scr slides">%s</div></div>'
            '<ul class="rail">%s</ul><div class="cur" aria-hidden="true"><span class="t">%s</span><span class="l">%s</span></div></div>'
            '</div></section>') % (
        img('bg-b-45'), esc(t['tag']), esc(t['h1a']), esc(t['h1b']), esc(t['lead']), store_btns(l, a[0], p[0]),
        trust([('star-fill', RATING_SHORT[l]), ('gift', t['trial']), ('prohibit', t['noads'])]),
        esc(t['rail_label']), slides, rail, esc(day[0][0]), esc(day[0][1]))

    pil_meta = [('bg-c-45', '50% 30%', 'C', '#86692A', FEAT_PATHS['quran']), ('bg-a-45', '50% 40%', 'A2', '#9A5A62', FEAT_PATHS['period']), ('bg-b-45', '50% 40%', 'B5', '#3F6B55', FEAT_PATHS['protect'])]
    pillars = ''.join(
        ('<article class="pillar"><div class="pillar-img"><img class="bg" src="%s" alt="" loading="lazy" style="object-position:%s">'
         '<div class="phone sm"><div class="scr"><img src="%s" alt="%s" loading="lazy" width="390" height="800"></div></div></div>'
         '<div class="pillar-txt"><span class="kicker" style="color:%s">%s</span><h3>%s</h3><p>%s</p><a class="more" href="%s">%s %s</a></div></article>') % (
            img(bg), pos, shot(l, k), esc(t['shot_alt'][keys.index(k)]), col, esc(pt[0]), esc(pt[1]), esc(pt[2]), paths.get(l, paths['en']), esc(t['more']), ic('arrow-right-bold'))
        for (bg, pos, k, col, paths), pt in zip(pil_meta, t['pil']))
    covers = ''.join('<div class="cover"><img src="%s" alt="" loading="lazy"><span><small>%s</small><b>%s</b></span></div>' % (img(n), esc(c[0]), esc(c[1]))
                     for n, c in zip(['hacer', 'hatice', 'rahman'], t['covers']))
    sec1 = ('<section class="sec" id="features"><div class="wrap">'
            '<div class="head"><span class="kicker">%s</span><h2>%s</h2></div><div class="pillars">%s</div>'
            '<p class="and">%s</p>'
            '<div class="band lib"><img class="bg" src="%s" alt="" loading="lazy"><div class="lib-wash"></div><div class="band-in">'
            '<div class="band-txt"><span class="pill dark">%s</span><h2>%s <em>%s</em></h2><p>%s</p><div class="chips">%s</div></div>'
            '<div class="covers">%s</div></div></div></div></section>') % (
        esc(t['k1']), esc(t['h2a']), pillars, esc(t['and1']), img('kehf'), esc(t['libK']), esc(t['libA']), esc(t['libB']), esc(t['libP']),
        ''.join('<span>%s</span>' % esc(s) for s in t['shelves']), covers)
    per_icons = ['flower-fill', 'book-open-text-fill', 'moon-stars-fill']
    sec2 = ('<section id="period-mode"><div class="wrap"><p class="and" style="margin-top:0">%s</p>'
            '<div class="band per"><img class="bg" src="%s" alt="" loading="lazy"><div class="per-wash"></div><div class="band-in">'
            '<div class="band-txt"><span class="pill rose">%s</span><h2>%s <em>%s</em></h2><p>%s</p><ul>%s</ul><a class="link-more" href="%s">%s %s</a></div>'
            '<div class="ring"><img src="%s" alt="%s" loading="lazy" width="400" height="400"><img class="sak" src="%s" alt="" loading="lazy"></div>'
            '</div></div></div></section>') % (
        esc(t['and2']), img('bg-a-wide'), esc(t['perK']), esc(t['perA']), esc(t['perB']), esc(t['perP']),
        ''.join('<li>%s%s</li>' % (ic(i), esc(x)) for i, x in zip(per_icons, t['per'])),
        FEAT_PATHS['period'].get(l, FEAT_PATHS['period']['en']), esc(t['perMore']), ic('arrow-right-bold'), img('ring-a'), esc(t['ring_alt']), img('sakura'))
    feat_imgs = ['ic-tasbih', 'ic-rug', 'ic-lantern', 'ic-books', 'ic-rahle', 'ic-rug', 'ic-pen', 'ic-tree']
    feat_links = [FEAT_PATHS['dhikr'], None, None, None, None, None, None, None]
    feats = ''
    for (ti, de), im, lk in zip(t['feats'], feat_imgs, feat_links):
        inner = '<span class="disk"><img src="%s" alt="" loading="lazy" width="56" height="56"></span><b>%s</b><span>%s</span>' % (img(im), esc(ti), esc(de))
        feats += ('<a class="feat" href="%s">%s</a>' % (lk.get(l, lk['en']), inner)) if lk else '<div class="feat">%s</div>' % inner
    sec3 = '<section class="sec"><div class="wrap"><div class="head"><span class="kicker">%s</span><h2>%s</h2></div><div class="feats">%s</div></div></section>' % (esc(t['k2']), esc(t['h2b']), feats)
    stars = ic('star-fill') * 5
    revs = ''.join('<figure class="rev"><div class="stars" role="img" aria-label="5/5">%s</div><blockquote lang="%s"%s>“%s”</blockquote>%s</figure>' % (
        stars, r['lang'], ' dir="rtl"' if r['lang'] == 'ar' else '', esc(r['q']), ('<figcaption><span>— %s</span></figcaption>' % esc(r['name'])) if r.get('name') else '') for r in REVIEWS[l])
    sec4 = ('<section class="sec revs"><img class="bg" src="%s" alt="" loading="lazy"><div class="revs-wash"></div><div class="wrap">'
            '<div class="head"><span class="kicker">%s</span><p class="rev-score"><span class="stars" aria-hidden="true">%s</span>%s</p></div><div class="rev-grid">%s</div><p class="rev-note">%s</p></div></section>') % (
        img('guven-bg'), esc(t['revK']), stars, esc(RATING[l]), revs, esc(t['revNote']))
    # widgets
    n0 = 12; fmt = lambda x: ''.join(num[int(c)] for c in str(x))
    ar_name = 'Subhanallah' if l != 'tr' else 'Sübhânallah'
    widgets = ('<div class="wstack" data-tasbih="%d" data-num="%s">'
               '<div class="w-med"><img class="bg" src="%s" alt="" loading="lazy">'
               '<button class="beads" type="button" data-add aria-label="%s"><span class="n"><b data-count>%s</b><small>/ %s</small></span></button>'
               '<span class="w-sep"></span><div class="w-txt"><span class="eb">%s</span><span class="ar" lang="ar" dir="rtl">سُبْحَانَ اللّٰه</span>%s'
               '<div class="w-btns"><button class="say" type="button" data-add>%s%s</button><button class="reset" type="button" data-reset aria-label="%s">%s</button></div></div></div>'
               '<div class="w-lock"><img class="bg" src="%s" alt="" loading="lazy">'
               '<div class="w-rect"><small>SUBHANALLAH</small><b><span data-count>%s</span> <small>/ %s</small></b><span class="bar"><i data-bar></i></span></div>'
               '<div class="w-circ"><svg width="72" height="72" viewBox="0 0 72 72" aria-hidden="true"><circle cx="36" cy="36" r="29" fill="none" stroke="rgba(255,255,255,.3)" stroke-width="5" stroke-linecap="round" stroke-dasharray="136.7 182.2"/><circle data-gauge cx="36" cy="36" r="29" fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round" stroke-dasharray="49.7 182.2"/></svg><span data-count>%s</span></div>'
               '</div></div>') % (
        n0, num, img('tesbih-bg-wide'), esc(t['wSay']), fmt(n0), fmt(33), esc(t['wEye']),
        '' if l == 'ar' else '<span class="nm">%s</span>' % ar_name, ic('plus'), esc(t['wSay']), esc(t['wReset']), ic('x') if False else _reset_icon(),
        img('tesbih-bg'), fmt(n0), fmt(33), fmt(n0))
    sec5 = ('<section class="sec"><div class="wrap wgrid"><div class="wtxt"><span class="kicker">%s</span><h2>%s</h2><p>%s</p>'
            '<a class="link-more" style="color:var(--green);border-color:var(--green)" href="%s">%s %s</a></div>%s</div></section>') % (
        esc(t['wK']), esc(t['wH']), esc(t['wP']), FEAT_PATHS['dhikr'].get(l, FEAT_PATHS['dhikr']['en']), esc(UI[l]['dhikr']), ic('arrow-right-bold'), widgets)
    sec6 = ('<section class="sec" id="faq" style="padding-top:0"><div class="wrap"><div class="head"><h2>%s</h2></div>%s</div></section>') % (
        esc(faq_h2), faq_block(faq_items))
    sec7 = ('<section class="sec" id="download" style="padding-top:0"><div class="wrap"><div class="cta">'
            '<img class="heart" src="%s" alt="" width="88" height="88" loading="lazy"><h2>%s</h2><p>%s</p>%s<span class="salam">%s</span></div></div></section>') % (
        img('heart'), esc(t['ctaH']), esc(t['ctaP']), store_btns(l, a[1], p[1], light=True), esc(t['salam']))
    body = hero + sec1 + sec2 + sec3 + sec4 + sec5 + sec6 + sec7
    hh = head(l, t['title'], tags, jsonld, amiri=True, preload=img('bg-b-45'))
    return write(HOME[l] + 'index.html', page(l, hh, body, 'home', HOME))

def _reset_icon():
    # Phosphor arrow-counter-clockwise (regular), inline
    return '<svg viewBox="0 0 256 256" class="ic" aria-hidden="true" focusable="false"><path d="M224,128a96,96,0,0,1-94.71,96H128A95.38,95.38,0,0,1,62.1,197.8a8,8,0,0,1,11-11.63A80,80,0,1,0,71.43,71.39a3.07,3.07,0,0,1-.26.25L44.59,96H72a8,8,0,0,1,0,16H24a8,8,0,0,1-8-8V56a8,8,0,0,1,16,0V85.8L60.25,60A96,96,0,0,1,224,128Z"/></svg>'

# ---------------------------------------------------------------- feature pages
THEMES = {
 'period': dict(pill='rose', acc='#9A5A62', line='#D4A5A5', bg='bg-a-wide', pos='50% 40%', vis='phone', key='A2', cta='rose', band='', cards='t-rose',
                icons=['sakura', 'ic-books', 'ic-dates', 'ic-tasbih', 'ic-lotus', 'ic-pillow', 'ic-tree', 'ic-pen', 'ic-lock'],
                dicons=['book-open-text', 'user-circle', 'timer', 'moon-stars-fill']),
 'protect': dict(pill='green', acc='#3F6B55', line='#8FB09E', bg='bg-b-wide', pos='60% 40%', vis='phone', key='B5', cta='', band='gold', cards='',
                 icons=['ic-lantern', 'ic-rug', 'ic-lock', 'ic-mosque', 'sakura', 'ic-tree'], dicons=['apple-logo-fill', 'android-logo']),
 'quran': dict(pill='', acc='#86692A', line='#C4A35A', bg='bg-c-wide', pos='40% 50%', vis='plans', key=None, cta='', band='gold', cards='',
               icons=['ic-lantern', 'ic-rahle', 'ic-quran-stand', 'ic-book-pink', 'ic-pen', 'sakura'], dicons=['book-open-text-fill', 'device-mobile']),
 'dhikr': dict(pill='green', acc='#3F6B55', line='#8FB09E', bg='tesbih-bg-wide', pos='20% 50%', vis='widget', key=None, cta='', band='dark', cards='',
               icons=['ic-tasbih', 'ic-lotus', 'kapak-tesbih', 'ic-books', 'ic-pen', 'ic-lantern'], dicons=['apple-logo-fill', 'android-logo']),
}
VIS_ALT = {'A2': 4, 'B5': 1}

def feature_page(key, l):
    d = LIVE['features'][key][l]; th = THEMES[key]; u = UI[l]
    alts = FEAT_PATHS[key]
    st = d['stores']
    crumbs = ''.join('<li><a href="%s">%s</a></li>' % (h, esc(t)) for t, h in d['crumbs']) + '<li aria-current="page">%s</li>' % esc(d['crumb_last'])
    if th['vis'] == 'phone':
        alt = d['shot']['alt'] or HT[l]['shot_alt'][VIS_ALT[th['key']]]
        vis = '<div class="phone"><div class="scr"><img src="%s" alt="%s" width="390" height="800" fetchpriority="high"></div></div>' % (shot(l, th['key']), att(alt))
        if key == 'period': vis += '<img class="sak a" src="%s" alt=""><img class="sak b" src="%s" alt="">' % (img('sakura'), img('sakura'))
    elif th['vis'] == 'plans':
        vis = '<div class="plans">%s</div>' % ''.join('<div class="plan"><img src="%s" alt="" width="110" height="110"><b>%s</b></div>' % (img(im), c['h3'])
                                                    for c, im in zip(d['what']['cards'][:4], th['icons'][:4]))
    else:
        num = '0123456789'
        vis = ('<div class="wscene"><img class="bg" src="%s" alt="">'
               '<div class="wstack" data-tasbih="12" data-num="%s" style="position:relative">'
               '<div class="w-med"><img class="bg" src="%s" alt="">'
               '<button class="beads" type="button" data-add aria-label="+1"><span class="n"><b data-count>12</b><small>/ 33</small></span></button>'
               '<span class="w-sep"></span><div class="w-txt"><span class="eb">%s</span><span class="ar" lang="ar" dir="rtl">سُبْحَانَ اللّٰه</span><span class="nm">%s</span>'
               '<div class="w-btns"><button class="say" type="button" data-add>%s%s</button><button class="reset" type="button" data-reset aria-label="%s">%s</button></div></div></div>'
               '<div class="w-lock" style="background:rgba(31,42,36,.25)"><div class="w-rect"><small>SUBHANALLAH</small><b><span data-count>12</span> <small>/ 33</small></b><span class="bar"><i data-bar></i></span></div>'
               '<div class="w-circ"><svg width="72" height="72" viewBox="0 0 72 72" aria-hidden="true"><circle cx="36" cy="36" r="29" fill="none" stroke="rgba(255,255,255,.3)" stroke-width="5" stroke-linecap="round" stroke-dasharray="136.7 182.2"/><circle data-gauge cx="36" cy="36" r="29" fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round" stroke-dasharray="49.7 182.2"/></svg><span data-count>12</span></div></div>'
               '</div></div>') % (img('tesbih-bg'), num, img('tesbih-bg-wide'), esc(HT[l]['wEye']), 'Sübhânallah' if l == 'tr' else 'Subhanallah',
                                  ic('plus'), esc(HT[l]['wSay']), esc(HT[l]['wReset']), _reset_icon())
    pill_cls = ('pill ' + th['pill']).strip()
    hero = ('<section class="phero"><img class="bg" src="%s" alt="" style="--pos:%s"><div class="phero-wash"></div>'
            '<div class="wrap phero-grid"><div class="phero-txt"><ol class="crumbs">%s</ol><span class="%s">%s</span><h1>%s</h1>%s%s%s</div>'
            '<div class="phero-vis">%s</div></div></section>') % (
        img(th['bg']), th['pos'], crumbs, pill_cls, esc(d['badge']), split_h1(d['h1']),
        ''.join('<p class="lead">%s</p>' % p for p in d['summary']), store_btns(l, st['apple'][0], st['play'][0]),
        trust([('device-mobile', d['trust'][0]), ('prohibit', d['trust'][1]), ('globe-hemisphere-west', d['trust'][2])]), vis)
    style = '--acc:%s;--line:%s' % (th['acc'], th['line'])
    w = d['what']
    cards = ''.join('<article class="card"><div class="card-img"><img src="%s" alt="" loading="lazy" width="130" height="130"></div><div class="card-txt"><h3>%s</h3><p>%s</p></div></article>' % (
        img(im), c['h3'], c['p']) for c, im in zip(w['cards'], th['icons']))
    s_what = ('<section class="sec %s" id="what"><div class="wrap"><div class="head"><span class="kicker" style="color:%s">%s</span><h2>%s</h2>%s</div><div class="cards">%s</div></div></section>') % (
        th['cards'], th['acc'], esc(w['badge']), w['h2'], ('<p>%s</p>' % w['p']) if w['p'] else '', cards)
    hw = d['how']
    steps = ''.join('<li class="step"><span class="num">%d</span><h3>%s</h3><p>%s</p></li>' % (i + 1, s['h3'], s['p']) for i, s in enumerate(hw['steps']))
    s_how = ('<section class="sec" id="how-it-works" style="padding-top:0;%s"><div class="wrap"><div class="head"><span class="kicker" style="color:%s">%s</span><h2>%s</h2></div>'
             '<ol class="steps" style="--n:%d">%s</ol></div></section>') % (style, th['acc'], esc(hw['badge']), hw['h2'], len(hw['steps']), steps)
    dt = d['details']
    facts = ''.join('<div class="fact">%s<h3>%s</h3>%s</div>' % (ic(i), it['h3'], ''.join('<p>%s</p>' % p for p in it['ps'])) for it, i in zip(dt['items'], th['dicons']))
    note = ''
    if dt['note']: note = '<p class="note">%s</p>' % dt['note']
    if key == 'period':
        note += '<div class="disclaim">%s<span>%s</span></div>' % (ic('info'), esc(DISCLAIM[l]))
    band_bg = {'': ('bg-a-wide', 'rose'), 'gold': ('bg-c-wide', 'gold'), 'dark': ('guven-bg', 'dark')}[th['band']]
    pill_b = {'': 'pill rose', 'gold': 'pill', 'dark': 'pill dark'}[th['band']]
    s_det = ('<section id="details"><div class="wrap"><div class="dband %s"><img class="bg" src="%s" alt="" loading="lazy"><div class="band-in">'
             '<div class="band-txt"><span class="%s">%s</span><h2>%s</h2>%s</div><div class="facts">%s</div></div></div></div></section>') % (
        band_bg[1], img(band_bg[0]), pill_b, esc(dt['badge']), dt['h2'], note, facts)
    fq = d['faq']
    s_faq = '<section class="sec" id="faq"><div class="wrap"><div class="head"><span class="kicker">%s</span><h2>%s</h2></div>%s</div></section>' % (esc(fq['badge']), fq['h2'], faq_block(fq['items']))
    mo = d['more']
    icon_for = {'/dhikr-widget.html': 'ic-tasbih', '/quran-reading-plan.html': 'ic-rahle', '/protect-my-prayer.html': 'ic-lock', '/period-mode.html': 'sakura'}
    def icon_of(href):
        for k2, paths in FEAT_PATHS.items():
            if href in paths.values(): return icon_for[paths['en']]
        return 'ic-books'
    rel = ''.join('<a class="feat" href="%s"><span class="disk"><img src="%s" alt="" loading="lazy" width="56" height="56"></span><div><b>%s</b><span>%s</span></div></a>' % (
        c['href'], img(icon_of(c['href'])), c['h3'], c['p']) for c in mo['cards'])
    reading = '<div class="read"><h3>%s</h3><ul>%s</ul></div>' % (mo['reading']['h3'], ''.join('<li><a href="%s">%s %s</a></li>' % (h, ic('arrow-right-bold'), t) for h, t in mo['reading']['links']))
    s_more = '<section class="sec" id="more" style="padding-top:0"><div class="wrap"><div class="head"><span class="kicker">%s</span><h2>%s</h2></div><div class="rel">%s</div>%s</div></section>' % (
        esc(mo['badge']), mo['h2'], rel, reading)
    dl = d['download']
    s_dl = ('<section class="sec" id="download" style="padding-top:0"><div class="wrap"><div class="cta %s"><span class="kicker" style="color:rgba(255,255,255,.8)">%s</span><h2>%s</h2><p>%s</p>%s<span class="salam">%s</span></div></div></section>') % (
        th['cta'], esc(dl['badge']), dl['h2'], dl['p'], store_btns(l, st['apple'][1], st['play'][1], light=True), esc(dl['greeting']))
    body = hero + s_what + s_how + s_det + s_faq + s_more + s_dl
    hh = head(l, d['head']['title'], d['head']['tags'], d['head']['jsonld'], amiri=(key == 'dhikr'))
    active = {'period': 'period', 'protect': 'protect'}.get(key, 'features')
    return write(alts[l], page(l, hh, body, active, alts))

DISCLAIM = {
    'en': 'Predictions help you plan. They are never a ruling; when in doubt, ask a scholar you trust.',
    'tr': 'Tahminler plan yapmanıza yardım eder, hüküm değildir; şüphede kaldığınızda güvendiğiniz bir âlime danışın.',
    'de': 'Vorhersagen helfen dir beim Planen. Sie sind nie ein Urteil; frag im Zweifel eine Gelehrte oder einen Gelehrten deines Vertrauens.',
    'fr': 'Les prévisions t’aident à t’organiser. Ce ne sont jamais des avis juridiques ; en cas de doute, demande à une personne savante de confiance.',
}

# ---------------------------------------------------------------- blog
POST_META = {
    'muslim-women-marriage-spiritual-guide': ('life', 'hatice'),
    'muslim-women-mental-health-faith': ('life', 'guven-bg'),
    'daily-duas-dhikr-muslim-women-guide': ('dhikr', 'tesbih-bg'),
    'muslim-women-prayer-times-salah-guide': ('prayer', 'namaz-bg'),
    'quran-reading-guide-muslim-women': ('quran', 'kurs-bg'),
    'can-muslim-women-pray-during-period': ('period', 'empty-invite'),
    'spiritual-self-care-muslim-women': ('life', 'bg-a-wide'),
    'what-to-do-during-period-in-islam': ('period', 'empty-waiting'),
}
CAT_COL = {'period': '#9A5A62', 'prayer': '#3F6B55', 'quran': '#86692A', 'dhikr': '#3F6B55', 'life': '#86692A'}
CATS = {'en': [('all', 'All'), ('period', 'Period'), ('prayer', 'Prayer'), ('quran', 'Quran'), ('dhikr', 'Duas & dhikr'), ('life', 'Life & faith')],
        'tr': [('all', 'Tümü'), ('period', 'Dönem'), ('prayer', 'Namaz'), ('quran', 'Kur’an'), ('dhikr', 'Dua ve zikir'), ('life', 'Hayat ve iman')]}
BLOG_TXT = {'en': dict(tag='The Lunora journal', h1a='Notes for', h1b='your quiet moments.', cta=('Read it', 'in the app, too'), ctaP='Duas, dhikr, the Quran and Period Mode, together in Lunora. No ads, in 9 languages.'),
            'tr': dict(tag='Lunora yazıları', h1a='Sakin anlarınız', h1b='için notlar.', cta=('Uygulamada', 'da okuyun'), ctaP='Dualar, zikirler, Kur’an ve Dönem Modu, Lunora’da bir arada. Reklamsız, 9 dilde.')}

def slug_of(href): return href.split('/')[-1].replace('.html', '')

def blog_page(l):
    d = LIVE['blog'][l]; bt = BLOG_TXT[l]; u = UI[l]
    posts = ''
    for p in d['posts']:
        s = slug_of(p['href']); cat, im = POST_META[s]
        href = '/' + s + '.html'
        date = p['meta'][0] if p['meta'] else ''
        mins = p['meta'][1] if len(p['meta']) > 1 else ''
        posts += ('<a class="post" href="%s" data-cat="%s"><div class="post-img"><img src="%s" alt="" loading="lazy"></div><div class="post-txt">'
                  '<span class="kicker" style="color:%s">%s</span><h2>%s</h2><p>%s</p><span class="meta"><time>%s</time> · %s %s</span></div></a>') % (
            href, cat, img(im), CAT_COL[cat], esc(p['badge']), p['h2'], p['p'], esc(date), esc(mins), ic('arrow-right-bold'))
    chips = ''.join('<button type="button" data-cat="%s" aria-pressed="%s">%s</button>' % (c, 'true' if c == 'all' else 'false', esc(n)) for c, n in CATS[l])
    hero = ('<section class="bhero"><img class="bg" src="%s" alt=""><div class="bhero-wash"></div><div class="wrap"><span class="pill">%s</span>'
            '<h1>%s <em>%s</em></h1><p class="lead">%s</p></div></section>') % (img('guven-bg'), esc(bt['tag']), esc(bt['h1a']), esc(bt['h1b']), d['p'])
    lst = '<section class="sec"><div class="wrap"><h2 class="sr">%s</h2><div class="filters" role="group">%s</div><div class="posts">%s</div></div></section>' % (esc(H.unescape(re.sub('<[^>]+>', '', d['h1']))), chips, posts)
    a, p = d['stores']['apple'], d['stores']['play']
    apple = a[-1] if a else APPLE % ('web-blog-%s-2' % l)
    play = p[-1] if p else PLAY % ('blog_%s' % l)
    cta = '<section class="sec" id="download" style="padding-top:0"><div class="wrap"><div class="cta"><h2>%s <em>%s</em></h2><p>%s</p>%s</div></div></section>' % (
        esc(bt['cta'][0]), esc(bt['cta'][1]), esc(bt['ctaP']), store_btns(l, apple, play, light=True))
    hh = head(l, d['head']['title'], d['head']['tags'], d['head']['jsonld'])
    return write(BLOG_PATHS[l], page(l, hh, hero + lst + cta, 'blog', BLOG_PATHS))

ART_CTA_P = 'No ads, in 9 languages.'
def article_page(slug):
    d = LIVE['articles'][slug]; l = 'en'; cat, im = POST_META[slug]
    crumbs = re.split(r'\s*&rarr;\s*|\s*→\s*', d['crumbs_html'])
    cl = ''
    for c in crumbs:
        m = re.match(r'<a href="([^"]+)">(.*?)</a>', c.strip())
        if m:
            h = m.group(1); h = h if h.startswith('/') or h.startswith('http') else '/' + h
            cl += '<li><a href="%s">%s</a></li>' % (h, m.group(2))
        elif c.strip(): cl += '<li aria-current="page">%s</li>' % c.strip()
    hero = ('<section class="ahero"><img class="bg" src="%s" alt=""><div class="ahero-wash"></div><div class="wrap"><ol class="crumbs" style="justify-content:center">%s</ol>'
            '<span class="kicker" style="color:%s">%s</span><h1>%s</h1><p class="meta">%s</p></div></section>') % (
        img(im), cl, CAT_COL[cat], esc(dict(CATS['en'])[cat]), d['h1'], d['meta'])
    body = '<article class="prose">%s</article>' % d['body']
    rel = ''
    if d['related']:
        rel = '<section class="arel"><h2>%s</h2><div class="posts">%s</div></section>' % (esc(d['related_h3'] or UI['en']['reltitle']), ''.join(
            '<a class="post" href="/%s"><div class="post-txt"><span class="kicker" style="color:%s">%s</span><h2>%s</h2><p>%s</p></div></a>' % (
                r['href'].lstrip('/'), CAT_COL[POST_META.get(slug_of(r['href']), ('life', ''))[0]], esc(r['k']), r['t'], r['p']) for r in d['related']))
    apple = d['stores']['apple'][-1] if d['stores']['apple'] else APPLE % ('web-%s-en' % slug[:16])
    play = d['stores']['play'][-1] if d['stores']['play'] else PLAY % ('article_%s' % slug.replace('-', '_')[:40])
    cta = '<section class="acta" id="download"><div class="cta"><h2>%s</h2><p>%s</p>%s</div></section>' % (
        d['cta']['h2'] or 'Download Lunora', d['cta']['p'] or ART_CTA_P, store_btns(l, apple, play, light=True))
    jsonld = d['head']['jsonld'] + d['body_scripts']
    hh = head(l, d['head']['title'], d['head']['tags'], jsonld)
    return write('/%s.html' % slug, page(l, hh, hero + body + rel + cta, 'blog', {'en': '/%s.html' % slug}))

# ---------------------------------------------------------------- support / privacy / terms
def simple_page(k):
    d = LIVE['simple'][k]; l = 'en'
    hero = ('<section class="ahero"><img class="bg" src="%s" alt=""><div class="ahero-wash"></div><div class="wrap">'
            '<span class="pill">%s</span><h1>%s</h1>%s</div></section>') % (img('guven-bg'), esc(d['badge']), d['h1'], ('<p class="meta">%s</p>' % d['sub']) if d['sub'] else '')
    body = '<div class="prose">%s</div>' % d['body']
    if d['faq']:
        body += '<section class="sec" style="padding-top:8px"><div class="wrap"><div class="head"><h2>%s</h2></div>%s</div></section>' % (esc(d.get('faq_h2') or 'Frequently asked questions'), faq_block(d['faq'], first_open=False))
    hh = head(l, d['head']['title'], d['head']['tags'], d['head']['jsonld'])
    return write('/%s.html' % k, page(l, hh, hero + body, 'support' if k == 'support' else '', {'en': '/%s.html' % k}))

# ---------------------------------------------------------------- sitemap
def sitemap(today):
    urls = []
    def add(loc, alts):
        x = '  <url>\n    <loc>%s%s</loc>\n    <lastmod>%s</lastmod>\n' % (SITE, loc, today)
        if len(alts) > 1:
            for k in LANGS:
                if k in alts: x += '    <xhtml:link rel="alternate" hreflang="%s" href="%s%s"/>\n' % (k, SITE, alts[k])
            x += '    <xhtml:link rel="alternate" hreflang="x-default" href="%s%s"/>\n' % (SITE, alts['en'])
        urls.append(x + '  </url>\n')
    for l in LANGS: add(HOME[l], HOME)
    for k, alts in FEAT_PATHS.items():
        for l in alts: add(alts[l], alts)
    for l in BLOG_PATHS: add(BLOG_PATHS[l], BLOG_PATHS)
    for s in POST_META: add('/%s.html' % s, {'en': '/%s.html' % s})
    for extra in ['/support.html', '/privacy.html', '/terms.html']: add(extra, {'en': extra})
    s = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n%s</urlset>\n' % ''.join(urls)
    return write('/sitemap.xml', s)

if __name__ == '__main__':
    import datetime
    out = [home_page(l) for l in LANGS]
    out += [feature_page(k, l) for k in FEAT_PATHS for l in FEAT_PATHS[k]]
    out += [blog_page(l) for l in BLOG_PATHS]
    out += [article_page(s) for s in POST_META]
    out += [simple_page(k) for k in ['support', 'privacy', 'terms']]
    out.append(sitemap(datetime.date.today().isoformat()))
    print(len(out), 'files'); print('\n'.join(out))
