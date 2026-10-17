# Mira de cerca un candidato: la diferencia celda por celda y las dos imágenes lado a lado.
# Uso: python3 inspect_match.py <cursos> <exercises.json> <detect.json> <renders> <imagen> <panel> <out.png> [n]
import json
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, sys.argv[0].rsplit('/', 1)[0])
from match import PAD, candidates, cell_features, key_of  # noqa: E402

cursos, exercises_path, detect_path, renders, image, panel_index, out = sys.argv[1:8]
n = int(sys.argv[8]) if len(sys.argv) > 8 else 3
exercises = json.load(open(exercises_path))['exercises']
detect = json.load(open(detect_path))
d = detect[image]
ex = exercises[d['exercise']]
panel = d['panels'][int(panel_index)]
shot = Image.open(f'{cursos}/{image}').convert('RGB')
gx0, gy0, gx1, gy1 = panel['grid']
rows = []
for index, cell, mode, grid in candidates(ex, panel):
    gx0, gy0, gx1, gy1 = grid
    board = ex['boards'][index]['board']
    W, H = board['width'], board['height']
    render = Image.open(f'{renders}/{key_of(d["exercise"], index, cell, mode)}.png').convert('RGB')
    a = cell_features(shot, gx0, gy0, (gx1 - gx0) / W, (gy1 - gy0) / H, W, H)
    b = cell_features(render, PAD, PAD, cell, cell, W, H)
    per = np.abs(a - b).mean(axis=2)
    rows.append((per.mean(), ex['boards'][index]['file'], mode, per, render.crop((PAD, PAD, PAD + W * cell, PAD + H * cell))))
rows.sort(key=lambda r: r[0])
crop = shot.crop((gx0, gy0, gx1, gy1))
tiles = [crop] + [r[4] for r in rows[:n]]
w = sum(t.width for t in tiles) + 10 * len(tiles)
h = max(t.height for t in tiles)
sheet = Image.new('RGB', (w, h), 'white')
x = 0
for t in tiles:
    sheet.paste(t, (x, 0))
    x += t.width + 10
sheet.save(out)
np.set_printoptions(precision=0, suppress=True, linewidth=200)
for r in rows[:n]:
    print(round(r[0], 2), r[1], r[2])
    print(r[3])
