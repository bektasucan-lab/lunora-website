# -*- coding: utf-8 -*-
"""Copy the handoff images into img/v1 as compressed webp. Run with a python that has Pillow."""
import os, sys
from PIL import Image
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, '_handoff/design_handoff_web/design/assets')
DST = os.path.join(ROOT, 'img/v1')
os.makedirs(DST, exist_ok=True)
JOBS = [  # (src, dst name, max width, quality)
    ('ads/bg-B-45.png', 'bg-b-45', 1100, 72), ('ads/bg-A-45.png', 'bg-a-45', 900, 72), ('ads/bg-C-45.png', 'bg-c-45', 900, 72),
    ('ads/bg-A-wide.png', 'bg-a-wide', 1344, 72), ('ads/bg-B-wide.png', 'bg-b-wide', 1344, 72), ('ads/bg-C-wide.png', 'bg-c-wide', 1344, 72),
    ('ads/ring-A.png', 'ring-a', 800, 82),
    ('sakura.png', 'sakura', 160, 85), ('support-heart-green.png', 'heart', 200, 85), ('onb/app-icon.png', 'app-icon', 96, 90),
    ('kutup/kehf.jpg', 'kehf', 900, 70), ('kutup/hacer.jpg', 'hacer', 420, 78), ('kutup/hatice.jpg', 'hatice', 420, 78), ('kutup/rahman.jpg', 'rahman', 420, 78),
    ('store/guven-bg.jpg', 'guven-bg', 860, 70), ('wc/tesbih-bg-l2.jpg', 'tesbih-bg', 720, 76), ('wc/tesbih-bg-wide.jpg', 'tesbih-bg-wide', 720, 76),
    ('wc/ogr/namaz-bg.jpg', 'namaz-bg', 960, 74), ('wc/ogr/kurs-bg.jpg', 'kurs-bg', 960, 74), ('zikir/kapak-tesbih.jpg', 'kapak-tesbih', 480, 76),
    ('donem3/empty-invite.jpg', 'empty-invite', 560, 76), ('donem3/empty-waiting.jpg', 'empty-waiting', 560, 76), 
]
ICONS = {'wc/67b7cfdb.png': 'lock', 'wc/8be74634.png': 'tasbih', 'wc/f4b430fe.png': 'rahle', 'wc/hab/19736ec3.png': 'tree', 'wc/hab/4eb467c8.png': 'dates',
         'wc/hab/52d3e3d2.png': 'rug', 'wc/hab/5d56e719.png': 'books', 'wc/hab/c32795cf.png': 'lantern', 'wc/hab/d50c0479.png': 'pillow', 'wc/hab/ea56fbff.png': 'pen',
         'wc/plan/cuma.png': 'mosque', 'wc/plan/hatim365.png': 'quran-stand', 'wc/plan/huzur.png': 'lotus', 'wc/plan/yedi.png': 'book-pink'}
for k, v in ICONS.items(): JOBS.append((k, 'ic-' + v, 240, 82))

def conv(src, name, w, q):
    im = Image.open(os.path.join(SRC, src))
    im = im.convert('RGBA') if im.mode in ('RGBA', 'LA', 'P') else im.convert('RGB')
    if im.width > w: im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    out = os.path.join(DST, name + '.webp'); im.save(out, 'WEBP', quality=q, method=6)
    return out, im.size

if __name__ == '__main__':
    tot = 0
    for j in JOBS:
        out, sz = conv(*j); n = os.path.getsize(out); tot += n
    # favicon-style png for nav (crisp)
    print('files', len(JOBS), 'total KB', tot // 1024)
