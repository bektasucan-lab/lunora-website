# -*- coding: utf-8 -*-
"""Lunora web v1 page builder. Content: content/live.json (texts, FAQ, SEO tags
and store links of the pre-v1 pages) + home_text.py. Output: the site's HTML.
Run from anywhere:  python3 _build/build.py"""
import os, re, json, html as H
from home_text import T as HT, REVIEWS, FAQ as NEW_FAQ

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = os.path.join(ROOT, '_build')
LIVE = json.load(open(os.path.join(B, 'content', 'live.json')))
V = '6'  # css/js cache version
SITE = 'https://mylunora.app'
APPLE = 'https://apps.apple.com/app/apple-store/id6758765933?pt=128518745&amp;ct=%s&amp;mt=8'
PLAY = 'https://play.google.com/store/apps/details?id=com.studiolunora.lunora&amp;referrer=utm_source%%3Dmylunora.app%%26utm_medium%%3Dweb%%26utm_campaign%%3D%s'

LANGS = ['en', 'tr', 'ar', 'de', 'fr', 'id']
LNAME = {'en': 'English', 'tr': 'Türkçe', 'ar': 'العربية', 'de': 'Deutsch', 'fr': 'Français', 'id': 'Bahasa Indonesia'}
HOME = {l: '/' if l == 'en' else '/%s/' % l for l in LANGS}
OGLOC = {'en': 'en_US', 'tr': 'tr_TR', 'ar': 'ar_AR', 'de': 'de_DE', 'fr': 'fr_FR', 'id': 'id_ID'}
RTL = {'ar', 'ur'}
FEAT_PATHS = {
    'period': {'en': '/period-mode.html', 'tr': '/tr/donem-modu.html', 'de': '/de/periodenmodus.html', 'fr': '/fr/mode-regles.html'},
    'protect': {'en': '/protect-my-prayer.html', 'tr': '/tr/namazimi-koru.html', 'de': '/de/mein-gebet-schuetzen.html', 'fr': '/fr/proteger-ma-priere.html'},
    'quran': {'en': '/quran-reading-plan.html', 'tr': '/tr/kuran-okuma-plani.html', 'de': '/de/koran-leseplan.html', 'fr': '/fr/plan-lecture-coran.html'},
    'dhikr': {'en': '/dhikr-widget.html', 'tr': '/tr/zikir-widget.html', 'de': '/de/dhikr-widget.html', 'fr': '/fr/widget-dhikr.html'},
}
BLOG_PATHS = {'en': '/blog.html', 'tr': '/tr/blog.html'}
# Free online tasbih counter (28 Nov): "dhikr counter" ~1,000 US searches a month, KD 3.
TASBIH = {'en': '/tasbih-counter.html', 'tr': '/tr/zikirmatik.html', 'de': '/de/tasbih-zaehler.html',
          'fr': '/fr/compteur-tasbih.html', 'id': '/id/tasbih-digital.html'}

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
    elif l == 'ur': fam += ['Amiri:wght@400;700', 'Noto+Nastaliq+Urdu:wght@400;600;700']
    elif l == 'bn': fam += ['Amiri:wght@700', 'Hind+Siliguri:wght@400;500;600;700']
    elif amiri: fam += ['Amiri:wght@700']
    return ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
            '<link href="https://fonts.googleapis.com/css2?%s&amp;display=swap" rel="stylesheet">' % '&amp;'.join('family=' + f for f in fam))

def fix_tag(t):
    # relative og:image -> absolute; leave everything else as it was
    t = re.sub(r'(property="og:image" content=")(?!https?:)/?([^"]+)"', lambda m: '%s%s/%s"' % (m.group(1), SITE, m.group(2)), t)
    return t

def head(l, title, tags, jsonld=(), amiri=False, preload=None):
    out = ['<!DOCTYPE html>', '<html lang="%s"%s>' % (l, ' dir="rtl"' if l in RTL else ''), '<head>',
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
    tc_link = ('<a href="%s">%s</a>' % (TASBIH[l], esc(TC[l]['crumb']))) if l in TASBIH else ''
    return ('<footer class="foot"><div class="wrap foot-grid">'
            '<div class="foot-about"><a class="brand" href="%s"><img src="/img/v1/app-icon.webp" alt="" width="32" height="32"><span>Lunora</span></a><p>%s</p></div>'
            '<div><h4>%s</h4><a href="%s#features">%s</a><a href="%s">%s</a><a href="%s">%s</a><a href="%s">%s</a><a href="%s">%s</a>' + tc_link + '<a href="%s">%s</a></div>'
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

def loc_graph(j, desc):
    """Site-wide @graph JSON-LD with the app description in the page's language."""
    o = json.loads(j)
    for n in o.get('@graph', []):
        if n.get('@type') == 'MobileApplication': n['description'] = H.unescape(desc)
    return json.dumps(o, ensure_ascii=False, indent=1)

def meta_desc(tags):
    for t in tags:
        m = re.search(r'name="description" content="([^"]*)"', t)
        if m: return m.group(1)
    return ''

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
DIGITS = {'ar': AR_DIGITS}   # overlays may add their own (e.g. ur, bn)
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
    jsonld = [faq_jsonld(faq_items), loc_graph(graph, t['desc'])]
    keys = ['F', 'B5', 'D', 'C', 'A2']   # index order of t['day'] / t['shot_alt']
    num = DIGITS.get(l, '0123456789')
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
               '<div class="w-rect"><small>' + ('سبحان الله' if l in RTL else 'SUBHANALLAH') + '</small><b><span data-count>%s</span> <small>/ %s</small></b><span class="bar"><i data-bar></i></span></div>'
               '<div class="w-circ"><svg width="72" height="72" viewBox="0 0 72 72" aria-hidden="true"><circle cx="36" cy="36" r="29" fill="none" stroke="rgba(255,255,255,.3)" stroke-width="5" stroke-linecap="round" stroke-dasharray="136.7 182.2"/><circle data-gauge cx="36" cy="36" r="29" fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round" stroke-dasharray="49.7 182.2"/></svg><span data-count>%s</span></div>'
               '</div></div>') % (
        n0, num, img('tesbih-bg-wide'), esc(t['wSay']), fmt(n0), fmt(33), esc(t['wEye']),
        '' if l in RTL else '<span class="nm">%s</span>' % ar_name, ic('plus'), esc(t['wSay']), esc(t['wReset']), ic('x') if False else _reset_icon(),
        img('tesbih-bg'), fmt(n0), fmt(33), fmt(n0))
    sec5 = ('<section class="sec"><div class="wrap wgrid"><div class="wtxt"><span class="kicker">%s</span><h2>%s</h2><p>%s</p>'
            '<a class="link-more" style="color:var(--green);border-color:var(--green)" href="%s">%s %s</a></div>%s</div></section>') % (
        esc(t['wK']), esc(t['wH']), esc(t['wP']), FEAT_PATHS['dhikr'].get(l, FEAT_PATHS['dhikr']['en']), esc(UI[l]['dhikr']), ic('arrow-right-bold'), widgets)
    sec6 = ('<section class="sec" id="faq" style="padding-top:0"><div class="wrap"><div class="head"><h2>%s</h2></div>%s</div></section>') % (
        esc(faq_h2), faq_block(faq_items))
    sec7 = ('<section class="sec" id="download" style="padding-top:0"><div class="wrap"><div class="cta">'
            '<img class="heart" src="%s" alt="" width="88" height="88" loading="lazy"><h2>%s</h2><p>%s</p>%s<span class="salam">%s</span></div></div></section>') % (
        img('heart'), esc(t['ctaH']), esc(t['ctaP']), store_btns(l, a[1], p[1], light=True), esc(t['salam']))
    body = hero + sec1 + sec2 + sec3 + sec4 + sec5 + guides_block(l) + sec6 + sec7
    hh = head(l, t['title'], tags, jsonld, amiri=True, preload=img('bg-b-45'))
    return write(HOME[l] + 'index.html', page(l, hh, body, 'home', HOME))

GUIDES = {'en': dict(k='Guides', h='Read before you download', all='All guides', tc='Free online tasbih counter', tcp='Count your dhikr in the browser: the tasbih after prayer, istighfar, salawat.'),
          'tr': dict(k='Rehberler', h='İndirmeden önce okuyun', all='Tüm yazılar', tc='Ücretsiz online zikirmatik', tcp='Tarayıcıda zikir sayın: namaz sonrası tesbihat, istiğfar, salavat.'),
          'de': dict(k='Mehr entdecken', h='Kostenlos ausprobieren, mehr erfahren', all='Alle Funktionen', tc='Kostenloser Online-Tasbih-Zähler', tcp='Zähle deinen Dhikr im Browser: Tasbih nach dem Gebet, Istighfar, Salawat.'),
          'fr': dict(k='À découvrir', h='Essaie gratuitement, découvre la suite', all='Toutes les fonctionnalités', tc='Compteur tasbih en ligne gratuit', tcp='Compte ton dhikr dans le navigateur : tasbih après la prière, istighfar, salawat.'),
          'id': dict(k='Coba sekarang', h='Gratis, langsung di browser', all='Semua fitur', tc='Tasbih digital online gratis', tcp='Hitung zikirmu di browser: tasbih setelah salat, istigfar, selawat.')}
def guides_block(l):
    """Home section that links the blog guides and the tasbih counter, so every guide is
    one click from an indexed page (28 Nov: Google had found several only via other languages)."""
    if l not in GUIDES: return ''
    g = GUIDES[l]
    cards = '<a class="post" href="%s"><div class="post-txt"><span class="kicker" style="color:var(--green)">%s</span><h3>%s</h3><p>%s</p></div></a>' % (
        TASBIH[l], esc(TC[l]['crumb']), esc(g['tc']), esc(g['tcp']))
    if l == 'en':
        for p in LIVE['blog']['en']['posts'][:6]:
            s = slug_of(p['href']); cat = POST_META[s][0]
            cards += '<a class="post" href="/%s.html"><div class="post-txt"><span class="kicker" style="color:%s">%s</span><h3>%s</h3><p>%s</p></div></a>' % (
                s, CAT_COL[cat], esc(p['badge']), LIVE['articles'][s]['h1'] if s in LIVE['articles'] else p['h2'], p['p'])
    elif l in LART:   # this language has its own guides
        for es, ar_ in list(LART[l].items())[:6]:
            cat = POST_META[es][0]
            cards += '<a class="post" href="%s"><div class="post-txt"><span class="kicker" style="color:%s">%s</span><h3>%s</h3><p>%s</p></div></a>' % (
                ART_ALTS[es][l], CAT_COL[cat], esc(dict(BLOGX[l]['cats'])[cat]), esc(ar_['h1']), esc(ar_['desc']))
    elif l not in BLOG_PATHS:   # no blog in this language: link the feature pages instead
        for k2 in ['period', 'protect', 'quran', 'dhikr']:
            if l not in FEAT_PATHS[k2]: continue
            fd = LIVE['features'][k2][l]
            cards += '<a class="post" href="%s"><div class="post-txt"><span class="kicker" style="color:%s">%s</span><h3>%s</h3><p>%s</p></div></a>' % (
                FEAT_PATHS[k2][l], THEMES[k2]['acc'], esc(H.unescape(fd['badge'])), re.sub('<[^>]+>', '', fd['h1']), re.sub('<[^>]+>', '', fd['summary'][0]))
    more = BLOG_PATHS.get(l, HOME[l] + '#features')
    return ('<section class="sec guides" style="padding-top:0"><div class="wrap"><div class="head"><span class="kicker">%s</span><h2>%s</h2></div>'
            '<div class="posts">%s</div><p class="and"><a href="%s">%s %s</a></p></div></section>') % (
        esc(g['k']), esc(g['h']), cards, more, esc(g['all']), ic('arrow-right-bold'))

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
    st = d.get('stores') or {'apple': [APPLE % ('web-%s-%s-%d' % (key, l, i)) for i in (1, 2)],
                             'play': [PLAY % ('%s_%s_%s' % (key, w, l)) for w in ('hero', 'download')]}
    cr = d.get('crumbs') or [[u['home'], HOME[l]], [u['nav'][0], HOME[l] + '#features']]
    crumbs = ''.join('<li><a href="%s">%s</a></li>' % (h, esc(t)) for t, h in cr) + '<li aria-current="page">%s</li>' % esc(d.get('crumb_last') or H.unescape(d['badge']))
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
    if l in RTL: vis = vis.replace('<small>SUBHANALLAH</small>', '<small>سبحان الله</small>')
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
    rlinks = list(mo['reading']['links'])
    if key == 'dhikr' and l in TASBIH: rlinks.insert(0, (TASBIH[l], esc(GUIDES[l]['tc'])))
    reading = '<div class="read"><h3>%s</h3><ul>%s</ul></div>' % (mo['reading']['h3'], ''.join('<li><a href="%s">%s %s</a></li>' % (h, ic('arrow-right-bold'), t) for h, t in rlinks))
    s_more = '<section class="sec" id="more" style="padding-top:0"><div class="wrap"><div class="head"><span class="kicker">%s</span><h2>%s</h2></div><div class="rel">%s</div>%s</div></section>' % (
        esc(mo['badge']), mo['h2'], rel, reading)
    dl = d['download']
    s_dl = ('<section class="sec" id="download" style="padding-top:0"><div class="wrap"><div class="cta %s"><span class="kicker" style="color:rgba(255,255,255,.8)">%s</span><h2>%s</h2><p>%s</p>%s<span class="salam">%s</span></div></div></section>') % (
        th['cta'], esc(dl['badge']), dl['h2'], dl['p'], store_btns(l, st['apple'][1], st['play'][1], light=True), esc(dl['greeting']))
    body = hero + s_what + s_how + s_det + s_faq + s_more + s_dl
    ft, ftags, fjl = feature_head(key, l, d)
    hh = head(l, ft, ftags, fjl, amiri=(key == 'dhikr'))
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
    'spiritual-self-care-muslim-women': ('life', 'bg-a-wide'),
    'what-to-do-during-period-in-islam': ('period', 'empty-waiting'),
}
# Guides that exist only in other languages (28 Nov): no English page, so no 'en' alternate.
TOPICS = {
    'after-prayer-dhikr': ('dhikr', 'tesbih-bg-wide'),
    'ghusl-guide': ('period', 'bg-a-wide'),
    'quran-during-period': ('period', 'kurs-bg'),
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
# Each guide points at the app feature it is about (internal link to a feature page).
APPBOX = {
    'period': ('period', 'Period Mode', 'Track your cycle alongside prayer, Quran and dhikr, see the views of the four madhhabs, and keep count of the fasts to make up.'),
    'dhikr': ('dhikr', 'Dhikr widget and tasbih counter', 'Count dhikr from your home screen without opening the app.'),
    'quran': ('quran', 'Quran reading plan', 'Daily portions and khatm tracking, from a 30-day Ramadan khatm to a year-long plan.'),
    'prayer': ('protect', 'Protect My Prayer', 'Pause the apps you choose when prayer time comes in; tap “I prayed” to open them again.'),
    'life': (None, 'Lunora for Muslim women', 'Prayer times, the whole Quran, duas and dhikr, and Period Mode in one calm app. No ads.'),
}

def retired_page(slug, to):
    """Old URL kept as a pointer: noindex + canonical + instant refresh (GitHub Pages has no 301)."""
    s = ('<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="UTF-8">\n<title>Lunora</title>\n<meta name="robots" content="noindex">\n'
         '<link rel="canonical" href="%s%s">\n<meta http-equiv="refresh" content="0; url=%s">\n</head>\n<body>\n<p><a href="%s">Continue to %s%s</a></p>\n</body>\n</html>\n') % (
        SITE, to, to, to, SITE, to)
    return write('/%s.html' % slug, s)
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
    fk, ftitle, fp = APPBOX[cat]
    fhref = FEAT_PATHS[fk]['en'] if fk else '/'
    extra = (' <a href="%s">%s</a>' % (TASBIH['en'], esc(GUIDES['en']['tc']))) if fk == 'dhikr' else ''
    body += ('<aside class="appbox"><span class="kicker" style="color:%s">%s</span><h2><a href="%s">%s</a></h2><p>%s%s</p></aside>') % (
        CAT_COL[cat], 'In the Lunora app', fhref, esc(ftitle), esc(fp), extra)
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
    tags = list(d['head']['tags'])
    if len(ART_ALTS.get(slug, {})) > 1:
        tags += ['<link rel="alternate" hreflang="%s" href="%s%s">' % (x, SITE, ART_ALTS[slug][x]) for x in LANGS if x in ART_ALTS[slug]]
        tags.append('<link rel="alternate" hreflang="x-default" href="%s/%s.html">' % (SITE, slug))
    hh = head(l, d['head']['title'], tags, jsonld)
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

# ---------------------------------------------------------------- tasbih counter (28 Nov)
# Steps: (arabic, transliteration, meaning, count). count 0 = no target (free count).
_SUB, _HAM, _AKB = 'سُبْحَانَ اللّٰهِ', 'الْحَمْدُ لِلّٰهِ', 'اللّٰهُ أَكْبَرُ'
_TAHLIL = 'لَا إِلٰهَ إِلَّا اللّٰهُ وَحْدَهُ لَا شَرِيكَ لَهُ، لَهُ الْمُلْكُ وَلَهُ الْحَمْدُ وَهُوَ عَلَى كُلِّ شَيْءٍ قَدِيرٌ'
TC = {
 'en': dict(
    crumb='Tasbih counter', title='Online Tasbih Counter: Free Digital Dhikr Counter | Lunora',
    desc='A free online tasbih counter. Tap or press the space bar to count dhikr: the tasbih after prayer, Fatimah’s tasbih before sleep, istighfar and salawat.',
    pill='Free · no sign-up', h1='Online tasbih counter', lead='A free digital tasbih in your browser. Tap the circle or press the space bar to count, and choose a set below. Your count stays on this device.',
    tap='Tap to count', reset='Reset', done='Completed. May Allah accept it.', today='Today on this device', of='of', next='Next',
    sets=[('After prayer', [(_SUB, 'SubhanAllah', 'Glory be to Allah', 33), (_HAM, 'Alhamdulillah', 'All praise is for Allah', 33), (_AKB, 'Allahu Akbar', 'Allah is the Greatest', 33),
                            (_TAHLIL, 'La ilaha illallah wahdahu la sharika lah…', 'None has the right to be worshipped but Allah alone…', 1)]),
          ('Before sleep', [(_SUB, 'SubhanAllah', 'Glory be to Allah', 33), (_HAM, 'Alhamdulillah', 'All praise is for Allah', 33), (_AKB, 'Allahu Akbar', 'Allah is the Greatest', 34)]),
          ('Istighfar', [('أَسْتَغْفِرُ اللّٰهَ', 'Astaghfirullah', 'I seek Allah’s forgiveness', 100)]),
          ('Salawat', [('اللّٰهُمَّ صَلِّ عَلَى مُحَمَّدٍ', 'Allahumma salli ‘ala Muhammad', 'O Allah, send blessings upon Muhammad', 100)]),
          ('Free count', [('لَا إِلٰهَ إِلَّا اللّٰهُ', 'La ilaha illallah', 'There is no god but Allah', 0)])],
    how_h='How to use it', how=[('Pick a set', 'After prayer, before sleep, istighfar, salawat, or a free count with no target.'),
                                 ('Tap or press space', 'Each tap adds one. The ring fills as you go and moves on to the next phrase by itself.'),
                                 ('Finish and reset', 'At the end you see your total for today. Reset starts the set again.')],
    src_h='Where the numbers come from',
    src=['<b>After every prayer:</b> the Prophet ﷺ taught saying SubhanAllah 33 times, Alhamdulillah 33 times and Allahu Akbar 33 times, then completing the hundred with “La ilaha illallah wahdahu la sharika lah, lahul-mulku wa lahul-hamdu wa huwa ‘ala kulli shay’in qadir”. (<a href="https://sunnah.com/muslim:597" rel="noopener">Sahih Muslim 597</a>)',
         '<b>Before sleep:</b> he taught Ali and Fatimah to say SubhanAllah 33 times, Alhamdulillah 33 times and Allahu Akbar 34 times when going to bed, and told them it was better for them than a servant. (<a href="https://sunnah.com/bukhari:3113" rel="noopener">Sahih al-Bukhari 3113</a>, <a href="https://sunnah.com/muslim:2727" rel="noopener">Sahih Muslim 2727</a>)'],
    faq_h='Questions', faq=[
        ('Is it fine to count dhikr with a digital counter?', 'Counting on the fingers is the Sunnah, and the Prophet ﷺ encouraged it. Many scholars see beads or a counter as a permissible tool for keeping count. If you are unsure, ask a scholar you trust.'),
        ('Does the counter save my count?', 'Yes, on this device only. Your count and today’s total are stored in your browser. Nothing is sent to us, and there is no account.'),
        ('Can I use it during my period?', 'Yes. Dhikr, dua and salawat are open to you during your period; the counter is a good companion for those days.'),
        ('Is there a tasbih for my home screen?', 'Lunora has a tasbih widget for the iPhone and Android home screen, with a sourced dhikr library, so you can count without opening an app.')],
    cta_h='Keep your tasbih on your home screen', cta_p='Lunora’s dhikr widget counts from your home screen, alongside prayer times, the Quran and Period Mode. No ads, in 9 languages.', widget='See the dhikr widget'),
 'tr': dict(
    crumb='Zikirmatik', title='Online Zikirmatik: Ücretsiz Dijital Tesbih Sayacı | Lunora',
    desc='Ücretsiz online zikirmatik. Dokunarak ya da boşluk tuşuyla zikir sayın: namaz sonrası tesbihat, yatmadan önce Hz. Fâtıma tesbihi, istiğfar ve salavat.',
    pill='Ücretsiz · üyelik yok', h1='Online zikirmatik', lead='Tarayıcınızda ücretsiz bir dijital tesbih. Saymak için daireye dokunun ya da boşluk tuşuna basın, aşağıdan bir set seçin. Sayınız bu cihazda kalır.',
    tap='Saymak için dokunun', reset='Sıfırla', done='Tamamlandı. Allah kabul etsin.', today='Bugün bu cihazda', of='/', next='Sonraki',
    sets=[('Namaz sonrası', [(_SUB, 'Sübhânallah', 'Allah her türlü eksiklikten uzaktır', 33), (_HAM, 'Elhamdülillah', 'Hamd Allah’adır', 33), (_AKB, 'Allâhu ekber', 'Allah en büyüktür', 33),
                             (_TAHLIL, 'Lâ ilâhe illallâhu vahdehû lâ şerîke leh…', 'Allah’tan başka ilah yoktur, O tektir, ortağı yoktur…', 1)]),
          ('Yatmadan önce', [(_SUB, 'Sübhânallah', 'Allah her türlü eksiklikten uzaktır', 33), (_HAM, 'Elhamdülillah', 'Hamd Allah’adır', 33), (_AKB, 'Allâhu ekber', 'Allah en büyüktür', 34)]),
          ('İstiğfar', [('أَسْتَغْفِرُ اللّٰهَ', 'Estağfirullah', 'Allah’tan bağışlanma dilerim', 100)]),
          ('Salavat', [('اللّٰهُمَّ صَلِّ عَلَى مُحَمَّدٍ', 'Allâhümme salli alâ Muhammed', 'Allah’ım, Muhammed’e salât eyle', 100)]),
          ('Serbest', [('لَا إِلٰهَ إِلَّا اللّٰهُ', 'Lâ ilâhe illallah', 'Allah’tan başka ilah yoktur', 0)])],
    how_h='Nasıl kullanılır', how=[('Bir set seçin', 'Namaz sonrası, yatmadan önce, istiğfar, salavat ya da hedefsiz serbest sayım.'),
                                    ('Dokunun ya da boşluğa basın', 'Her dokunuş bir sayar. Halka doldukça bir sonraki zikre kendiliğinden geçer.'),
                                    ('Bitirin, sıfırlayın', 'Sonunda bugünkü toplamınızı görürsünüz. Sıfırla, seti baştan başlatır.')],
    src_h='Sayılar nereden geliyor',
    src=['<b>Her namazdan sonra:</b> Peygamber Efendimiz ﷺ 33 kez Sübhânallah, 33 kez Elhamdülillah, 33 kez Allâhu ekber demeyi ve yüzü “Lâ ilâhe illallâhu vahdehû lâ şerîke leh, lehü’l-mülkü ve lehü’l-hamdü ve hüve alâ külli şey’in kadîr” ile tamamlamayı öğretti. (<a href="https://sunnah.com/muslim:597" rel="noopener">Müslim, 597</a>)',
         '<b>Yatmadan önce:</b> Hz. Ali ve Hz. Fâtıma’ya yatağa girerken 33 kez Sübhânallah, 33 kez Elhamdülillah ve 34 kez Allâhu ekber demelerini öğretti ve bunun onlar için bir hizmetçiden daha hayırlı olduğunu söyledi. (<a href="https://sunnah.com/bukhari:3113" rel="noopener">Buhârî, 3113</a>; <a href="https://sunnah.com/muslim:2727" rel="noopener">Müslim, 2727</a>)'],
    faq_h='Sorular', faq=[
        ('Zikri dijital sayaçla saymak uygun mu?', 'Parmaklarla saymak sünnettir ve Peygamber Efendimiz ﷺ bunu teşvik etmiştir. Pek çok âlim tesbih ya da sayacı saymayı kolaylaştıran caiz bir araç olarak görür. Emin değilseniz güvendiğiniz bir âlime danışın.'),
        ('Sayaç sayımı kaydediyor mu?', 'Evet, yalnız bu cihazda. Sayınız ve bugünkü toplamınız tarayıcınızda saklanır. Bize hiçbir şey gönderilmez, hesap gerekmez.'),
        ('Özel günlerimde kullanabilir miyim?', 'Evet. Zikir, dua ve salavat özel günlerinizde de size açıktır; sayaç bu günler için iyi bir yol arkadaşıdır.'),
        ('Ana ekranım için bir tesbih var mı?', 'Lunora’da iPhone ve Android ana ekranı için kaynaklı zikir kütüphanesiyle bir tesbih widget’ı var; uygulamayı açmadan sayabilirsiniz.')],
    cta_h='Tesbihiniz ana ekranınızda olsun', cta_p='Lunora’nın zikir widget’ı ana ekrandan sayar; namaz vakitleri, Kur’an ve Dönem Modu da bir arada. Reklamsız, 9 dilde.', widget='Zikir widget’ını görün'),
 'de': dict(
    crumb='Tasbih-Zähler', title='Tasbih-Zähler online: Kostenloser Dhikr-Zähler | Lunora',
    desc='Kostenloser Tasbih-Zähler online. Tippe oder drücke die Leertaste, um Dhikr zu zählen: Tasbih nach dem Gebet, Fatimas Tasbih vor dem Schlafen, Istighfar, Salawat.',
    pill='Kostenlos · ohne Anmeldung', h1='Tasbih-Zähler online', lead='Eine kostenlose digitale Tasbih in deinem Browser. Tippe auf den Kreis oder drücke die Leertaste, um zu zählen, und wähle unten ein Set. Dein Zählstand bleibt auf diesem Gerät.',
    tap='Zum Zählen tippen', reset='Zurücksetzen', done='Geschafft. Möge Allah es annehmen.', today='Heute auf diesem Gerät', of='von', next='Weiter',
    sets=[('Nach dem Gebet', [(_SUB, 'Subhanallah', 'Gepriesen sei Allah', 33), (_HAM, 'Alhamdulillah', 'Alles Lob gebührt Allah', 33), (_AKB, 'Allahu Akbar', 'Allah ist der Größte', 33),
                              (_TAHLIL, 'La ilaha illallahu wahdahu la scharika lah…', 'Es gibt keinen Gott außer Allah, dem Einen, ohne Partner…', 1)]),
          ('Vor dem Schlafen', [(_SUB, 'Subhanallah', 'Gepriesen sei Allah', 33), (_HAM, 'Alhamdulillah', 'Alles Lob gebührt Allah', 33), (_AKB, 'Allahu Akbar', 'Allah ist der Größte', 34)]),
          ('Istighfar', [('أَسْتَغْفِرُ اللّٰهَ', 'Astaghfirullah', 'Ich bitte Allah um Vergebung', 100)]),
          ('Salawat', [('اللّٰهُمَّ صَلِّ عَلَى مُحَمَّدٍ', 'Allahumma salli ‘ala Muhammad', 'O Allah, segne Muhammad', 100)]),
          ('Frei zählen', [('لَا إِلٰهَ إِلَّا اللّٰهُ', 'La ilaha illallah', 'Es gibt keinen Gott außer Allah', 0)])],
    how_h='So funktioniert es', how=[('Set wählen', 'Nach dem Gebet, vor dem Schlafen, Istighfar, Salawat oder frei ohne Ziel.'),
                                      ('Tippen oder Leertaste', 'Jedes Tippen zählt eins. Der Ring füllt sich und springt von selbst zum nächsten Satz.'),
                                      ('Fertig und zurücksetzen', 'Am Ende siehst du deine Summe für heute. „Zurücksetzen“ startet das Set neu.')],
    src_h='Woher die Zahlen kommen',
    src=['<b>Nach jedem Gebet:</b> Der Prophet ﷺ lehrte, 33-mal Subhanallah, 33-mal Alhamdulillah und 33-mal Allahu Akbar zu sagen und die Hundert mit „La ilaha illallahu wahdahu la scharika lah, lahul-mulku wa lahul-hamdu wa huwa ‘ala kulli schay’in qadir“ zu vollenden. (<a href="https://sunnah.com/muslim:597" rel="noopener">Sahih Muslim 597</a>)',
         '<b>Vor dem Schlafen:</b> Er lehrte Ali und Fatima, beim Zubettgehen 33-mal Subhanallah, 33-mal Alhamdulillah und 34-mal Allahu Akbar zu sagen, und sagte, das sei besser für sie als ein Diener. (<a href="https://sunnah.com/bukhari:3113" rel="noopener">Sahih al-Bukhari 3113</a>, <a href="https://sunnah.com/muslim:2727" rel="noopener">Sahih Muslim 2727</a>)'],
    faq_h='Fragen', faq=[
        ('Darf man Dhikr mit einem digitalen Zähler zählen?', 'Das Zählen an den Fingern ist Sunna, und der Prophet ﷺ hat dazu ermutigt. Viele Gelehrte sehen Perlen oder einen Zähler als erlaubtes Hilfsmittel zum Zählen. Frag im Zweifel eine Gelehrte oder einen Gelehrten deines Vertrauens.'),
        ('Speichert der Zähler meinen Stand?', 'Ja, nur auf diesem Gerät. Dein Zählstand und die Summe für heute bleiben in deinem Browser. Nichts wird an uns gesendet, ein Konto brauchst du nicht.'),
        ('Kann ich ihn während meiner Periode nutzen?', 'Ja. Dhikr, Dua und Salawat stehen dir auch während deiner Periode offen; der Zähler ist für diese Tage ein guter Begleiter.'),
        ('Gibt es eine Tasbih für den Startbildschirm?', 'Lunora hat ein Tasbih-Widget für den Startbildschirm von iPhone und Android, mit einer Dhikr-Bibliothek mit Quellen. So zählst du, ohne eine App zu öffnen.')],
    cta_h='Deine Tasbih auf dem Startbildschirm', cta_p='Das Dhikr-Widget von Lunora zählt direkt auf dem Startbildschirm, dazu Gebetszeiten, der Koran und der Periodenmodus. Ohne Werbung, in 9 Sprachen.', widget='Zum Dhikr-Widget'),
 'fr': dict(
    crumb='Compteur tasbih', title='Compteur tasbih en ligne : compteur de dhikr gratuit | Lunora',
    desc='Compteur tasbih en ligne et gratuit. Touche ou appuie sur la barre d’espace pour compter ton dhikr : tasbih après la prière, tasbih de Fatima avant de dormir, istighfar, salawat.',
    pill='Gratuit · sans inscription', h1='Compteur tasbih en ligne', lead='Un tasbih numérique gratuit dans ton navigateur. Touche le cercle ou appuie sur la barre d’espace pour compter, et choisis une série ci-dessous. Ton compte reste sur cet appareil.',
    tap='Touche pour compter', reset='Recommencer', done='Terminé. Qu’Allah l’accepte.', today='Aujourd’hui sur cet appareil', of='sur', next='Suivant',
    sets=[('Après la prière', [(_SUB, 'SubhanAllah', 'Gloire à Allah', 33), (_HAM, 'Alhamdoulillah', 'Louange à Allah', 33), (_AKB, 'Allahou Akbar', 'Allah est le plus grand', 33),
                               (_TAHLIL, 'La ilaha illa Allah wahdahou la charika lah…', 'Nul ne mérite d’être adoré en dehors d’Allah, Seul, sans associé…', 1)]),
          ('Avant de dormir', [(_SUB, 'SubhanAllah', 'Gloire à Allah', 33), (_HAM, 'Alhamdoulillah', 'Louange à Allah', 33), (_AKB, 'Allahou Akbar', 'Allah est le plus grand', 34)]),
          ('Istighfar', [('أَسْتَغْفِرُ اللّٰهَ', 'Astaghfiroullah', 'Je demande pardon à Allah', 100)]),
          ('Salawat', [('اللّٰهُمَّ صَلِّ عَلَى مُحَمَّدٍ', 'Allahoumma salli ‘ala Muhammad', 'Ô Allah, prie sur Muhammad', 100)]),
          ('Compte libre', [('لَا إِلٰهَ إِلَّا اللّٰهُ', 'La ilaha illa Allah', 'Il n’y a de dieu qu’Allah', 0)])],
    how_h='Comment ça marche', how=[('Choisis une série', 'Après la prière, avant de dormir, istighfar, salawat, ou un compte libre sans objectif.'),
                                     ('Touche ou appuie sur espace', 'Chaque touche ajoute un. L’anneau se remplit et passe tout seul à la formule suivante.'),
                                     ('Termine et recommence', 'À la fin, tu vois ton total du jour. « Recommencer » relance la série.')],
    src_h='D’où viennent ces nombres',
    src=['<b>Après chaque prière :</b> le Prophète ﷺ a enseigné de dire 33 fois SubhanAllah, 33 fois Alhamdoulillah et 33 fois Allahou Akbar, puis de compléter la centaine par « La ilaha illa Allah wahdahou la charika lah, lahoul-moulkou wa lahoul-hamdou wa houwa ‘ala koulli chay’in qadir ». (<a href="https://sunnah.com/muslim:597" rel="noopener">Sahih Muslim 597</a>)',
         '<b>Avant de dormir :</b> il a enseigné à Ali et Fatima de dire, au moment de se coucher, 33 fois SubhanAllah, 33 fois Alhamdoulillah et 34 fois Allahou Akbar, et leur a dit que c’était meilleur pour eux qu’un serviteur. (<a href="https://sunnah.com/bukhari:3113" rel="noopener">Sahih al-Boukhari 3113</a>, <a href="https://sunnah.com/muslim:2727" rel="noopener">Sahih Muslim 2727</a>)'],
    faq_h='Questions', faq=[
        ('Peut-on compter son dhikr avec un compteur numérique ?', 'Compter sur les doigts est la Sunna, et le Prophète ﷺ y a encouragé. Beaucoup de savants considèrent le chapelet ou un compteur comme un outil permis pour garder le compte. En cas de doute, demande à une personne savante de confiance.'),
        ('Le compteur garde-t-il mon compte ?', 'Oui, sur cet appareil uniquement. Ton compte et ton total du jour restent dans ton navigateur. Rien ne nous est envoyé, et il n’y a pas de compte à créer.'),
        ('Puis-je l’utiliser pendant mes règles ?', 'Oui. Le dhikr, les douas et les salawat te restent ouverts pendant tes règles ; le compteur t’accompagne bien ces jours-là.'),
        ('Existe-t-il un tasbih pour l’écran d’accueil ?', 'Lunora propose un widget tasbih pour l’écran d’accueil de l’iPhone et d’Android, avec une bibliothèque de dhikr sourcés, pour compter sans ouvrir d’appli.')],
    cta_h='Ton tasbih sur ton écran d’accueil', cta_p='Le widget dhikr de Lunora compte depuis l’écran d’accueil, avec les horaires de prière, le Coran et le Mode règles. Sans publicité, en 9 langues.', widget='Voir le widget dhikr'),
 'id': dict(
    crumb='Tasbih digital', title='Tasbih Digital Online: Penghitung Zikir Gratis | Lunora',
    desc='Tasbih digital online gratis. Ketuk atau tekan spasi untuk menghitung zikir: tasbih setelah salat, tasbih Fatimah sebelum tidur, istigfar, dan selawat.',
    pill='Gratis · tanpa daftar', h1='Tasbih digital online', lead='Tasbih digital gratis di browsermu. Ketuk lingkaran atau tekan spasi untuk menghitung, lalu pilih bacaan di bawah. Hitunganmu tersimpan di perangkat ini.',
    tap='Ketuk untuk menghitung', reset='Ulangi', done='Selesai. Semoga Allah menerimanya.', today='Hari ini di perangkat ini', of='dari', next='Berikutnya',
    sets=[('Setelah salat', [(_SUB, 'Subhanallah', 'Mahasuci Allah', 33), (_HAM, 'Alhamdulillah', 'Segala puji bagi Allah', 33), (_AKB, 'Allahu Akbar', 'Allah Mahabesar', 33),
                             (_TAHLIL, 'La ilaha illallahu wahdahu la syarika lah…', 'Tiada tuhan selain Allah, Yang Maha Esa, tiada sekutu bagi-Nya…', 1)]),
          ('Sebelum tidur', [(_SUB, 'Subhanallah', 'Mahasuci Allah', 33), (_HAM, 'Alhamdulillah', 'Segala puji bagi Allah', 33), (_AKB, 'Allahu Akbar', 'Allah Mahabesar', 34)]),
          ('Istigfar', [('أَسْتَغْفِرُ اللّٰهَ', 'Astaghfirullah', 'Aku memohon ampun kepada Allah', 100)]),
          ('Selawat', [('اللّٰهُمَّ صَلِّ عَلَى مُحَمَّدٍ', 'Allahumma shalli ‘ala Muhammad', 'Ya Allah, limpahkan selawat kepada Muhammad', 100)]),
          ('Bebas', [('لَا إِلٰهَ إِلَّا اللّٰهُ', 'La ilaha illallah', 'Tiada tuhan selain Allah', 0)])],
    how_h='Cara memakainya', how=[('Pilih bacaan', 'Setelah salat, sebelum tidur, istigfar, selawat, atau hitungan bebas tanpa target.'),
                                   ('Ketuk atau tekan spasi', 'Setiap ketukan menambah satu. Lingkaran terisi dan berpindah sendiri ke bacaan berikutnya.'),
                                   ('Selesai dan ulangi', 'Di akhir kamu melihat total hari ini. Tombol Ulangi memulai bacaan dari awal.')],
    src_h='Dari mana angka-angka ini',
    src=['<b>Setiap selesai salat:</b> Nabi ﷺ mengajarkan membaca Subhanallah 33 kali, Alhamdulillah 33 kali, dan Allahu Akbar 33 kali, lalu menggenapkan seratus dengan “La ilaha illallahu wahdahu la syarika lah, lahul-mulku wa lahul-hamdu wa huwa ‘ala kulli syai’in qadir”. (<a href="https://sunnah.com/muslim:597" rel="noopener">HR. Muslim no. 597</a>)',
         '<b>Sebelum tidur:</b> beliau mengajarkan kepada Ali dan Fatimah untuk membaca Subhanallah 33 kali, Alhamdulillah 33 kali, dan Allahu Akbar 34 kali ketika hendak tidur, dan bersabda bahwa itu lebih baik bagi mereka daripada seorang pembantu. (<a href="https://sunnah.com/bukhari:3113" rel="noopener">HR. Bukhari no. 3113</a>; <a href="https://sunnah.com/muslim:2727" rel="noopener">HR. Muslim no. 2727</a>)'],
    faq_h='Pertanyaan', faq=[
        ('Bolehkah menghitung zikir dengan penghitung digital?', 'Menghitung dengan jari adalah sunah, dan Nabi ﷺ menganjurkannya. Banyak ulama memandang tasbih atau alat penghitung sebagai sarana yang boleh untuk menjaga hitungan. Jika ragu, tanyakan kepada ustaz atau ustazah yang kamu percaya.'),
        ('Apakah hitunganku tersimpan?', 'Ya, hanya di perangkat ini. Hitungan dan total hari ini tersimpan di browsermu. Tidak ada yang dikirim kepada kami, dan tidak perlu akun.'),
        ('Bolehkah dipakai saat haid?', 'Boleh. Zikir, doa, dan selawat tetap terbuka bagimu saat haid; penghitung ini teman yang baik untuk hari-hari itu.'),
        ('Ada tasbih untuk layar utama?', 'Lunora punya widget tasbih untuk layar utama iPhone dan Android, dengan pustaka zikir bersumber, jadi kamu bisa menghitung tanpa membuka aplikasi.')],
    cta_h='Tasbihmu di layar utama', cta_p='Widget zikir Lunora menghitung langsung dari layar utama, bersama jadwal salat, Al-Qur’an, dan Mode Haid. Tanpa iklan, dalam 9 bahasa.', widget='Lihat aplikasinya'),
}

TC_JS = r"""<script>
(function(){var root=document.getElementById('tc');if(!root)return;var S=JSON.parse(root.dataset.sets),L=JSON.parse(root.dataset.l);
var si=0,st=0,c=0,K='lunora.tc.'+new Date().toISOString().slice(0,10),tot=0;try{tot=parseInt(localStorage.getItem(K)||'0',10)||0}catch(e){}
var q=function(s){return root.querySelector(s)},btn=q('.tc-tap'),ring=q('.tc-ring'),n=q('.tc-n'),of=q('.tc-of'),ar=q('.tc-ar'),tr=q('.tc-tr'),mn=q('.tc-mean'),dn=q('.tc-done'),td=q('.tc-today b'),stp=q('.tc-steps');
function save(){try{localStorage.setItem(K,String(tot))}catch(e){}}
function draw(){var step=S[si][1][st],t=step[3];n.textContent=c;of.textContent=t?(L.of+' '+t):'∞';ar.textContent=step[0];tr.textContent=step[1];mn.textContent=step[2];
ring.style.setProperty('--p',t?Math.min(c/t,1):(c%33)/33);td.textContent=tot;
stp.innerHTML=S[si][1].length<2?'':S[si][1].map(function(s,i){var w=s[1].replace('…','').split(' '),k=/^(La|Lâ|Allahu|Allâhu|Allahou)$/.test(w[0])?2:1;return '<span class="'+(i<st?'ok':i==st?'on':'')+'">'+w.slice(0,k).join(' ')+' · '+s[3]+'</span>'}).join('')}
function setSet(i){si=i;st=0;c=0;dn.hidden=true;root.querySelectorAll('.tc-sets button').forEach(function(b,j){b.setAttribute('aria-pressed',j==i?'true':'false')});draw()}
function tap(){if(!dn.hidden)return;var t=S[si][1][st][3];c++;tot++;save();if(navigator.vibrate)navigator.vibrate(12);
if(t&&c>=t){if(navigator.vibrate)navigator.vibrate([30,40,30]);if(st<S[si][1].length-1){draw();setTimeout(function(){st++;c=0;draw()},450);return}draw();dn.hidden=false;return}draw()}
btn.addEventListener('click',tap);q('.tc-reset').addEventListener('click',function(){setSet(si)});
root.querySelectorAll('.tc-sets button').forEach(function(b,i){b.addEventListener('click',function(){setSet(i)})});
document.addEventListener('keydown',function(e){if((e.code=='Space'||e.key==' ')&&!/INPUT|TEXTAREA|BUTTON|SUMMARY/.test(document.activeElement.tagName)){e.preventDefault();tap()}});
setSet(0)})();
</script>"""

def tasbih_page(l):
    t = TC[l]; u = UI[l]; path = TASBIH[l]
    apple = [APPLE % ('web-tasbih-%s-%d' % (l, i)) for i in (1, 2)]
    play = [PLAY % ('tasbih_%s_%d' % (l, i)) for i in (1, 2)]
    canon = SITE + path
    tags = ['<meta name="description" content="%s">' % esc(t['desc']), '<link rel="canonical" href="%s">' % canon]
    tags += ['<link rel="alternate" hreflang="%s" href="%s%s">' % (x, SITE, TASBIH[x]) for x in LANGS if x in TASBIH]
    tags += ['<link rel="alternate" hreflang="x-default" href="%s%s">' % (SITE, TASBIH['en']),
             '<meta property="og:title" content="%s">' % esc(t['title']), '<meta property="og:description" content="%s">' % esc(t['desc']),
             '<meta property="og:url" content="%s">' % canon, '<meta property="og:image" content="%s/icon-192.png">' % SITE,
             '<meta property="og:type" content="website">', '<meta property="og:site_name" content="Lunora">', '<meta property="og:locale" content="%s">' % OGLOC[l],
             '<meta name="twitter:card" content="summary">']
    app_ld = json.dumps({'@context': 'https://schema.org', '@type': 'WebApplication', 'name': t['h1'], 'url': canon, 'description': t['desc'],
                         'applicationCategory': 'LifestyleApplication', 'operatingSystem': 'Any', 'inLanguage': l, 'isAccessibleForFree': True,
                         'offers': {'@type': 'Offer', 'price': '0', 'priceCurrency': 'USD'},
                         'publisher': {'@type': 'Organization', 'name': 'Lunora', 'url': SITE + '/'}}, ensure_ascii=False, indent=1)
    crumb_ld = json.dumps({'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': 1, 'name': u['home'], 'item': SITE + HOME[l]}, {'@type': 'ListItem', 'position': 2, 'name': t['crumb'], 'item': canon}]}, ensure_ascii=False)
    faq_items = [{'q': esc(q), 'a': esc(a)} for q, a in t['faq']]
    sets_json = json.dumps([[n, s] for n, s in t['sets']], ensure_ascii=False)
    lbl = json.dumps({'of': t['of']}, ensure_ascii=False)
    chips = ''.join('<button type="button" aria-pressed="%s">%s</button>' % ('true' if i == 0 else 'false', esc(n)) for i, (n, _) in enumerate(t['sets']))
    counter = ('<div class="tc" id="tc" data-sets="%s" data-l="%s">'
               '<div class="tc-sets filters" role="group" aria-label="%s">%s</div>'
               '<div class="tc-steps" aria-hidden="true"></div>'
               '<button class="tc-tap" type="button" aria-label="%s"><span class="tc-ring"><i></i></span>'
               '<span class="tc-mid"><b class="tc-n" aria-live="polite">0</b><small class="tc-of"></small></span></button>'
               '<p class="tc-ar" lang="ar" dir="rtl"></p><p class="tc-tr"></p><p class="tc-mean"></p>'
               '<p class="tc-done" hidden>%s</p>'
               '<div class="tc-foot"><span class="tc-today">%s: <b>0</b></span><button class="tc-reset" type="button">%s %s</button></div>'
               '</div>') % (att(sets_json), att(lbl), esc(t['crumb']), chips, esc(t['tap']), esc(t['done']), esc(t['today']), _reset_icon(), esc(t['reset']))
    crumbs = '<li><a href="%s">%s</a></li><li aria-current="page">%s</li>' % (HOME[l], esc(u['home']), esc(t['crumb']))
    hero = ('<section class="phero tc-hero"><img class="bg" src="%s" alt="" style="--pos:20%% 50%%"><div class="phero-wash"></div>'
            '<div class="wrap phero-grid"><div class="phero-txt"><ol class="crumbs">%s</ol><span class="pill green">%s</span><h1>%s</h1><p class="lead">%s</p></div>'
            '<div class="phero-vis">%s</div></div></section>') % (img('tesbih-bg-wide'), crumbs, esc(t['pill']), esc(t['h1']), esc(t['lead']), counter)
    steps = ''.join('<li class="step"><span class="num">%d</span><h3>%s</h3><p>%s</p></li>' % (i + 1, esc(a), esc(b)) for i, (a, b) in enumerate(t['how']))
    s_how = '<section class="sec" style="--acc:#3F6B55;--line:#8FB09E"><div class="wrap"><div class="head"><h2>%s</h2></div><ol class="steps" style="--n:3">%s</ol></div></section>' % (esc(t['how_h']), steps)
    s_src = '<section class="sec" style="padding-top:0"><div class="wrap prose-narrow"><div class="head"><h2>%s</h2></div>%s</div></section>' % (
        esc(t['src_h']), ''.join('<p class="tc-src">%s</p>' % p for p in t['src']))
    s_faq = '<section class="sec" id="faq" style="padding-top:0"><div class="wrap"><div class="head"><h2>%s</h2></div>%s</div></section>' % (esc(t['faq_h']), faq_block(faq_items))
    s_dl = ('<section class="sec" id="download" style="padding-top:0"><div class="wrap"><div class="cta"><h2>%s</h2><p>%s</p>%s'
            '<a class="link-more" href="%s" style="color:#fff;border-color:rgba(255,255,255,.6);margin-top:18px">%s %s</a></div></div></section>') % (
        esc(t['cta_h']), esc(t['cta_p']), store_btns(l, apple[1], play[1], light=True), FEAT_PATHS['dhikr'].get(l, HOME[l] + '#features'), esc(t['widget']), ic('arrow-right-bold'))
    body = hero + s_how + s_src + s_faq + s_dl + TC_JS
    hh = head(l, t['title'], tags, [app_ld, crumb_ld, faq_jsonld(faq_items)], amiri=True)
    return write(path, page(l, hh, body, 'features', TASBIH))

# ---------------------------------------------------------------- per-language content files (28 Nov)
# _build/content/lang/<l>.json holds one language's content. It is deep-merged over the
# built-in dictionaries above (dicts merge, lists and strings replace), so a file can
# add a whole new language or only fix parts of an existing one. Format: _build/i18n/FORMAT.md
LART = {}    # {lang: {en_slug: article}}   translated guides
BLOGX = {}   # {lang: blog index copy}       for languages with their own guides
ARTUI = {}   # {lang: article page labels}
ART_ALTS = {}  # {en_slug: {lang: path}}

def _merge(base, over):
    if isinstance(base, dict) and isinstance(over, dict):
        out = dict(base)
        for k, v in over.items(): out[k] = _merge(base.get(k), v) if k in base else v
        return out
    return over

def feature_head(key, l, d):
    alts = FEAT_PATHS[key]; canon = SITE + alts[l]
    hre = ['<link rel="alternate" hreflang="%s" href="%s%s">' % (x, SITE, alts[x]) for x in LANGS if x in alts]
    hre.append('<link rel="alternate" hreflang="x-default" href="%s%s">' % (SITE, alts['en']))
    if 'seo' in d:
        s = d['seo']
        ogimg = [t for t in LIVE['features'][key]['en']['head']['tags'] if 'og:image' in t]
        tags = ['<meta name="description" content="%s">' % att(s['desc']), '<link rel="canonical" href="%s">' % canon] + hre + [
            '<meta property="og:title" content="%s">' % att(s.get('og_title') or s['title']),
            '<meta property="og:description" content="%s">' % att(s.get('og_desc') or s['desc']),
            '<meta property="og:url" content="%s">' % canon] + ogimg + [
            '<meta property="og:type" content="website">', '<meta property="og:site_name" content="Lunora">',
            '<meta property="og:locale" content="%s">' % OGLOC[l], '<meta name="twitter:card" content="summary">']
        crumb = json.dumps({'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': UI[l]['home'], 'item': SITE + HOME[l]},
            {'@type': 'ListItem', 'position': 2, 'name': H.unescape(d.get('crumb_last') or d['badge']), 'item': canon}]}, ensure_ascii=False)
        graph = [j for j in LIVE['home']['en']['head']['jsonld'] if '"@graph"' in j][0]
        return s['title'], tags, [faq_jsonld(d['faq']['items']), crumb, loc_graph(graph, s['desc'])]
    tags = [t for t in d['head']['tags'] if 'hreflang=' not in t]
    i = next(n for n, t in enumerate(tags) if 'rel="canonical"' in t) + 1
    jl = [loc_graph(j, meta_desc(tags)) if '"@graph"' in j else j for j in d['head']['jsonld']]
    return d['head']['title'], tags[:i] + hre + tags[i:], jl

def load_overlays():
    import glob
    files = glob.glob(os.path.join(B, 'content', 'lang', '*.json')) + glob.glob(os.path.join(B, 'content', 'lang', '*', '*.json'))
    only = os.environ.get('LUNORA_LANG')   # writers check their own language alone
    for f in sorted(files):
        if only and os.path.relpath(f, os.path.join(B, 'content', 'lang')).split(os.sep)[0].split('.')[0] != only: continue
        o = json.load(open(f)); l = o['lang']
        if l not in LANGS:
            LANGS.append(l); HOME[l] = '/%s/' % l
        if 'name' in o: LNAME[l] = o['name']
        if 'ogloc' in o: OGLOC[l] = o['ogloc']
        if o.get('rtl'): RTL.add(l)
        if 'digits' in o: DIGITS[l] = o['digits']
        if 'ui' in o: UI[l] = _merge(UI.get(l, {}), o['ui'])
        if 'rating' in o: RATING[l] = o['rating']
        if 'rating_short' in o: RATING_SHORT[l] = o['rating_short']
        if 'home' in o: HT[l] = _merge(HT.get(l, {}), o['home'])
        if 'reviews' in o: REVIEWS[l] = o['reviews']
        if 'home_faq' in o:
            hf = o['home_faq']
            if l in LIVE['home']:
                LIVE['home'][l]['faq']['items'] = [{'q': esc(q), 'a': esc(a)} for q, a in hf['items']]
                if hf.get('h2'): FAQ_H2[l] = hf['h2']
            else:
                NEW_FAQ[l] = (hf['h2'], [tuple(x) for x in hf['items']])
        if 'disclaim' in o: DISCLAIM[l] = o['disclaim']
        if 'guides' in o: GUIDES[l] = _merge(GUIDES.get(l, {}), o['guides'])
        if 'tasbih' in o:
            t = dict(o['tasbih']); path = t.pop('path', None)
            if 'sets' in t: t['sets'] = [(n, [tuple(x) for x in st]) for n, st in t['sets']]
            for k2 in ('how', 'faq'):
                if k2 in t: t[k2] = [tuple(x) for x in t[k2]]
            TC[l] = _merge(TC.get(l, {}), t)
            if path: TASBIH[l] = path
        for k, fd in o.get('features', {}).items():
            LIVE['features'][k][l] = _merge(LIVE['features'][k].get(l, {}), fd)
            if 'path' in fd: FEAT_PATHS[k][l] = fd['path']
        if 'article_ui' in o: ARTUI[l] = o['article_ui']
        if 'blog' in o:
            BLOGX[l] = o['blog']; BLOG_PATHS[l] = o['blog']['path']
        for es, a in o.get('articles', {}).items():
            assert es in POST_META or es in TOPICS, (f, es)
            if es in TOPICS: POST_META.setdefault(es, TOPICS[es])
            LART.setdefault(l, {})[es] = a
            ART_ALTS.setdefault(es, {} if es in TOPICS else {'en': '/%s.html' % es})[l] = '/%s/%s.html' % (l, a['slug'])

def article_page_l(es, l):
    """A guide in another language (body written for that market, not a word-for-word translation)."""
    a = LART[l][es]; au = ARTUI[l]; u = UI[l]; cat, im = POST_META[es]; bx = BLOGX[l]
    path = ART_ALTS[es][l]; canon = SITE + path
    cats = dict(bx['cats'])
    crumbs = '<li><a href="%s">%s</a></li><li><a href="%s">%s</a></li><li aria-current="page">%s</li>' % (
        HOME[l], esc(u['home']), BLOG_PATHS[l], esc(u['blogLead']), esc(a.get('crumb') or cats[cat]))
    hero = ('<section class="ahero"><img class="bg" src="%s" alt=""><div class="ahero-wash"></div><div class="wrap"><ol class="crumbs" style="justify-content:center">%s</ol>'
            '<span class="kicker" style="color:%s">%s</span><h1>%s</h1><p class="meta">%s</p></div></section>') % (
        img(im), crumbs, CAT_COL[cat], esc(cats[cat]), esc(a['h1']), esc('%s · %s %s' % (a['date_label'], a['minutes'], u['minread'])))
    faq = a.get('faq') or []
    faq_html = ('<h2>%s</h2>%s' % (esc(au['faq_h']), ''.join('<div class="faq-item"><h3>%s</h3><p>%s</p></div>' % (esc(q), x) for q, x in faq))) if faq else ''
    body = '<article class="prose">%s%s</article>' % (a['body'], faq_html)
    fk = APPBOX[cat][0]; bt, bp = au['appbox'][cat]
    fhref = FEAT_PATHS[fk].get(l, HOME[l] + '#features') if fk else HOME[l]
    extra = (' <a href="%s">%s</a>' % (TASBIH[l], esc(GUIDES[l]['tc']))) if fk == 'dhikr' and l in TASBIH and l in GUIDES else ''
    body += '<aside class="appbox"><span class="kicker" style="color:%s">%s</span><h2><a href="%s">%s</a></h2><p>%s%s</p></aside>' % (
        CAT_COL[cat], esc(au['in_app']), fhref, esc(bt), esc(bp), extra)
    others = [(s2, x) for s2, x in LART[l].items() if s2 != es][:3]
    rel = ('<section class="arel"><h2>%s</h2><div class="posts">%s</div></section>' % (esc(u['reltitle']), ''.join(
        '<a class="post" href="%s"><div class="post-txt"><span class="kicker" style="color:%s">%s</span><h2>%s</h2><p>%s</p></div></a>' % (
            ART_ALTS[s2][l], CAT_COL[POST_META[s2][0]], esc(cats[POST_META[s2][0]]), esc(x['h1']), esc(x['desc'])) for s2, x in others))) if others else ''
    n = list(LART[l]).index(es) + 1
    apple, play = APPLE % ('web-art-%s-%d' % (l, n)), PLAY % ('article_%s_%d' % (l, n))
    cta = '<section class="acta" id="download"><div class="cta"><h2>%s</h2><p>%s</p>%s</div></section>' % (esc(au['cta_h']), esc(au['cta_p']), store_btns(l, apple, play, light=True))
    alts = ART_ALTS[es]
    tags = ['<meta name="description" content="%s">' % att(a['desc']), '<link rel="canonical" href="%s">' % canon]
    tags += ['<link rel="alternate" hreflang="%s" href="%s%s">' % (x, SITE, alts[x]) for x in LANGS if x in alts]
    tags += (['<link rel="alternate" hreflang="x-default" href="%s%s">' % (SITE, alts['en'])] if 'en' in alts else []) + [
             '<meta property="og:title" content="%s">' % att(a['h1']), '<meta property="og:description" content="%s">' % att(a['desc']),
             '<meta property="og:url" content="%s">' % canon, '<meta property="og:image" content="%s/img/v1/%s.webp">' % (SITE, im),
             '<meta property="og:type" content="article">', '<meta property="og:site_name" content="Lunora">', '<meta property="og:locale" content="%s">' % OGLOC[l],
             '<meta name="twitter:card" content="summary_large_image">']
    art_ld = json.dumps({'@context': 'https://schema.org', '@type': 'Article', 'headline': a['h1'], 'description': a['desc'], 'inLanguage': l,
                         'datePublished': a['date'], 'dateModified': a['date'], 'mainEntityOfPage': canon, 'image': '%s/img/v1/%s.webp' % (SITE, im),
                         'author': {'@type': 'Organization', 'name': 'Lunora', 'url': SITE + '/'},
                         'publisher': {'@type': 'Organization', 'name': 'Lunora', 'logo': {'@type': 'ImageObject', 'url': SITE + '/icon-192.png'}}}, ensure_ascii=False, indent=1)
    crumb_ld = json.dumps({'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': 1, 'name': u['home'], 'item': SITE + HOME[l]},
        {'@type': 'ListItem', 'position': 2, 'name': u['blogLead'], 'item': SITE + BLOG_PATHS[l]},
        {'@type': 'ListItem', 'position': 3, 'name': a['h1'], 'item': canon}]}, ensure_ascii=False)
    jl = [art_ld, crumb_ld] + ([faq_jsonld([{'q': esc(q), 'a': x} for q, x in faq])] if faq else [])
    hh = head(l, a['title'], tags, jl)
    return write(path, page(l, hh, hero + body + rel + cta, 'blog', alts))

def blog_page_l(l):
    bx = BLOGX[l]; u = UI[l]; posts = ''
    for es, a in LART[l].items():
        cat, im = POST_META[es]
        posts += ('<a class="post" href="%s" data-cat="%s"><div class="post-img"><img src="%s" alt="" loading="lazy"></div><div class="post-txt">'
                  '<span class="kicker" style="color:%s">%s</span><h2>%s</h2><p>%s</p><span class="meta"><time datetime="%s">%s</time> · %s %s %s</span></div></a>') % (
            ART_ALTS[es][l], cat, img(im), CAT_COL[cat], esc(dict(bx['cats'])[cat]), esc(a['h1']), esc(a['desc']), a['date'], esc(a['date_label']), a['minutes'], esc(u['minread']), ic('arrow-right-bold'))
    used = {POST_META[es][0] for es in LART[l]}
    chips = ''.join('<button type="button" data-cat="%s" aria-pressed="%s">%s</button>' % (c, 'true' if c == 'all' else 'false', esc(n)) for c, n in bx['cats'] if c == 'all' or c in used)
    hero = ('<section class="bhero"><img class="bg" src="%s" alt=""><div class="bhero-wash"></div><div class="wrap"><span class="pill">%s</span>'
            '<h1>%s <em>%s</em></h1><p class="lead">%s</p></div></section>') % (img('guven-bg'), esc(bx['tag']), esc(bx['h1a']), esc(bx['h1b']), esc(bx['lead']))
    lst = '<section class="sec"><div class="wrap"><h2 class="sr">%s</h2><div class="filters" role="group">%s</div><div class="posts">%s</div></div></section>' % (esc(bx['title']), chips, posts)
    cta = '<section class="sec" id="download" style="padding-top:0"><div class="wrap"><div class="cta"><h2>%s <em>%s</em></h2><p>%s</p>%s</div></div></section>' % (
        esc(bx['cta'][0]), esc(bx['cta'][1]), esc(bx['ctaP']), store_btns(l, APPLE % ('web-blog-%s-2' % l), PLAY % ('blog_%s' % l), light=True))
    canon = SITE + BLOG_PATHS[l]
    alts = {x: p for x, p in BLOG_PATHS.items()}
    tags = ['<meta name="description" content="%s">' % att(bx['desc']), '<link rel="canonical" href="%s">' % canon]
    tags += ['<link rel="alternate" hreflang="%s" href="%s%s">' % (x, SITE, alts[x]) for x in LANGS if x in alts]
    tags += ['<link rel="alternate" hreflang="x-default" href="%s/blog.html">' % SITE,
             '<meta property="og:title" content="%s">' % att(bx['title']), '<meta property="og:description" content="%s">' % att(bx['desc']),
             '<meta property="og:url" content="%s">' % canon, '<meta property="og:image" content="%s/icon-192.png">' % SITE,
             '<meta property="og:type" content="website">', '<meta property="og:site_name" content="Lunora">', '<meta property="og:locale" content="%s">' % OGLOC[l]]
    hh = head(l, bx['title'], tags, [])
    return write(BLOG_PATHS[l], page(l, hh, hero + lst + cta, 'blog', alts))

load_overlays()

# ---------------------------------------------------------------- llms.txt (28 Nov)
# Plain-text map of the site for AI assistants and agents (llmstxt.org format).
# Facts only, as the English pages state them; regenerated with every build.
def page_title(path):
    f = os.path.join(ROOT, path.lstrip('/') + ('index.html' if path.endswith('/') else ''))
    m = re.search(r'<title>(.*?)</title>', open(f).read())
    return re.sub(r' (?:[—|-] Lunora(?: Blog)?|Blog)$', '', H.unescape(m.group(1)).replace(' | Lunora', '')).strip() if m else path

def llms_txt():
    L = ['# Lunora', '',
         '> Lunora is an Islamic app for Muslim women on iPhone and Android: prayer times, the whole Quran, duas and dhikr with widgets, '
         'and Period Mode, which follows the cycle alongside worship with the views of the four madhhabs (Hanafi, Shafi\'i, Maliki, Hanbali). '
         'No ads. 9 languages. Lunora+ subscription with a 7-day free trial.', '',
         '- Publisher: Studio Lunora. Website: https://mylunora.app/',
         '- App Store: https://apps.apple.com/app/id6758765933',
         '- Google Play: https://play.google.com/store/apps/details?id=com.studiolunora.lunora',
         '- Languages (app and site): ' + ', '.join('%s (%s)' % (LNAME[l], l) for l in LANGS),
         '- Rating: ' + RATING['en'],
         '- Religious content presents scholarly views with sources; the app and site do not issue rulings.',
         '- Free web tool: an online tasbih (dhikr) counter, in every language below.', '']
    L += ['## Main pages (English)', '']
    for path in ['/', FEAT_PATHS['period']['en'], FEAT_PATHS['protect']['en'], FEAT_PATHS['quran']['en'], FEAT_PATHS['dhikr']['en'], TASBIH['en'], '/blog.html', '/support.html', '/privacy.html']:
        L.append('- [%s](%s%s)' % (page_title(path), SITE, path))
    L += ['', '## Guides (English)', '']
    for s in POST_META:
        if s in TOPICS: continue
        L.append('- [%s](%s/%s.html)' % (page_title('/%s.html' % s), SITE, s))
    for l in LANGS:
        if l == 'en': continue
        L += ['', '## %s (%s)' % (LNAME[l], l), '']
        paths = [HOME[l]] + [FEAT_PATHS[k][l] for k in FEAT_PATHS if l in FEAT_PATHS[k]]
        if l in TASBIH: paths.append(TASBIH[l])
        if l in BLOG_PATHS: paths.append(BLOG_PATHS[l])
        paths += [ART_ALTS[es][l] for es in LART.get(l, {})]
        L += ['- [%s](%s%s)' % (page_title(p), SITE, p) for p in paths]
    L += ['', '## Optional', '', '- [Sitemap with language alternates](%s/sitemap.xml)' % SITE, '- [Terms](%s/terms.html)' % SITE, '']
    full = os.path.join(ROOT, 'llms.txt'); open(full, 'w').write('\n'.join(L))
    return '/llms.txt'

# ---------------------------------------------------------------- sitemap
def sitemap(today):
    urls = []
    def add(loc, alts):
        x = '  <url>\n    <loc>%s%s</loc>\n    <lastmod>%s</lastmod>\n' % (SITE, loc, today)
        if len(alts) > 1:
            for k in LANGS:
                if k in alts: x += '    <xhtml:link rel="alternate" hreflang="%s" href="%s%s"/>\n' % (k, SITE, alts[k])
            if 'en' in alts: x += '    <xhtml:link rel="alternate" hreflang="x-default" href="%s%s"/>\n' % (SITE, alts['en'])
        urls.append(x + '  </url>\n')
    for l in LANGS: add(HOME[l], HOME)
    for k, alts in FEAT_PATHS.items():
        for l in alts: add(alts[l], alts)
    for l in TASBIH: add(TASBIH[l], TASBIH)
    for l in BLOG_PATHS: add(BLOG_PATHS[l], BLOG_PATHS)
    for s in POST_META:
        alts = ART_ALTS.get(s, {'en': '/%s.html' % s})
        for l in alts: add(alts[l], alts)
    for extra in ['/support.html', '/privacy.html', '/terms.html']: add(extra, {'en': extra})
    s = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n%s</urlset>\n' % ''.join(urls)
    return write('/sitemap.xml', s)

if __name__ == '__main__':
    import datetime
    out = [home_page(l) for l in LANGS]
    out += [feature_page(k, l) for k in FEAT_PATHS for l in FEAT_PATHS[k]]
    out += [blog_page_l(l) if l in BLOGX else blog_page(l) for l in BLOG_PATHS]
    out += [article_page(s) for s in POST_META if s not in TOPICS]
    out += [article_page_l(es, l) for l in LART for es in LART[l]]
    out += [tasbih_page(l) for l in TASBIH]
    # privacy.html is kept by hand since 26 Nov (2.0.9 policy); live.json holds the old text.
    out += [simple_page(k) for k in ['support', 'terms']]
    out += [retired_page(s, r['to']) for s, r in LIVE.get('retired', {}).items()]
    out.append(sitemap(datetime.date.today().isoformat()))
    out.append(llms_txt())
    print(len(out), 'files'); print('\n'.join(out))
