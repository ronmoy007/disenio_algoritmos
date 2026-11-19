"""armar_keynote.py <pptx> <notas.json> <key|-> <pdf> [etapas.pdf]: abre el pptx en Keynote, pone las notas del presentador y los GIF (de <notas>.gifs.json, como videos en bucle), guarda y exporta."""
import json, subprocess, sys
from pathlib import Path
pptx, notas, key, pdf = sys.argv[1:5]
etapas = sys.argv[5] if len(sys.argv) > 5 else None
n = json.loads(Path(notas).read_text())
gifs = json.loads(Path(notas).with_suffix(".gifs.json").read_text())
esc = lambda t: t.replace("\\", "\\\\").replace('"', '\\"')
L = ['tell application "Keynote"', 'activate', f'set d to open POSIX file "{pptx}"', 'delay 2']
L += [f'set presenter notes of slide {i} of d to "{esc(t)}"' for i, t in enumerate(n, 1) if t]
for lam, ruta, x, y, w in gifs:
    L += [f'tell slide {lam} of d',
          f'set img to make new image with properties {{file:POSIX file "{ruta}"}}',
          f'set width of img to {round(w * 72)}',
          f'set position of img to {{{round(x * 72)}, {round(y * 72)}}}',
          'end tell']
if key != "-":
    L.append(f'save d in POSIX file "{key}"')
L.append(f'export d to POSIX file "{pdf}" as PDF with properties {{all stages:false}}')
if etapas:
    L.append(f'export d to POSIX file "{etapas}" as PDF with properties {{all stages:true}}')
if key == "-":
    L.append("close d saving no")
L.append("end tell")
scr = Path(notas).with_suffix(".applescript"); scr.write_text("\n".join(L))
r = subprocess.run(["osascript", str(scr)], capture_output=True, text=True)
print(r.stdout, r.stderr)
