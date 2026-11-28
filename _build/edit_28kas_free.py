# -*- coding: utf-8 -*-
"""One-off content edit, 28 Nov 2026: no "free" claims about the app (it has a paywall;
"7-day free trial" is right). The free web tasbih counter is untouched. Run once:
python3 _build/edit_28kas_free.py   (writes _build/content/live.json in place)"""
import os, json, re
B = os.path.dirname(os.path.abspath(__file__)); P = os.path.join(B, 'content', 'live.json')
s = json.dumps(json.load(open(P)), ensure_ascii=False)
R = [
    (". Free to download on iPhone and Android.", ". On iPhone and Android, with a 7-day free trial."),
    ("Free to download on iPhone and Android, with no ads.", "On iPhone and Android, with no ads and a 7-day free trial."),
    ("an Islamic app for Muslim women, free to download on iPhone and Android", "an Islamic app for Muslim women on iPhone and Android"),
    ("Lunora is free to download on iPhone and Android and has no ads", "Lunora has no ads"),
    ("Lunora is free to download from the App Store and Google Play and has no ads", "Lunora has no ads"),
    ("Lunora is free to download on iPhone and Android", "Lunora is available on iPhone and Android"),
    ("Lunora is free to download and has no ads", "Lunora has no ads"),
    ("; in countries where Lunora+ can't be purchased, the app is free to use", ""),
    ("into one app, free on iPhone and Android", "into one app, on iPhone and Android"),
    ("An Islamic app for Muslim women, free on iPhone and Android", "An Islamic app for Muslim women on iPhone and Android"),
    ("Lunora is an Islamic app for Muslim women, free on iPhone and Android", "Lunora is an Islamic app for Muslim women on iPhone and Android"),
    ("Download Lunora free on the App Store", "Download Lunora on the App Store"),
    ("download Lunora free on the App Store", "download Lunora on the App Store"),
    ("Download Lunora free", "Download Lunora"),
    ("And it's completely free", "And it has no ads"),
    ("And it's free, with no ads", "And it has no ads"),
    ("and a free reading tracker", "and a reading tracker"),
    ("The first guide designed for your whole reality", "A guide designed for your whole reality"),
    ("and the only Period Mode in any Islamic app", "and Period Mode"),
]
for a, b in R:
    n = s.count(a); assert n, a
    s = s.replace(a, b); print(n, a[:60])
L = json.loads(s)
json.dump(L, open(P, 'w'), ensure_ascii=False, indent=1)
left = re.findall(r'.{40}(?:free to download|Free to download|free on iPhone|Lunora free|first guide).{20}', s)
print('left:', left)
