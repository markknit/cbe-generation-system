#!/usr/bin/env python3
"""Fetches the colourful icons used on slides from Google's Noto Color Emoji (Apache-2.0,
https://github.com/googlefonts/noto-emoji). The downloaded PNGs are committed (small), so builds are
offline; this script only documents and reproduces where they came from.
Run: python3 -I generators/presentations/assets/fetch_icons.py"""
import json, os, urllib.request, sys
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "emoji")
BASE = "https://raw.githubusercontent.com/googlefonts/noto-emoji/main/2D/png/128/emoji_u{cp}.png"
# name -> code point(s) (lower-case hex, joined by '_'). Names are what the authoring step may use.
CATALOGUE = {
  # thinking / classroom routine
  "lightbulb": "1f4a1", "thinking": "1f914", "question": "2753", "eyes": "1f440", "magnifier": "1f50d", "speech": "1f4ac",
  "thought": "1f4ad", "pencil": "270f", "memo": "1f4dd", "clipboard": "1f4cb", "pushpin": "1f4cc", "star": "2b50",
  "check": "2705", "cross": "274c", "warning": "26a0", "raised_hand": "1f64b", "hands_together": "1f64f", "handshake": "1f91d",
  "teacher": "1f9d1_200d_1f3eb", "student": "1f9d1_200d_1f393", "people": "1f465", "puzzle": "1f9e9", "target": "1f3af",
  "stopwatch": "23f1", "hourglass": "231b", "books": "1f4da", "book": "1f4d6", "ruler": "1f4cf", "scissors": "2702",
  "palette": "1f3a8", "paintbrush": "1f58c", "camera": "1f4f7", "computer": "1f4bb", "video": "1f4f9", "link": "1f517",
  "globe_africa": "1f30d", "trophy": "1f3c6", "megaphone": "1f4e3", "ear": "1f442", "mouth": "1f444",
  # science kit / safety
  "microscope": "1f52c", "test_tube": "1f9ea", "flask": "2697", "petri": "1f9eb", "atom": "269b", "thermometer": "1f321",
  "goggles": "1f97d", "gloves": "1f9e4", "lab_coat": "1f97c", "magnet": "1f9f2", "battery": "1f50b", "scales": "2696",
  "fire": "1f525", "droplet": "1f4a7", "sun": "2600", "cloud": "2601", "snowflake": "2744", "lightning": "26a1",
  # living things
  "seedling": "1f331", "herb": "1f33f", "leaf": "1f343", "tree": "1f333", "potted_plant": "1fab4", "maize": "1f33d",
  "onion": "1f9c5", "tomato": "1f345", "carrot": "1f955", "banana": "1f34c", "apple": "1f34e", "mushroom": "1f344",
  "microbe": "1f9a0", "dna": "1f9ec", "egg": "1f95a", "baby": "1f476", "muscle": "1f4aa", "brain": "1f9e0", "heart": "2764",
  "lungs": "1fac1", "bone": "1f9b4", "tooth": "1f9b7", "bandage": "1fa79", "hand": "270b", "foot": "1f9b6",
  "cow": "1f404", "fish": "1f41f", "bird": "1f426", "butterfly": "1f98b", "bee": "1f41d", "ant": "1f41c", "frog": "1f438",
  # home / kitchen (Kenyan context: jiko, sufuria, ugali scenes)
  "house": "1f3e0", "door": "1f6aa", "stove_pot": "1f372", "pan": "1f958", "spoon": "1f944", "plate": "1f37d", "bread": "1f35e",
  "rice": "1f35a", "salt": "1f9c2", "bucket": "1faa3", "bottle": "1f9f4", "recipe_book": "1f4d6", "factory": "1f3ed", "hospital": "1f3e5", "school": "1f3eb",
  # shapes / arrows
  "arrow_right": "27a1", "arrow_down": "2b07", "arrow_up": "2b06", "arrows_cycle": "1f504", "red_circle": "1f534",
  "green_circle": "1f7e2", "blue_circle": "1f535", "yellow_circle": "1f7e1", "purple_circle": "1f7e3", "orange_circle": "1f7e0",
}
os.makedirs(OUT, exist_ok=True)
ok, bad = [], []
for name, cp in CATALOGUE.items():
    dest = os.path.join(OUT, name + ".png")
    if os.path.exists(dest): ok.append(name); continue
    try:
        data = urllib.request.urlopen(BASE.format(cp=cp), timeout=30).read()
        if not data.startswith(b"\x89PNG"): raise ValueError("not a PNG")
        open(dest, "wb").write(data); ok.append(name)
    except Exception as e:
        bad.append((name, cp, str(e)[:60]))
json.dump({k: v for k, v in CATALOGUE.items() if k in ok}, open(os.path.join(OUT, "catalogue.json"), "w"), indent=1)
open(os.path.join(OUT, "LICENSE-noto-emoji.txt"), "w").write("Icons: Noto Color Emoji by Google, licensed under the Apache License, Version 2.0 (https://www.apache.org/licenses/LICENSE-2.0). Source: https://github.com/googlefonts/noto-emoji\n")
print(f"{len(ok)} icons ok, {len(bad)} failed")
for b in bad: print("  FAILED", b)
