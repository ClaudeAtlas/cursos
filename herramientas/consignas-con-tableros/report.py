# El informe de la conversión: una fila por imagen de consigna, con qué pasó y por qué.
# Las que no son tableros y las que son tableros con anotaciones se marcaron a ojo,
# mirando las hojas de contacto (índices de pending-unique en el orden de detect.json).
import csv
import hashlib
import json
from collections import Counter

detect = json.load(open('detect.json'))
classes = json.load(open('classes.json'))
pending = json.load(open('pending-unique.json'))
items = [k for k in detect if k in pending]
NOT_BOARD = {0, 3, 4, 5, 8, 32, 47, 48, 69, 121}
ANNOTATED = {2, 84, 92, 94, 132}
h = lambda f: hashlib.sha1(open('cursos/' + f, 'rb').read()).hexdigest() if __import__('os').path.exists('cursos/' + f) else None
# Las convertidas ya no están en la rama: se toma el contenido de la copia de main.
import subprocess


def content_hash(f):
    data = subprocess.run(['git', '-C', 'cursos', 'show', f'main:{f}'], capture_output=True).stdout
    return hashlib.sha1(data).hexdigest()


hashes = {k: content_hash(k) for k in classes}
not_board = {hashes[items[i]] for i in NOT_BOARD}
annotated = {hashes[items[i]] for i in ANNOTATED}
rows = []
for k, v in sorted(classes.items()):
    if v['status'] == 'convertida':
        cat = 'convertida'
    elif hashes[k] in not_board:
        cat = 'no-es-tablero'
    elif hashes[k] in annotated:
        cat = 'tablero-con-anotaciones'
    else:
        cat = 'necesita-gbb-a-mano'
    detail = ''
    if v['status'] in ('parcial', 'ambigua'):
        detail = '; '.join(
            f"panel {i + 1}: " + (
                'sin coincidencia' if not p['match'] else
                ('ambiguo entre ' + ', '.join(sorted({(a['board'] or 'final') for a in [p['match']] + p['alternatives']}))
                 if p.get('ambiguous') else (p['match']['board'] or 'final de ' + str(p['match']['from'])))
            ) for i, p in enumerate(v['panels']))
    rows.append({'imagen': k, 'estado': v['status'], 'categoria': cat, 'detalle': detail, 'contenido': hashes[k][:10]})

with open('conversion.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader()
    w.writerows(rows)
print('rutas', Counter(r['categoria'] for r in rows))
uniq = {}
for r in rows:
    uniq.setdefault(r['contenido'], r['categoria'])
print('contenidos distintos', Counter(uniq.values()))
print('por estado de las que necesitan gbb', Counter(r['estado'] for r in rows if r['categoria'] == 'necesita-gbb-a-mano'))
