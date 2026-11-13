#!/usr/bin/env python3
"""Render every PDF page and contact sheets for human visual inspection."""
import json
from pathlib import Path
import fitz
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'audit' / 'rendered'
OUT.mkdir(parents=True, exist_ok=True)
for previous in OUT.glob('*'):
    if previous.name.startswith(('page-', 'contact-')) and previous.is_file():
        previous.unlink()
doc = fitz.open(ROOT / 'downloads' / 'business-careers-guide.pdf')
pages = []
for number, page in enumerate(doc, 1):
    page.get_pixmap(matrix=fitz.Matrix(1.5, 1.5), alpha=False).save(OUT / f'page-{number:03d}.png')
    text = page.get_text()
    outside = []
    for word in page.get_text('words'):
        x0, y0, x1, y1 = word[:4]
        if x0 < -0.5 or y0 < -0.5 or x1 > page.rect.width + 0.5 or y1 > page.rect.height + 0.5:
            outside.append(word[4])
    pages.append({'page': number, 'characters': len(text.strip()), 'outside_page_words': outside, 'replacement_characters': text.count('\ufffd')})
for start in range(1, len(doc) + 1, 9):
    end = min(start + 8, len(doc))
    sheet = Image.new('RGB', (1260, 1845), '#d8ddd6')
    drawer = ImageDraw.Draw(sheet)
    for offset, number in enumerate(range(start, end + 1)):
        img = Image.open(OUT / f'page-{number:03d}.png')
        img.thumbnail((400, 572))
        x, y = 10 + (offset % 3) * 420, 24 + (offset // 3) * 615
        sheet.paste(img, (x, y))
        drawer.text((x, y - 18), f'PAGE {number:03d}', fill='#18241d')
    sheet.save(OUT / f'contact-{start:03d}-{end:03d}.jpg', quality=92)
record = {'pdf': 'downloads/business-careers-guide.pdf', 'pages': len(doc), 'rendered_pages': len(pages), 'page_checks': pages,
          'method': 'PyMuPDF render of every page; text bounds and replacement-character scan. Human visual review recorded separately.'}
(ROOT / 'audit' / 'pdf-render-check.json').write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'pages': len(doc), 'contact_sheets': (len(doc)+8)//9, 'outside_words': sum(len(p['outside_page_words']) for p in pages)}, ensure_ascii=False))
