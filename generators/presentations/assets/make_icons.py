#!/usr/bin/env python3
"""Draws the resource-link icons used on slides (video, reading, exercise, simulation, web).
Plain flat glyphs on a round badge; "any icon for now" (Mark 2026-10-21), replaceable later.
Run: python3 -I generators/presentations/assets/make_icons.py"""
import os
from PIL import Image, ImageDraw
OUT = os.path.dirname(os.path.abspath(__file__))
S = 4  # supersample
N = 96 * S
BADGE = {"video": "1F6FB2", "reading": "2E8B57", "exercise": "B8571B", "simulation": "7B3FA0", "web": "455A64"}

def badge(color):
    im = Image.new("RGBA", (N, N), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.ellipse((2 * S, 2 * S, N - 2 * S, N - 2 * S), fill="#" + color)
    return im, d

def finish(im, name):
    im.resize((96, 96), Image.LANCZOS).save(os.path.join(OUT, f"icon_{name}.png"))

for name, col in BADGE.items():
    im, d = badge(col); c = N // 2; w = "white"
    if name == "video":     # play triangle
        d.polygon([(c - 14 * S, c - 20 * S), (c - 14 * S, c + 20 * S), (c + 22 * S, c)], fill=w)
    elif name == "reading": # open book
        d.polygon([(c - 26 * S, c - 16 * S), (c - 2 * S, c - 10 * S), (c - 2 * S, c + 22 * S), (c - 26 * S, c + 16 * S)], fill=w)
        d.polygon([(c + 26 * S, c - 16 * S), (c + 2 * S, c - 10 * S), (c + 2 * S, c + 22 * S), (c + 26 * S, c + 16 * S)], fill=w)
    elif name == "exercise": # pencil on page
        d.rectangle((c - 18 * S, c - 22 * S, c + 12 * S, c + 22 * S), fill=w)
        for i in range(4): d.line((c - 12 * S, c - 12 * S + i * 9 * S, c + 6 * S, c - 12 * S + i * 9 * S), fill="#" + col, width=3 * S)
    elif name == "simulation": # flask
        d.polygon([(c - 7 * S, c - 24 * S), (c + 7 * S, c - 24 * S), (c + 7 * S, c - 6 * S), (c + 24 * S, c + 22 * S), (c - 24 * S, c + 22 * S), (c - 7 * S, c - 6 * S)], fill=w)
    else:                   # globe-ish link
        d.ellipse((c - 22 * S, c - 22 * S, c + 22 * S, c + 22 * S), outline=w, width=4 * S)
        d.line((c - 22 * S, c, c + 22 * S, c), fill=w, width=3 * S); d.ellipse((c - 10 * S, c - 22 * S, c + 10 * S, c + 22 * S), outline=w, width=3 * S)
    finish(im, name)
print("icons written to", OUT)
