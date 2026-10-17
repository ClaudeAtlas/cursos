# Hojas para revisar a ojo cada coincidencia: la captura recortada y, al lado, lo que
# dibuja el IDE con el tablero elegido.
# Uso: python3 review.py <cursos> <classes.json> <renders> <estado> <out-prefix>
import json
import sys

from PIL import Image, ImageDraw

sys.path.insert(0, sys.argv[0].rsplit('/', 1)[0])
from match import PAD, key_of  # noqa: E402

cursos, classes_path, renders, status, prefix = sys.argv[1:6]
classes = json.load(open(classes_path))
pairs = []
for image, v in classes.items():
    if v['status'] != status:
        continue
    for i, p in enumerate(v['panels']):
        m = p['match'] or p.get('best')
        if not m:
            continue
        pairs.append((image, i, p, m, v['exercise']))

TW, TH = 290, 200
PER = 12
for page in range(0, len(pairs), PER):
    chunk = pairs[page:page + PER]
    sheet = Image.new('RGB', (2 * (2 * TW + 20), ((len(chunk) + 1) // 2) * (TH + 30)), 'white')
    draw = ImageDraw.Draw(sheet)
    for n, (image, i, p, m, exercise) in enumerate(chunk):
        x0 = (n % 2) * (2 * TW + 20)
        y0 = (n // 2) * (TH + 30)
        shot = Image.open(f'{cursos}/{image}').convert('RGB').crop(tuple(m.get('grid', p['grid'])))
        W, H = m['size']
        render = Image.open(f'{renders}/{key_of(exercise, m["index"], m["cell"], m["mode"])}.png').convert('RGB')
        render = render.crop((PAD, PAD, PAD + W * m['cell'], PAD + H * m['cell']))
        for k, im in enumerate([shot, render]):
            im = im.copy()
            im.thumbnail((TW - 6, TH - 6))
            sheet.paste(im, (x0 + k * TW, y0))
        name = image.split('/')[-4][:24] + '/' + image.split('/')[-1][:12]
        label = f'{page + n}: {name} p{i} {m["board"] or "final"} {m["mode"]} m{m["mean"]} w{m["worst"]} s{m["stones"]}'
        draw.text((x0, y0 + TH + 4), label.encode('latin-1', 'replace').decode('latin-1'), fill='black')
    sheet.save(f'{prefix}-{page // PER:02d}.png')
print(len(pairs), 'paneles en', (len(pairs) + PER - 1) // PER, 'hojas')
