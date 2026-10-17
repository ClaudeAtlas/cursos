# Hojas de contacto para mirar a ojo: las imágenes, con lo detectado encima.
# Uso: python3 sheet.py <cursos> <detect.json> <filtro: zero|panels|all> <out-prefix> [lista.json]
import json
import sys

from PIL import Image, ImageDraw

cursos, detect_path, which, prefix = sys.argv[1:5]
only = json.load(open(sys.argv[5])) if len(sys.argv) > 5 else None
detect = json.load(open(detect_path))
items = [(k, v) for k, v in detect.items() if (only is None or k in only)]
if which == 'zero':
    items = [(k, v) for k, v in items if not v['panels']]
elif which == 'panels':
    items = [(k, v) for k, v in items if v['panels']]

TW, TH = 300, 230
COLS = 4
PER = 16
for page in range(0, len(items), PER):
    chunk = items[page:page + PER]
    rows = (len(chunk) + COLS - 1) // COLS
    sheet = Image.new('RGB', (COLS * TW, rows * (TH + 24)), 'white')
    draw = ImageDraw.Draw(sheet)
    for i, (k, v) in enumerate(chunk):
        im = Image.open(f'{cursos}/{k}').convert('RGB')
        d = ImageDraw.Draw(im)
        for p in v['panels']:
            d.rectangle(p['grid'], outline=(255, 0, 255), width=2)
        im.thumbnail((TW - 6, TH - 6))
        x, y = (i % COLS) * TW, (i // COLS) * (TH + 24)
        sheet.paste(im, (x + 3, y + 3))
        label = f'{page + i}: {k.split("/")[-4][:30]}/{k.split("/")[-1][:16]}'
        draw.text((x + 3, y + TH), label.encode('latin-1', 'replace').decode('latin-1'), fill='black')
    sheet.save(f'{prefix}-{page // PER:02d}.png')
print(len(items), 'imágenes en', (len(items) + PER - 1) // PER, 'hojas')
