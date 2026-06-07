#!/usr/bin/env python3
"""Generate docs/ogp.png - the social-card image (1200x630) for X / GitHub.

Uses only this project's own assets (the face texture) + drawn shapes — no
official M5Stack / Stack-chan logos or product photos. Run: python make_ogp.py
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
FB = "C:/Windows/Fonts/YuGothB.ttc"   # Yu Gothic Bold
FM = "C:/Windows/Fonts/YuGothM.ttc"   # Yu Gothic Medium
def font(path, size):
    try: return ImageFont.truetype(path, size, index=0)
    except Exception: return ImageFont.truetype("C:/Windows/Fonts/meiryob.ttc", size)

# background gradient
img = Image.new("RGB", (W, H))
top, bot = (239, 242, 247), (214, 221, 231)
px = img.load()
for y in range(H):
    t = y / (H - 1)
    c = tuple(int(top[i] + (bot[i] - top[i]) * t) for i in range(3))
    for x in range(W):
        px[x, y] = c
d = ImageDraw.Draw(img, "RGBA")

# ---- right side: Stack-chan-like illustration (white head + our face texture) ----
cx, cy = 880, 300
# soft shadow
sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
ImageDraw.Draw(sh).rounded_rectangle([cx-190, cy-150, cx+190, cy+210], radius=60, fill=(20, 28, 45, 60))
sh = sh.filter(__import__("PIL.ImageFilter", fromlist=["GaussianBlur"]).GaussianBlur(18))
img.paste(sh, (0, 0), sh)
# base / stand hint
d.rounded_rectangle([cx-90, cy+150, cx+90, cy+205], radius=18, fill=(186, 193, 205, 255))
d.rounded_rectangle([cx-55, cy+128, cx+55, cy+168], radius=14, fill=(206, 212, 222, 255))
# white head shell
hs = 360
d.rounded_rectangle([cx-hs//2, cy-hs//2, cx+hs//2, cy+hs//2], radius=54, fill=(247, 248, 250, 255), outline=(225, 228, 234, 255), width=2)
# face texture centred on the head
face = Image.open("coreS3_face_tex.png").convert("RGBA").resize((312, 312), Image.LANCZOS)
img.paste(face, (cx - 156, cy - 156), face)

# ---- left side: title + subtitle + swatches + tag ----
x0 = 70
d.text((x0, 120), "Stack-chan", font=font(FB, 70), fill=(30, 35, 48))
d.text((x0, 200), "配色シミュレーター", font=font(FB, 50), fill=(43, 53, 80))
sub = font(FM, 23)
d.text((x0, 285), "M5Stack K151 / CoreS3 の 3D プリント配色を、", font=sub, fill=(86, 95, 112))
d.text((x0, 318), "ブラウザでパーツごとに試せるツール。", font=sub, fill=(86, 95, 112))
# filament-color swatches
sw = [(236,236,236),(34,36,40),(196,52,45),(214,120,40),(232,196,60),(74,160,90),
      (60,170,165),(58,108,196),(150,86,196),(214,108,150)]
sx, sy, ss, gap = x0, 380, 34, 9
for i, c in enumerate(sw):
    x = sx + i * (ss + gap)
    d.rounded_rectangle([x, sy, x+ss, sy+ss], radius=8, fill=c+(255,), outline=(255,255,255,180), width=1)
# unofficial tag
d.text((x0, 452), "⚠ 非公式ファンツール（M5Stack / Stack-chan とは無関係・AS-IS）", font=font(FM, 19), fill=(138, 147, 163))
d.text((x0, 484), "Unofficial fan tool — for color reference only", font=font(FM, 17), fill=(150, 158, 172))

img.save("docs/ogp.png")
print("wrote docs/ogp.png", img.size)
