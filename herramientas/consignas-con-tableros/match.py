# Compara cada tablero de cada captura con los tableros del ejercicio dibujados por el IDE.
#
#   python3 match.py plan  <exercises.json> <detect.json> <requests.json>
#   python3 match.py score <cursos> <exercises.json> <detect.json> <renders> <out.json>
#
# La medida: cada celda se recorta un 15% de cada lado —para no comparar ni las líneas de
# la grilla ni el borde del cabezal, que los dos renderers dibujan distinto— y se reduce a
# 4×4 píxeles en color. La distancia de una celda es la diferencia media por canal (0-255);
# la de un tablero, la media de sus celdas, y además se cuenta cuántas celdas difieren
# mucho. Es una medida perceptual gruesa a propósito: los dos renderers no dibujan igual
# una bolita, pero sí la ponen en el mismo cuadrante y del mismo color, y una vestimenta
# usa las mismas imágenes.
import hashlib
import json
import sys

import numpy as np
from PIL import Image
from scipy import ndimage

PAD = 8
INSET = 0.15
GRID = 4
ASPECT_TOLERANCE = 0.12


def guided_grid(panel, W, H):
    """La grilla deducida del marco y del tamaño del candidato, cuando la detectada no cierra.

    El GobstonesWeb deja el mismo margen para los números arriba, abajo y a los costados:
    con el marco de Fw×Fh y un tablero de W×H, Fw = W·c + 2g y Fh = H·c + 2g.
    """
    x0, y0, x1, y1 = panel['frame']
    Fw, Fh = x1 - x0, y1 - y0
    if W != H:
        c = (Fw - Fh) / (W - H)
        g = (Fw - W * c) / 2
    else:
        g = (panel['gutters'][1] + panel['gutters'][3]) / 2
        c = (Fw - 2 * g) / W
        if abs((Fh - 2 * g) / H - c) > 0.1 * c:
            return None
    if c < 8 or not (0.1 * c <= g <= 1.0 * c):
        return None
    return [round(x0 + g), round(y0 + g), round(x1 - g), round(y1 - g)]


def candidates(ex, panel):
    """Los tableros del ejercicio que pueden ser el de la captura, con su grilla y su celda."""
    for index, entry in enumerate(ex['boards']):
        board = entry['board']
        W, H = board['width'], board['height']
        grid = panel['grid']
        cw, ch = (grid[2] - grid[0]) / W, (grid[3] - grid[1]) / H
        if cw < 5 or ch < 5 or abs(cw / ch - 1) > ASPECT_TOLERANCE:
            grid = guided_grid(panel, W, H)
            if grid is None:
                continue
            cw, ch = (grid[2] - grid[0]) / W, (grid[3] - grid[1]) / H
        cell = max(6, round((cw + ch) / 2))
        modes = ['none'] + (['attire'] if ex.get('attireDir') else [])
        for mode in modes:
            yield index, cell, mode, grid


def key_of(exercise, index, cell, mode):
    h = hashlib.sha1(exercise.encode()).hexdigest()[:10]
    return f'{h}-{index}-{cell}-{mode}'


def cell_features(img, x0, y0, cw, ch, cols, rows, inset=INSET):
    """Los rasgos de cada celda: una matriz rows×cols×(GRID·GRID·3). La fila 0 es la de arriba."""
    feats = np.zeros((rows, cols, GRID * GRID * 3))
    for r in range(rows):
        for c in range(cols):
            left = x0 + c * cw + inset * cw
            top = y0 + r * ch + inset * ch
            right = x0 + (c + 1) * cw - inset * cw
            bottom = y0 + (r + 1) * ch - inset * ch
            crop = img.crop((round(left), round(top), max(round(left) + 1, round(right)), max(round(top) + 1, round(bottom))))
            feats[r, c] = np.asarray(crop.resize((GRID, GRID), Image.BOX), dtype=float).reshape(-1)
    return feats


def presence(img, x0, y0, cw, ch, cols, rows):
    """Qué bolitas hay en cada cuadrante: rows×cols×4 cuadrantes×4 colores, en booleano.

    Es la parte de la medida que no depende de cómo se dibuja una bolita: los dos
    renderers ponen cada color en su cuadrante y con un color parecido.
    """
    a = np.asarray(img, dtype=int)
    out = np.zeros((rows, cols, 4, 4), dtype=bool)
    for r in range(rows):
        for c in range(cols):
            for q in range(4):
                qx, qy = q % 2, q // 2
                left = round(x0 + c * cw + qx * cw / 2 + 0.1 * cw)
                right = round(x0 + c * cw + (qx + 1) * cw / 2 - 0.1 * cw)
                top = round(y0 + r * ch + qy * ch / 2 + 0.1 * ch)
                bottom = round(y0 + r * ch + (qy + 1) * ch / 2 - 0.1 * ch)
                px = a[max(0, top):max(top + 1, bottom), max(0, left):max(left + 1, right)].reshape(-1, 3)
                if len(px) == 0:
                    continue
                R, G, B = px[:, 0], px[:, 1], px[:, 2]
                classes = [
                    (B > 150) & (R < 120) & (B - R > 80),
                    (np.maximum(np.maximum(R, G), B) < 70),
                    (R > 150) & (G < 90) & (B < 90),
                    (G > 120) & (R < 120) & (B < 120) & (G - R > 50),
                ]
                out[r, c, q] = [k.mean() > 0.06 for k in classes]
    return out


def head_in_shot(img, x0, y0, cw, ch, cols, rows):
    """Dónde está el cabezal en la captura, por el cuadrado rojo que le pone el GobstonesWeb.

    Se busca una componente roja con forma de anillo y del tamaño de una celda, y se toma
    la celda donde cae su centro: el cuadrado se dibuja un poco corrido de la grilla, y
    una vestimenta puede tener otras cosas rojas —puntitos de tomates, cartas—, pero no
    un anillo del tamaño de una celda. Devuelve (columna, fila) del tablero —la fila 0 es
    la de abajo— o nada si no lo encuentra.
    """
    a = np.asarray(img, dtype=int)
    red = (a[:, :, 0] >= 170) & (a[:, :, 1] <= 90) & (a[:, :, 2] <= 90)
    labels, count = ndimage.label(red, structure=np.ones((3, 3)))
    best = None
    for index, sl in enumerate(ndimage.find_objects(labels), start=1):
        h = sl[0].stop - sl[0].start
        w = sl[1].stop - sl[1].start
        if not (0.6 * cw <= w <= 1.6 * cw and 0.6 * ch <= h <= 1.6 * ch):
            continue
        fill = (labels[sl] == index).mean()
        if fill > 0.6:
            continue
        cx = (sl[1].start + sl[1].stop) / 2
        cy = (sl[0].start + sl[0].stop) / 2
        c = int((cx - x0) // cw)
        r = int((cy - y0) // ch)
        if 0 <= c < cols and 0 <= r < rows:
            if best is not None:
                return None  # dos anillos: no se sabe cuál es
            best = (c, rows - 1 - r)
    return best


def plan(exercises_path, detect_path, out_path):
    exercises = json.load(open(exercises_path))['exercises']
    detect = json.load(open(detect_path))
    requests = {}
    for image, d in detect.items():
        ex = exercises[d['exercise']]
        for panel in d['panels']:
            for index, cell, mode, _ in candidates(ex, panel):
                key = key_of(d['exercise'], index, cell, mode)
                requests[key] = {'key': key, 'exercise': d['exercise'], 'board': index, 'cell': cell, 'mode': mode}
    json.dump(list(requests.values()), open(out_path, 'w'))
    print('pedidos', len(requests))


def score(cursos, exercises_path, detect_path, renders, out_path):
    exercises = json.load(open(exercises_path))['exercises']
    detect = json.load(open(detect_path))
    out = {}
    for image, d in detect.items():
        ex = exercises[d['exercise']]
        shot = Image.open(f'{cursos}/{image}').convert('RGB')
        results = []
        for p, panel in enumerate(d['panels']):
            scored = []
            heads = {}
            for index, cell, mode, grid in candidates(ex, panel):
                gx0, gy0, gx1, gy1 = grid
                board = ex['boards'][index]['board']
                W, H = board['width'], board['height']
                render = Image.open(f'{renders}/{key_of(d["exercise"], index, cell, mode)}.png').convert('RGB')
                a = cell_features(shot, gx0, gy0, (gx1 - gx0) / W, (gy1 - gy0) / H, W, H)
                b = cell_features(render, PAD, PAD, cell, cell, W, H)
                per_cell = np.abs(a - b).mean(axis=2)
                # El pico: el peor píxel de 4×4 de cualquier celda, recortando menos. Es lo
                # que ve un objeto chico que está en una celda y no en la otra —el granjero
                # de una vestimenta sobre un fondo que ocupa toda la celda—.
                a8 = cell_features(shot, gx0, gy0, (gx1 - gx0) / W, (gy1 - gy0) / H, W, H, inset=0.08)
                b8 = cell_features(render, PAD, PAD, cell, cell, W, H, inset=0.08)
                peak = np.abs(a8 - b8).reshape(H, W, GRID * GRID, 3).mean(axis=3).max()
                pa = presence(shot, gx0, gy0, (gx1 - gx0) / W, (gy1 - gy0) / H, W, H)
                pb = presence(render, PAD, PAD, cell, cell, W, H)
                if (W, H, tuple(grid)) not in heads:
                    heads[(W, H, tuple(grid))] = head_in_shot(shot, gx0, gy0, (gx1 - gx0) / W, (gy1 - gy0) / H, W, H)
                seen_head = heads[(W, H, tuple(grid))]
                entry = ex['boards'][index]
                scored.append({
                    'index': index,
                    'board': entry['file'],
                    'from': entry.get('from'),
                    'solution': entry.get('solution'),
                    'stones': int((pa != pb).any(axis=3).sum()),
                    'peak': round(float(peak), 1),
                    'head': None if seen_head is None else seen_head == (board['head']['column'], board['head']['row']),
                    'mode': mode,
                    'cell': cell,
                    'size': [W, H],
                    'mean': round(float(per_cell.mean()), 2),
                    'worst': round(float(per_cell.max()), 2),
                    'bad': int((per_cell > 40).sum()),
                    'cells': W * H,
                    'grid': grid,
                    'guided': grid != panel['grid'],
                })
            scored.sort(key=lambda s: s['mean'])
            results.append({'panel': p, 'grid': panel['grid'], 'top': scored[:8]})
        out[image] = {'exercise': d['exercise'], 'size': d['size'], 'panels': results}
    json.dump(out, open(out_path, 'w'), indent=1)


if __name__ == '__main__':
    if sys.argv[1] == 'plan':
        plan(*sys.argv[2:5])
    else:
        score(*sys.argv[2:7])
