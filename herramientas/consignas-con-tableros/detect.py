# Encuentra los tableros dibujados en una captura del GobstonesWeb.
#
# El GobstonesWeb dibuja el tablero adentro de un marco gris (221,221,221) con los números
# de fila y columna. Cada marco es una componente conexa grande de ese gris; la grilla es
# lo de adentro, descontando el grosor del marco de cada lado (la mediana de las corridas
# de gris desde el borde, que no se deja engañar por los números).
#
# Uso: python3 detect.py <cursos> <exercises.json> <out.json>
import json
import sys

import numpy as np
from PIL import Image
from scipy import ndimage

cursos, exercises_path, out_path = sys.argv[1:4]
exercises = json.load(open(exercises_path))['exercises']

FRAME = np.array([221, 221, 221])


def frame_mask(im):
    return (np.abs(im.astype(int) - FRAME).max(axis=2) <= 6)


def run_from(line):
    """Cuántos píxeles de marco seguidos hay desde el principio de una línea."""
    if not line[0]:
        # Un borde antialiaseado de uno o dos píxeles antes del gris.
        k = 0
        while k < min(3, len(line)) and not line[k]:
            k += 1
        if k >= len(line) or not line[k]:
            return 0
        line = line[k:]
        start = k
    else:
        start = 0
    n = np.argmin(line) if not line.all() else len(line)
    return start + n


def longest_run(flags):
    """El tramo más largo de `True` seguidos: (desde, hasta)."""
    best, cur = (0, 0), None
    for i, f in enumerate(list(flags) + [False]):
        if f and cur is None:
            cur = i
        elif not f and cur is not None:
            if i - cur > best[1] - best[0]:
                best = (cur, i)
            cur = None
    return best


def thick(flags, thin=3):
    """Los tramos de `True` de más de `thin` elementos; los finitos pasan a `False`."""
    out = np.array(flags, dtype=bool)
    i = 0
    while i < len(out):
        if out[i]:
            j = i
            while j < len(out) and out[j]:
                j += 1
            if j - i <= thin:
                out[i:j] = False
            i = j
        else:
            i += 1
    return out


def panels(im):
    raw = frame_mask(im)
    # Se cierran los huecos finitos: una columna antialiaseada parte el marco en dos.
    mask = ndimage.binary_closing(raw, structure=np.ones((3, 3)), border_value=1)
    labels, count = ndimage.label(mask, structure=np.ones((3, 3)))
    found = []
    for index, sl in enumerate(ndimage.find_objects(labels), start=1):
        y0, y1, x0, x1 = sl[0].start, sl[0].stop, sl[1].start, sl[1].stop
        bw, bh = x1 - x0, y1 - y0
        if bw < 30 or bh < 25:
            continue
        sub = labels[y0:y1, x0:x1] == index
        filled = sub.sum() / (bw * bh)
        if filled > 0.9 or filled < 0.03:
            continue
        # Las filas del marco son casi todas gris; las de la grilla, solo en los costados.
        rows = sub.mean(axis=1)
        cols = sub.mean(axis=0)
        # Las líneas de la grilla, en los tableros blancos, son del mismo gris que el marco:
        # se distinguen porque son finitas. Un tramo gris de hasta 3 píxeles es una línea.
        ry0, ry1 = longest_run(~thick(rows >= 0.5))
        rx0, rx1 = longest_run(~thick(cols >= 0.5))
        if rx1 - rx0 < 8 or ry1 - ry0 < 8:
            continue
        # Y adentro de ese rectángulo casi no tiene que haber marco.
        inner = sub[ry0:ry1, rx0:rx1].mean()
        if inner > 0.35:
            continue
        found.append({
            'frame': [int(x0), int(y0), int(x1), int(y1)],
            'grid': [int(x0 + rx0), int(y0 + ry0), int(x0 + rx1), int(y0 + ry1)],
            'gutters': [int(rx0), int(ry0), int(bw - rx1), int(bh - ry1)],
            'fill': round(float(filled), 3),
        })
    found.sort(key=lambda p: (p['frame'][1] // 20, p['frame'][0]))
    return found


result = {}
for ex_dir, ex in exercises.items():
    for image in ex['images']:
        im = np.array(Image.open(f'{cursos}/{image}').convert('RGB'))
        result[image] = {'exercise': ex_dir, 'size': [im.shape[1], im.shape[0]], 'panels': panels(im)}

json.dump(result, open(out_path, 'w'), indent=1)
counts = {}
for r in result.values():
    counts[len(r['panels'])] = counts.get(len(r['panels']), 0) + 1
print('panels per image', dict(sorted(counts.items())))
