# -*- coding: utf-8 -*-
"""One-off content edit, 28 Nov 2026 (SEO pass). Run once:  python3 _build/edit_28kas_seo.py
1. Merge can-muslim-women-pray-during-period into what-to-do-during-period-in-islam
   (Google indexed the second, crawled-not-indexed the first; same topic).
2. Remove "first/only Islamic app" claims (25 Oct rule).
3. Point every link to the merged article at the kept one.
Writes _build/content/live.json in place."""
import os, json, re

B = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(B, 'content', 'live.json')
L = json.load(open(P))
A = L['articles']
OLD, NEW = 'can-muslim-women-pray-during-period', 'what-to-do-during-period-in-islam'

# ------------------------------------------------------------- 1. merge
src, dst = A[OLD]['body'], A[NEW]['body']

def cut(body, start_heading, end_heading):
    """Slice body from the tag that opens start_heading to the tag that opens end_heading."""
    i = body.index(start_heading); i = body.rindex('<h', 0, i)
    j = body.index(end_heading, i); j = body.rindex('<h', 0, j)
    return body[i:j]

short = cut(src, 'Can Muslim women pray during their period? The short answer', 'Why are Muslim women exempt')
short = re.sub(r'\s*<p><strong>Want to stay spiritually connected.*?</p>', '', short, flags=re.S)  # inline store promo
why = cut(src, 'Why are Muslim women exempt', "It's an exemption, not a punishment")
madhab = cut(src, 'What scholars say: different madhab positions', 'Dealing with guilt')
guilt = cut(src, 'Dealing with guilt', 'Special situations')
guilt = re.sub(r'\s*<p>Fatima, a new Muslim in Malaysia.*?</p>', '', guilt, flags=re.S)   # unsourced anecdote
guilt = guilt.replace('like the daily routine above', 'like the 7-day routine above')
istihadah = cut(src, 'Irregular bleeding (istihadah)', 'How Lunora supports')

# Madhab table: state the main positions plainly; reading from a screen follows the
# same recitation ruling, only the touching question changes.
madhab = re.sub(r'(<td><strong>Shafi\'i</strong></td>\s*<td>).*?(</td>)',
                r"\1Recitation is not permitted in the relied-upon position; reading verses as dhikr or dua, and looking at the text without reciting, is allowed\2", madhab, flags=re.S)
madhab = re.sub(r'<p><strong>The contemporary consensus</strong>.*?</p>',
                "<p><strong>What about a Quran app?</strong> A screen is not a <em>mushaf</em>, so the question of touching falls away for many scholars. Reciting aloud still follows your madhab's position above; listening and reading for meaning are open to everyone.</p>",
                madhab, flags=re.S)
madhab = madhab.replace('especially through digital means and listening', 'especially through listening, reflection and, in the Maliki school, recitation')

i_under = dst.index('<h2>Understanding menstruation in Islam')
i_special = dst.index('<h2>Special situations</h2>')
i_ghusl = dst.index('<h2>How to perform ghusl')
intro = dst[:i_under].replace(
    "This guide is different. Instead of focusing on restrictions, we'll answer the real question:",
    "This guide is different. We'll start with the short answer to <strong>whether Muslim women can pray during their period</strong>, then move to the real question:")
body = (intro + short + why + dst[i_under:i_special] + madhab + guilt
        + dst[i_special:i_ghusl].rstrip() + '\n\n    ' + istihadah.strip() + '\n\n    ' + dst[i_ghusl:])

phone_q = ('<div class="faq-item">\n            <h3>Can I read Quran on my phone during my period?</h3>\n'
           '            <p>A phone is not a <em>mushaf</em>, so many scholars do not apply the touching restriction to it. Whether you may recite aloud follows your madhab: the Maliki school allows it, while the Hanafi, Shafi\'i and Hanbali schools ask you to listen or read for meaning instead.</p>\n        </div>\n\n        ')
k = body.index('<h3>Do I need to make up missed prayers after my period?</h3>')
k = body.rindex('<div class="faq-item">', 0, k)
body = body[:k] + phone_q + body[k:]
A[NEW]['body'] = body

TITLE = 'Can Muslim Women Pray on Their Period? What to Do Instead'
DESC = 'Can Muslim women pray during their period? The short answer, why the exemption is a mercy, what the four madhhabs say, and what you can do instead.'
A[NEW]['h1'] = TITLE
A[NEW]['meta'] = 'Updated November 28, 2026 &middot; 18 min read'
tags = []
for t in A[NEW]['head']['tags']:
    t = re.sub(r'(name="description" content=")[^"]*', r'\g<1>' + DESC, t)
    t = re.sub(r'(property="og:description" content=")[^"]*', r'\g<1>' + DESC, t)
    t = re.sub(r'(name="twitter:description" content=")[^"]*', r'\g<1>' + DESC, t)
    t = re.sub(r'(property="og:title" content=")[^"]*', r'\g<1>' + TITLE, t)
    t = re.sub(r'(name="twitter:title" content=")[^"]*', r'\g<1>' + TITLE, t)
    t = re.sub(r'(name="keywords" content=")[^"]*', r'\g<1>can muslim women pray during period, can you pray on your period, what to do during period in islam, menstruation in islam, quran during period', t)
    tags.append(t)
A[NEW]['head']['tags'] = tags
A[NEW]['head']['title'] = TITLE + ' | Lunora'

jl = []
for j in A[NEW]['head']['jsonld']:
    o = json.loads(j)
    if o.get('@type') == 'Article':
        o['headline'] = TITLE; o['description'] = DESC; o['dateModified'] = '2026-11-28'
    if o.get('@type') == 'FAQPage':
        ents = o['mainEntity']
        idx = next(n for n, e in enumerate(ents) if e['name'].startswith('Do I need to make up'))
        ents.insert(idx, {'@type': 'Question', 'name': 'Can I read Quran on my phone during my period?',
                          'acceptedAnswer': {'@type': 'Answer', 'text': re.sub('<[^>]+>', '', phone_q.split('<p>')[1].split('</p>')[0])}})
    jl.append(json.dumps(o, ensure_ascii=False, indent=2))
A[NEW]['head']['jsonld'] = jl

# ------------------------------------------------------------- 2. claims
CLAIMS = [
    ("Period Mode</strong> is Lunora's signature feature, and it's the first of its kind in any Islamic app.", "Period Mode</strong> is Lunora's signature feature."),
    ("It's the first feature of its kind in any Islamic app: gentle spiritual guidance during menstruation", "It offers gentle spiritual guidance during menstruation"),
    (" It's the first feature of its kind in any Islamic app.</p>", "</p>"),
    ("created Period Mode, the first feature of its kind in any Islamic app.", "created Period Mode."),
    ("It's the first feature of its kind in any Islamic app: gentle spiritual guidance, adapted content", "It brings gentle spiritual guidance, adapted content"),
    ("It's the only Islamic app that understands what it means to be a Muslim woman through", "It is designed around what it means to be a Muslim woman through"),
    ("but it's the only Islamic app designed exclusively for Muslim women.", "and it's designed for Muslim women."),
    ("it's the first Islamic app designed to understand the full experience", "it's designed to understand the full experience"),
    ("is the first Islamic app designed specifically for Muslim women", "is an Islamic app designed specifically for Muslim women"),
]
for slug, d in A.items():
    for a, b in CLAIMS:
        d['body'] = d['body'].replace(a, b)

# ------------------------------------------------------------- 3. links
def repoint(x):
    if isinstance(x, str): return x.replace(OLD + '.html', NEW + '.html')
    if isinstance(x, list): return [repoint(v) for v in x]
    if isinstance(x, dict): return {k: repoint(v) for k, v in x.items()}
    return x
keep_old = A.pop(OLD)
L = repoint(L)
L['articles'][NEW]['related'] = [r for r in L['articles'][NEW]['related'] if NEW not in r['href']]
for slug, d in L['articles'].items():   # one related card per target
    seen, rel = set(), []
    for r in d['related']:
        if r['href'] not in seen: seen.add(r['href']); rel.append(r)
    d['related'] = rel
for l in L['blog']:
    seen, posts = set(), []
    for p in L['blog'][l]['posts']:
        if p['href'] not in seen: seen.add(p['href']); posts.append(p)
    L['blog'][l]['posts'] = posts
L['retired'] = {OLD: {'to': '/' + NEW + '.html', 'title': keep_old['head']['title']}}

left = json.dumps(L, ensure_ascii=False)
for a, _ in CLAIMS: assert a not in left, a
assert 'only Islamic app' not in left and 'first Islamic app' not in left
json.dump(L, open(P, 'w'), ensure_ascii=False, indent=1)
print('ok; merged body words:', len(re.sub('<[^>]+>', ' ', body).split()))
