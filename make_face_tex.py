#!/usr/bin/env python3
"""Generate coreS3_face_tex.png  (CoreS3 front "black-glass" decal, RGBA 512x512).

Clean parametric redraw: the front is split into just two FLAT colours -
the recessed display ("screen") and the surrounding black-glass bezel - with
no gradients. The crisp features are drawn on top: dot eyes + straight mouth,
the orange-ring camera, and the small sensor rings/dots.  Feature positions
were measured by eye from the M5Stack CoreS3 front layout (no photo bundled).

The four corners use a rounded alpha so the front tucks inside the case
opening (radius must match index.html `cr = pw*CORNER_FRAC`).

Tweak the tunables and re-run:  python make_face_tex.py
Then rebuild the distributables:  python build_standalone.py && python build_offline.py
"""
from PIL import Image, ImageDraw

S = 512
SS = 3                      # supersample factor for clean anti-aliased edges
# ---- colours (flat) -------------------------------------------------------
C_BEZEL  = (18, 20, 24)     # non-screen black glass (frame + bottom strip) - one flat colour
C_SCREEN = (37, 40, 47)     # recessed display - slightly lighter so it reads as a separate area
C_FRAME  = (27, 30, 35)     # thin recessed-display border
C_EYE    = (236, 237, 239)  # dot eyes / mouth (off-white)
C_MOUTH  = (236, 237, 239)
C_CAM    = (198, 116, 42)   # camera orange ring
C_LENS   = (9, 9, 11)       # camera dark lens
C_LENSHI = (38, 39, 44)     # tiny lens highlight
C_SENSOR = (43, 46, 52)     # faint sensor rings / dots
# ---- geometry (in 512 px space) ------------------------------------------
SCREEN   = (44, 100, 460, 415)   # display rect x0,y0,x1,y1
SCREEN_R = 3                     # display corner radius - small = squared corners (per the real LCD)
FRAME_PAD = 5                    # border thickness around the display
EYES     = [(161, 240), (347, 240)]
EYE_R    = 10
MOUTH    = (195, 313, 295, 8)    # x0, x1, centre-y, thickness
CAM      = (255, 468)            # camera centre
CAM_RO, CAM_W, LENS_R = 17, 3, 12
SENS_RINGS = [(115, 468), (400, 468)]
SENS_RING_R, SENS_RING_W = 12, 2
SENS_DOTS  = [(320, 468), (345, 468)]
SENS_DOT_R = 3
CORNER_FRAC = 0.12               # outer rounded-corner radius / width (MUST match index.html `cr`)
# ---------------------------------------------------------------------------

s = S * SS
im = Image.new('RGB', (s, s), C_BEZEL)
d = ImageDraw.Draw(im)
def sc(v): return int(round(v * SS))
def box(x0, y0, x1, y1): return [sc(x0), sc(y0), sc(x1), sc(y1)]
def circ(cx, cy, r): return [sc(cx - r), sc(cy - r), sc(cx + r), sc(cy + r)]

# recessed display: thin frame, then the flat screen fill (squared corners)
d.rounded_rectangle(box(SCREEN[0]-FRAME_PAD, SCREEN[1]-FRAME_PAD, SCREEN[2]+FRAME_PAD, SCREEN[3]+FRAME_PAD),
                    radius=sc(SCREEN_R+2), fill=C_FRAME)
d.rounded_rectangle(box(*SCREEN), radius=sc(SCREEN_R), fill=C_SCREEN)

# dot eyes
for (ex, ey) in EYES:
    d.ellipse(circ(ex, ey, EYE_R), fill=C_EYE)
# straight mouth (rounded bar)
mx0, mx1, my, mt = MOUTH
d.rounded_rectangle(box(mx0, my-mt/2, mx1, my+mt/2), radius=sc(mt/2), fill=C_MOUTH)

# camera: orange ring + dark lens + tiny highlight
cx, cy = CAM
d.ellipse(circ(cx, cy, CAM_RO), outline=C_CAM, width=sc(CAM_W))
d.ellipse(circ(cx, cy, LENS_R), fill=C_LENS)
d.ellipse(circ(cx-3, cy-3, 3), fill=C_LENSHI)

# sensor rings + dots
for (rx, ry) in SENS_RINGS:
    d.ellipse(circ(rx, ry, SENS_RING_R), outline=C_SENSOR, width=sc(SENS_RING_W))
for (dx, dy) in SENS_DOTS:
    d.ellipse(circ(dx, dy, SENS_DOT_R), fill=C_SENSOR)

# downscale for AA
im = im.resize((S, S), Image.LANCZOS)

# rounded-corner alpha
am = Image.new('L', (s, s), 0)
ImageDraw.Draw(am).rounded_rectangle([0, 0, s-1, s-1], radius=int(CORNER_FRAC * S) * SS, fill=255)
alpha = am.resize((S, S), Image.LANCZOS)
res = im.convert('RGBA')
res.putalpha(alpha)
res.save('coreS3_face_tex.png')
print('wrote coreS3_face_tex.png  screen=%s bezel=%s' % (C_SCREEN, C_BEZEL))
