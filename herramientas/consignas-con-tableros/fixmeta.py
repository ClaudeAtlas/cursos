# Pone en el meta.yml el nombre de la carpeta de la vestimenta que el ejercicio usa de
# verdad, cuando nombra una que el IDE no encuentra. Uso: python3 fixmeta.py <cursos> <exercises.json>
import json
import os
import re
import sys

cursos, exercises_path = sys.argv[1:3]
exercises = json.load(open(exercises_path))['exercises']
for d, ex in sorted(exercises.items()):
    if not ex.get('attireFallback') or not ex.get('attireDir'):
        continue
    folder = os.path.basename(ex['attireDir'])
    path = f'{cursos}/{d}/meta.yml'
    # Se respetan los finales de línea del archivo: varios están en CRLF.
    text = open(path, newline='').read()
    pattern = re.compile(r'(^attire:\r?\n(?:[ \t]+.*\n)*?[ \t]+active:[ \t]*)([^\r\n]+)', re.M)
    m = pattern.search(text)
    if not m:
        print('sin attire.active', d)
        continue
    old = m.group(2).strip()
    quoted = f"'{folder}'" if (',' in folder or ':' in folder) else folder
    text = text[:m.start(2)] + quoted + text[m.end(2):]
    open(path, 'w', newline='').write(text)
    print(f'{d}: {old} -> {quoted}')
