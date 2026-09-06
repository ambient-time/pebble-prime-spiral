"""Prime sunflower menu icon. Copyright 2026 Luke Steuber. MIT."""
import math
from pathlib import Path
from PIL import Image,ImageDraw
root=Path(__file__).resolve().parent.parent
im=Image.new('1',(25,25));d=ImageDraw.Draw(im)
for i in range(2,81):
 if any(i%p==0 for p in range(2,math.isqrt(i)+1)):continue
 r=10*math.sqrt(i/80);a=i*math.pi*(3-math.sqrt(5))
 x=round(12+r*math.sin(a));y=round(12-r*math.cos(a));d.point((x,y),fill=1)
d.ellipse((10,10,14,14),fill=1);im.save(root/'resources/menu-icon.png')
