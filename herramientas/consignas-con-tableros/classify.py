# Decide, con los puntajes, qué captura se convierte sola y cuál no.
#
# Dos medidas, según cómo esté dibujado el tablero:
#
# - **Con vestimenta**, las imágenes son las mismas en los dos renderers, así que alcanza
#   la diferencia de color celda por celda: coincide si ninguna celda difiere más de
#   ATTIRE_WORST y la media no pasa de ATTIRE_MEAN. Una coincidencia verdadera da 1-5.
#   Además, el peor píxel (de 4×4 por celda) no pasa de ATTIRE_PEAK: es lo que ve un
#   objeto chico que está en una celda y no en la otra. Revisado a ojo: las verdaderas
#   llegan a 24, y las dos falsas que pasaban lo demás dan 28.
# - **Con bolitas**, los dos renderers no dibujan igual una bolita: una celda con cuatro
#   da hasta 26 de diferencia sin que cambie nada. Ahí manda qué colores hay en cada
#   cuadrante (`stones`, que tiene que dar cero) y la diferencia de color solo descarta lo
#   grueso —el cabezal en otra celda da más de 40—.
#
# Lo que la medida no ve: **cuántas** bolitas hay. Un tablero con 2 rojas y otro con 3
# en la misma celda dan lo mismo. Por eso, si coinciden varios tableros con contenido
# distinto, la captura no se convierte sola: queda como ambigua.
#
# Uso: python3 classify.py <scores.json> <exercises.json> <out.json>
import json
import sys
from collections import Counter

ATTIRE_WORST, ATTIRE_MEAN, ATTIRE_PEAK = 15, 6, 26
STONES_WORST, STONES_MEAN = 35, 10


def matches(t):
    # Si se ve dónde está el cabezal en la captura, tiene que estar en el mismo lugar.
    if t.get('head') is False:
        return False
    if t['mode'] == 'attire':
        return t['worst'] <= ATTIRE_WORST and t['mean'] <= ATTIRE_MEAN and t['peak'] <= ATTIRE_PEAK
    return t['stones'] == 0 and t['worst'] <= STONES_WORST and t['mean'] <= STONES_MEAN


scores = json.load(open(sys.argv[1]))
exercises = json.load(open(sys.argv[2]))['exercises']
out = {}
for image, d in scores.items():
    ex = exercises[d['exercise']]
    panels = []
    for p in d['panels']:
        good = [t for t in p['top'] if matches(t)]
        if not good:
            panels.append({'grid': p['grid'], 'match': None, 'best': p['top'][0] if p['top'] else None})
            continue
        # Si la vestimenta coincide, se prefiere: es lo que se dibuja sin decir nada.
        good.sort(key=lambda t: (t['mode'] != 'attire', t['board'] is None, t['mean']))
        # Un tablero inicial del ejercicio que se ve **igual** que el mejor —la misma
        # diferencia con la captura, hasta la décima— gana sobre lo que deja un programa: lo
        # que cambia entre los dos no se ve (queda debajo de la vestimenta), así que la
        # consigna se va a ver igual, y no hace falta un archivo nuevo.
        best_mean = min(t['mean'] for t in good)
        same_look = [t for t in good if t['board'] is not None and t['mean'] <= best_mean + 0.05]
        if same_look and any(t['board'] is None for t in good):
            good = [same_look[0]] + [t for t in good if t is not same_look[0] and t['mean'] > best_mean + 0.05]
        contents = {json.dumps(ex['boards'][t['index']]['board'], sort_keys=True) for t in good}
        panels.append({'grid': p['grid'], 'match': good[0], 'ambiguous': len(contents) > 1,
                       'alternatives': [t for t in good[1:]]})
    matched = [p for p in panels if p['match'] and not p['ambiguous']]
    if not panels:
        status = 'sin-tablero'
    elif len(matched) == len(panels):
        status = 'convertida'
    elif matched:
        status = 'parcial'
    elif any(p['match'] for p in panels):
        status = 'ambigua'
    else:
        status = 'sin-coincidencia'
    out[image] = {'exercise': d['exercise'], 'status': status, 'panels': panels, 'size': d['size']}

json.dump(out, open(sys.argv[3], 'w'), indent=1)
print(Counter(v['status'] for v in out.values()))
conv = [v for v in out.values() if v['status'] == 'convertida']
print('paneles de las convertidas', Counter(len(v['panels']) for v in conv))
print('con tableros finales', sum(1 for v in conv if any(p['match']['board'] is None for p in v['panels'])))
print('sin vestimenta pedida', sum(1 for v in conv if any(p['match']['mode'] == 'none' and exercises[v['exercise']].get('attireDir') for p in v['panels'])))
