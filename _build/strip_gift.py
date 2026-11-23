# -*- coding: utf-8 -*-
"""Find the Lunora+ gift badge (pill + two sentences) in a capture; return the
row span to cut, or None. A member never sees it; the website shows members."""
from PIL import Image

def gift_span(im):
    im = im.convert('RGB'); W, H = im.size; px = im.load()
    def bg(y): return px[4, y]
    def empty(y, tol=4):
        b = bg(y)
        for x in range(0, W, 3):
            p = px[x, y]
            if abs(p[0]-b[0]) > tol or abs(p[1]-b[1]) > tol or abs(p[2]-b[2]) > tol: return False
        return True
    def gold(p): return p[0] > 170 and 120 < p[1] < 185 and p[2] < 120 and p[0] - p[2] > 90
    def outside_card(y):  # x≈W*0.06 is inside a card's edge; outside it is page bg
        b = bg(y); p = px[int(W*0.07), y]
        return sum(abs(p[i]-b[i]) for i in range(3)) < 12
    top = None
    for y in range(int(H*0.15), H):
        if not outside_card(y): continue
        if sum(1 for x in range(int(W*0.3), int(W*0.7), 2) if gold(px[x, y])) >= 6:
            top = y; break
    if top is None: return None
    while top > 0 and not empty(top - 1): top -= 1   # up to the pill's own edge
    y = top; run = 0
    while y < H:
        run = run + 1 if empty(y) else 0
        if run >= 30: break
        y += 1
    while y < H and empty(y): y += 1
    return (top, y)   # cut [top, y): content after starts where the badge did

def strip(im, key):
    s = gift_span(im)
    if not s: return im, None
    a, b = s; im = im.convert('RGB'); W, H = im.size
    if key == 'D': b = H   # what follows the badge is a section title cut by the screen edge: drop it too
    out = Image.new('RGB', (W, H), im.getpixel((4, H - 1)))
    out.paste(im.crop((0, 0, W, a)), (0, 0)); out.paste(im.crop((0, b, W, H)), (0, a))
    filled = a + (H - b)
    if key == 'C':
        # The lesson list runs past the screen edge: continue its card with a
        # blank row of the same card (white, with its edges) to the bottom.
        px = out.load(); row = None
        for y in range(filled - 1, a, -1):
            if all(px[x, y] == (255, 255, 255) for x in range(int(W * .12), int(W * .88), 4)):
                row = out.crop((0, y, W, y + 1)); break
        if row:
            for y in range(filled, H): out.paste(row, (0, y))
    return out, (a, b)
