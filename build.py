#!/usr/bin/env python3
"""Build the self-contained, fully-offline web app -> docs/index.html.

- Inlines assembled.glb + coreS3_face.glb (geometry) + coreS3_face_tex.png as data URIs.
- Inlines three.js r0.160 (core + addons) from ./vendor as data-URI ES modules via an
  importmap, so NO internet / CDN is needed at runtime (no supply-chain dependency).
- Embeds the MIT license notices (three.js, M5Stack M5_Hardware) as required.

docs/index.html is what GitHub Pages serves AND what you can download for offline use
(double-click to run, even without internet).

Edit index.html (the dev source; it uses the three.js CDN and fetches the assets),
then run:  python build.py
"""
import base64, json, pathlib, re, sys

here = pathlib.Path(__file__).parent
vend = here / "vendor"
html = (here / "index.html").read_text(encoding="utf-8")

# bare module specifier -> local vendor filename
modules = {
    "three": "three.module.js",
    "three/addons/controls/OrbitControls.js": "OrbitControls.js",
    "three/addons/controls/TransformControls.js": "TransformControls.js",
    "three/addons/loaders/GLTFLoader.js": "GLTFLoader.js",
    "three/addons/exporters/GLTFExporter.js": "GLTFExporter.js",
    "three/addons/environments/RoomEnvironment.js": "RoomEnvironment.js",
    "three/addons/utils/TextureUtils.js": "TextureUtils.js",
    "three/addons/utils/BufferGeometryUtils.js": "BufferGeometryUtils.js",
}
# relative imports inside addons -> bare specifiers (data: URL modules can't resolve relative paths)
rewrites = {
    "GLTFLoader.js": [("'../utils/BufferGeometryUtils.js'", "'three/addons/utils/BufferGeometryUtils.js'")],
    "GLTFExporter.js": [("'./../utils/TextureUtils.js'", "'three/addons/utils/TextureUtils.js'")],
}

def js_data_uri(src: str) -> str:
    return "data:text/javascript;base64," + base64.b64encode(src.encode("utf-8")).decode("ascii")

imports = {}
for spec, fn in modules.items():
    f = vend / fn
    if not f.exists():
        print(f"ERROR: missing vendor file {f}"); sys.exit(1)
    src = f.read_text(encoding="utf-8")
    for old, new in rewrites.get(fn, []):
        if old not in src:
            print(f"ERROR: rewrite target not found in {fn}: {old}"); sys.exit(1)
        src = src.replace(old, new)
    imports[spec] = js_data_uri(src)

importmap = '<script type="importmap">\n' + json.dumps({"imports": imports}) + '\n</script>'
new_html, n = re.subn(r'<script type="importmap">.*?</script>', importmap, html, count=1, flags=re.S)
if n != 1:
    print("ERROR: could not locate the importmap block in index.html"); sys.exit(1)
html = new_html

def glb_uri(b: bytes) -> str:
    return "data:model/gltf-binary;base64," + base64.b64encode(b).decode("ascii")
def png_uri(b: bytes) -> str:
    return "data:image/png;base64," + base64.b64encode(b).decode("ascii")
inject = (f'<script>window.__GLB__="{glb_uri((here/"assembled.glb").read_bytes())}";'
          f'window.__CORES3GLB__="{glb_uri((here/"coreS3_face.glb").read_bytes())}";'
          f'window.__FACETEX__="{png_uri((here/"coreS3_face_tex.png").read_bytes())}";</script>')
idx = html.find("<head>")
if idx == -1:
    print("ERROR: <head> not found"); sys.exit(1)
html = html[:idx+6] + "\n" + inject + html[idx+6:]

license_block = """<!--
============================================================================
Stack-chan Color Simulator  -  self-contained build
Unofficial fan tool. Not affiliated with M5Stack or the Stack-chan project.
Provided AS-IS, without warranty or support (see README).
============================================================================
This file bundles the following third-party components under the MIT License.
The MIT permission notice is reproduced below as required by that license.

  * three.js (r0.160) - Copyright (c) 2010-2024 three.js authors
      https://github.com/mrdoob/three.js
  * M5Stack 3D hardware models (SKU K151 Stack-chan + CoreS3-Lite)
      - Copyright (c) 2021 M5Stack
      https://github.com/m5stack/M5_Hardware
      (Products/K151_StackChan, Products/K128-Lite_CoreS3-Lite)

----------------------------------------------------------------------------
MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
============================================================================
-->
"""
html = html.replace("<!DOCTYPE html>", "<!DOCTYPE html>\n" + license_block, 1)

dst = here / "docs" / "index.html"
dst.parent.mkdir(exist_ok=True)
dst.write_text(html, encoding="utf-8")
mb = dst.stat().st_size / 1_048_576
print(f"Wrote {dst.relative_to(here)}  ({mb:.2f} MB) - fully self-contained (GitHub Pages + offline).")
