# Copyright 2026 Luke Steuber. MIT License.
"""Arrange existing native captures for visual review; these are not store screenshots."""
from pathlib import Path
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1]
TARGETS=('basalt','chalk','diorite','emery','flint','gabbro')
NAMES=('hero','quarter','evening','noon-rollover','midnight-rollover')
for group in range(2):
    sheet=Image.new('RGB',(5*282,3*300),'#15191f');draw=ImageDraw.Draw(sheet)
    for row,target in enumerate(TARGETS[group*3:group*3+3]):
        for col,name in enumerate(NAMES):
            file=ROOT/'build/evidence'/f'{target}-{name}.png'
            if not file.exists():continue
            with Image.open(file) as image:
                image=image.convert('RGB')
                sheet.paste(image,(col*282+(282-image.width)//2,row*300+28+(260-image.height)//2))
            draw.text((col*282+8,row*300+8),f'{target} / {name}',fill='white')
    sheet.save(ROOT/'build'/f'visual-review-{group+1}.png')
