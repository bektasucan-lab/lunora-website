# -*- coding: utf-8 -*-
"""Emulator captures (_handoff/shots/<lang>/<key>.png) -> img/v1/app/<lang>-<key>.webp (390 wide)."""
import os, glob
from PIL import Image
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for f in sorted(glob.glob(os.path.join(ROOT, '_handoff/shots/*/*.png'))):
    lang = os.path.basename(os.path.dirname(f)); key = os.path.basename(f)[:-4]
    im = Image.open(f).convert('RGB'); w = 390
    if key == 'A2': im = im.crop((0, 112, im.width, im.height))  # Period Mode opens as a sheet: drop the dimmed strip above it
    im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    out = os.path.join(ROOT, 'img/v1/app/%s-%s.webp' % (lang, key)); im.save(out, 'WEBP', quality=80, method=6)
    print(lang, key, im.size, os.path.getsize(out) // 1024, 'KB')
